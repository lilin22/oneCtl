import datetime,os,sys,shutil,pymysql,subprocess
from time import sleep
from mslunit import sqlConct,select,insert,truncate,update,sqlcls
from parseconf import parselgn,parsegtcrl,parsegtrs,parseutt,parserrf,parsepjt,parsepjenv,parsedbcf,parsedcecf,parseuott
from log import *
import requests,json
from inital import cfgdir,casesdir

cachedir = parsedcecf(cfgdir)

def login(cfgdir):
    try:
        lgnuri,username,password = parselgn(cfgdir)
        data = {"username":username,"password":password}
        logger.info("登录oneBridge的请求参数：" + json.dumps(data,ensure_ascii=False))
        response = requests.post(url=lgnuri,data=json.dumps(data, ensure_ascii=False).encode("utf-8"))
        res = response.text
        res = json.loads(res)
        logger.info("登录oneBridge的返回内容：" + json.dumps(res, ensure_ascii=False))
        if res['code'] == 2000:
            token = res['token']
            with open("token.txt","w") as tk:
                tk.write(token)
            # return token
        else:
            logger.error("登录失败，重新登录")
            response = requests.post(url=lgnuri, data=json.dumps(data, ensure_ascii=False).encode("utf-8"))
            res = response.text
            res = json.loads(res)
            logger.info("登录oneBridge的返回内容：" + json.dumps(res, ensure_ascii=False))
            if res['code'] == 2000:
                token = res['token']
                with open("token.txt", "w") as tk:
                    tk.write(token)
                # return token
    except BaseException as msg:
        logger.error(msg)

def getTestRunStart(cfgdir,token):
    gtrsuri,appId = parsegtrs(cfgdir)
    headers = {'token': token}
    params = {"appId":appId}
    try:
        response = requests.get(url=gtrsuri, headers=headers,params=params)
        res = response.text
        res = json.loads(res)
        logger.info("检测是否有测试任务的返回内容：" + json.dumps(res, ensure_ascii=False))
    except:
        res = {'code': 3000, 'msg': '未检测到测试任务', 'runningFlag': 'False'}
        logger.info("请求异常情况下，检测是否有测试任务的返回内容：" + json.dumps(res, ensure_ascii=False))
    return res

def getTestcasesRunList(cfgdir,token):
    gtcrluri,pjtname = parsegtcrl(cfgdir)
    headers = {'token': token}
    params = {}
    logger.info("获取测试用例执行列表的请求参数：" + json.dumps(params, ensure_ascii=False))
    response = requests.get(url=gtcrluri, headers=headers,params=params)
    res = response.text
    print(res)
    res = json.loads(res)
    logger.info("获取测试用例执行列表的返回内容：" + json.dumps(res, ensure_ascii=False))
    return res

def updateOldTestTask(cfgdir,token,taskId,taskRunFlag):
    try:
        uotturi = parseuott(cfgdir)
        headers = {'token': token}
        data = {"taskId":taskId,"taskRunFlag": taskRunFlag}
        logger.info("更新历史测试任务的请求参数：" + json.dumps(data, ensure_ascii=False))
        response = requests.post(url=uotturi, headers=headers, data=json.dumps(data, ensure_ascii=False).encode("utf-8"))
        res = response.text
        res = json.loads(res)
        logger.info("更新历史测试任务的返回内容：" + json.dumps(res, ensure_ascii=False))
        return res
    except BaseException as msg:
        logger.error(msg)

def updateTestTask(optUsr,taskId,cfgdir,token,taskRunFlag):
    try:
        utturi,dtdir = parseutt(cfgdir)
        headers = {'token': token}
        try:
            with open(dtdir + "\\" + optUsr + "\\" + str(taskId) + "\\allure_report\\widgets\\summary.json",'r') as td:
                data = td.read()
            # with open(dtdir,'r') as td:
            #     ratio = td.read()
            data_json = json.loads(data)
            total = data_json["statistic"]["total"]
            passed = data_json["statistic"]["passed"]
            ratio = str('%.2f' % (((passed / total) * 100)) + '%')
        except BaseException as msg:
            logger.error(msg)
            ratio = "0.00%"
        data = {"taskId":taskId,"taskRunFlag": taskRunFlag,"ratio": ratio}
        logger.info("测试结束，更新测试任务的请求参数：" + json.dumps(data, ensure_ascii=False))
        response = requests.post(url=utturi, headers=headers, data=json.dumps(data, ensure_ascii=False).encode("utf-8"))
        res = response.text
        res = json.loads(res)
        logger.info("测试结束，更新测试任务的返回内容：" + json.dumps(res, ensure_ascii=False))
        return res
    except BaseException as msg:
        logger.error(msg)

def accessUpdateTestTask(taskId,cfgdir,token,taskRunFlag,caseTotal=None):
    try:
        utturi,dtdir = parseutt(cfgdir)
        headers = {'token': token}
        ratio = "-0.00%"
        # try:
        #     with open(dtdir + "\\" + optUsr + "\\" + str(taskId) + "\\allure_report\\widgets\\summary.json",'r') as td:
        #         data = td.read()
        #     # with open(dtdir,'r') as td:
        #     #     ratio = td.read()
        #     data_json = json.loads(data)
        #     total = data_json["statistic"]["total"]
        #     passed = data_json["statistic"]["passed"]
        #     ratio = str('%.2f' % (((passed / total) * 100)) + '%')
        # except BaseException as msg:
        #     logger.error(msg)
        #     ratio = "0.00%"
        data = {"taskId":taskId,"taskRunFlag": taskRunFlag,"ratio": ratio,"caseTotal":caseTotal}
        logger.info("开始测试，更新测试任务的请求参数：" + json.dumps(data, ensure_ascii=False))
        response = requests.post(url=utturi, headers=headers, data=json.dumps(data, ensure_ascii=False).encode("utf-8"))
        res = response.text
        res = json.loads(res)
        logger.info("开始测试，更新测试任务的返回内容：" + json.dumps(res, ensure_ascii=False))
        return res
    except BaseException as msg:
        logger.error(msg)

def collectFailedCases(lastReport_dir):
    src_file = ""
    for root, dirs, files in os.walk(lastReport_dir):
        for file in files:
            src_file = os.path.join(root, file)
            print(src_file)
    with open(src_file, "r", encoding='utf-8') as sf:
        sfContent = sf.read()
        sfJson = json.loads(sfContent)
        childrens = sfJson["children"]
        caseSuccessTotal = 0
        caseFailTotal = 0
        casetotal = 0
        casesSuccess = []
        casesFail = []
        for child in childrens:
            subChildrens = child["children"]
            for scd in subChildrens:
                for sscd in scd["children"]:
                    for ssscd in sscd["children"]:
                        if "---" in ssscd["name"]:
                            cid = ssscd["name"].split("---")
                            caseNo = cid[0]
                        elif "[" in ssscd["name"]:
                            cid = ssscd["name"].split("[")
                            cd = cid[-1].split("-")
                            caseNo = cd[0]
                        casetotal = casetotal + 1
                        if ssscd["status"] == "passed":
                            caseSuccessTotal = caseSuccessTotal + 1
                            casesSuccess.append(caseNo)
                        else:
                            caseFailTotal = caseFailTotal + 1
                            casesFail.append(caseNo)

        # logger.info("上次任务的成功用例：" + str(casesSuccess))
        if len(casesSuccess) == caseSuccessTotal:
            logger.info("上次任务的成功用例总数：" + str(caseSuccessTotal))
        if len(casesFail) == caseFailTotal:
            logger.info("上次任务的失败用例总数：" + str(caseFailTotal))
            logger.info("上次任务的失败用例：" + str(casesFail))
        logger.info("上次任务的用例总数：" + str(casetotal))
        return casesFail

def runTask(cfgdir,pjtdir,report_dir,currentdir,resgtrs,token):
    try:
        host, username, password, dbnameBridge, dbnameCtl,port = parsedbcf(cfgdir)
        # conn = pymysql.connect(host, username, password, dbname, int(port))
        connBridge = pymysql.connect(host=host, user=username, password=password, database=dbnameBridge, port=int(port))
        tpSql = "truncate table case_running_static"
        try:
            truncate(connBridge, tpSql)
        except BaseException as msg:
            logger.error(str(msg))

        connCtl = pymysql.connect(host=host, user=username, password=password, database=dbnameCtl, port=int(port))
        tcSql = "truncate table console_msg"
        try:
            truncate(connCtl, tcSql)
        except BaseException as msg:
            logger.error(str(msg))


        optUser = resgtrs['optUser']
        taskId = resgtrs['taskId']
        taskName = resgtrs['taskName']
        runMode = resgtrs['runMode']
        reRunFlag = resgtrs['reRunFlag']

        taskRunFlag = 'False'

        accessUpdateTestTask(taskId, cfgdir, token, "True")
        # content = '【' + optUser + '】' + '在easyTest测试平台上提交【' + taskName +'】测试任务，开始时间：' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        content = '自动化测试平台接收到新任务\n' + '提交人：' + optUser + '\n' + '任务名称：' + taskName + '\n' + '开始时间：' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logger.info('任务开始执行发送消息：' + content)
        try:
            # 待补充
            pass
            # msgSend(cfgdir, content)
        except BaseException as msg:
            logger.error('发送消息异常')
            logger.error(msg)
        rrfdir = parserrf(cfgdir)
        psndir = report_dir + optUser + '\\'
        if not os.path.exists(psndir):
            os.makedirs(psndir)
        taskdir = psndir + str(taskId)
        if os.path.exists(taskdir):
            shutil.rmtree(taskdir)
            logger.info('删除已存在的任务ID路径：' + taskdir)
        os.makedirs(taskdir)
        psndirlist = os.listdir(psndir)
        psndirlist.sort(key=lambda fn: os.path.getmtime(psndir + fn))
        if len(psndirlist) > 10:
            for i in range(len(psndirlist) - 10):
                shutil.rmtree(os.path.join(psndir, psndirlist[i]), ignore_errors=True)
                logger.info("删除测试任务Id为%s的测试报告" % psndirlist[i])
        caseNos = []
        if reRunFlag == "True":
            caseNos = collectFailedCases(rrfdir)
            tpSql = f"update start_test_task set caseTotal = {len(caseNos)} where id = {taskId}"
            try:
                truncate(connBridge, tpSql)
            except BaseException as msg:
                logger.error(str(msg))
            accessUpdateTestTask(taskId, cfgdir, token, "True",len(caseNos))
        else:
            res = getTestcasesRunList(cfgdir, token)
            data = res['data']
            # sorted_data = sorted(data, key=lambda c: c.__getitem__('id'))
            logger.info("测试用例执行列表：" + json.dumps(data,ensure_ascii=False))
            for cn in data:
                caseNos.append(cn["caseNo"])
        logger.info(f"用例总数：{str(len(caseNos))}，用例列表：{str(caseNos)}")
        runCases = {"taskId": taskId, "total": len(caseNos), "caseNos": caseNos}
        with open(casesdir, "w", encoding='utf-8') as ci:
            ci.write(json.dumps(runCases, ensure_ascii=False))
        timeOut = 3
        while timeOut >= 0:
            with open(casesdir, "r", encoding='utf-8') as ci:
                data = ci.read()
                rcs = json.loads(data)
                if rcs["caseNos"] == len(caseNos):
                    break
                else:
                    time.sleep(1)
                    timeOut = timeOut - 1
        if resgtrs['runMode'] == "1" or resgtrs['runMode'] == "2":
            if resgtrs['repeatMode'] == "02":
                runNum = resgtrs['runNum']
                if resgtrs['runMode'] == "2":
                    cmdrun = f"python start_all.py ['-v','-l','-x','-s','--durations=0','--instafail','--count={str(runNum)}']"
                else:
                    cmdrun = f"python start_all.py ['-v','-l','-s','--durations=0','--instafail','--count={str(runNum)}']"
                # cmdrun = 'pytest -v -l --durations=0 --instafail'
                cmdrun = cmdrun + ' ' + taskdir + r'\allure_raw'
                print(cmdrun)
                logger.info("生成调用自动化测试框架的命令：" + cmdrun)
                try:
                    count = 0
                    os.chdir(pjtdir)
                    os.system(cmdrun)
                    # p = os.popen(cmdrun,"r")
                    # print(p.read().encode('g'))
                    # pipe = subprocess.Popen(cmdrun, shell=True, stdout=subprocess.PIPE)
                    # print(pipe.stdout.readline())
                    # print(pipe)
                    # logger.info(pipe.read().decode('utf-8', 'ignore'))
                    # try:
                    #     # print(pipe[0])
                    #     pi = str(pipe[0],'utf-8')
                    #     # print(pi)
                    #     pp = pi.split(r'\r\n')
                    #     print(pp)
                    #     print()
                    #     # for i in iter(pipe[0], "b"):
                    #     for p in pp:
                    #         with open(cachedir, "r", encoding="utf-8") as cc:
                    #             fg = cc.read()
                    #         if fg == "1":
                    #             logger.info(optUser + "撤销任务：" + str(taskId))
                    #             with open(cachedir, "w", encoding="utf-8") as cc:
                    #                 cc.write("2")
                    #             taskRunFlag = 'Destroy'
                    #             sys.exit()
                    #         line = p.decode("utf-8")
                    #         print(line)
                    #         if line == "":
                    #             count += 1
                    #             if count >= 3:
                    #                 connCtl.close()
                    #                 break
                    #         else:
                    #             print(line)
                    #             logger.info(line)
                    #             count = 0
                    #             # print(line.replace("\r\n",""))
                    #             if line != "\r\n":
                    #                 ln = repr(line).replace(r"\r\n", "\n")
                    #                 createTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    #                 istSql = "insert into console_msg (taskId,msg,createTime) values (%d,%s,'%s')" % (taskId, ln, str(createTime))
                    #                 insert(connCtl, istSql)
                    # except BaseException as msg:
                    #     logger.error(msg)
                    os.chdir(currentdir)
                except BaseException as msg:
                    logger.error("自动化脚本异常了")
                    logger.error(msg)
                    os.chdir(currentdir)
        try:
            projectEnv = parsepjenv(cfgdir)
            shutil.copy(projectEnv, taskdir + r'\allure_raw')
            cmdrpt = 'allure generate ' + taskdir + r'\allure_raw' + ' -o ' + taskdir + r'\allure_report'
            logger.info(cmdrpt)
            # os.system(cmdrpt)
            pipe = subprocess.Popen(cmdrpt, shell=True, stdout=subprocess.PIPE).stdout
            logger.info(pipe.read().decode('utf-8', 'ignore'))
        except BaseException as msg:
            logger.error(msg)
        # else:
        #     print("未找到相应的运行模式")
        #     logger.error("未找到相应的运行模式")
        # try:
        #     makeZip(taskdir, taskdir + "\\report.zip")
        # except BaseException as msg:
        #     logger.error(msg)
        # res = cleanTestEnv(cfgdir, token)
        # if res['code'] == 2000:
        #     cleanTestEnvRes(cfgdir,token,taskId,"True")
        # else:
        #     cleanTestEnvRes(cfgdir, token, taskId,"False")
        # res = updateTestTask(cfgdir, token)
        for f in os.listdir(rrfdir):
            file_path = os.path.join(rrfdir,f)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        os.mkdir(rrfdir + "\\" + str(taskId))
        shutil.copy(taskdir + r'\allure_report\data\suites.json',rrfdir + "\\" + str(taskId))
        res = updateTestTask(optUser,taskId, cfgdir, token,taskRunFlag)
        print(res)
        if res['code'] == 2000:
            # content = '【' + optUser + '】' + '在easyTest测试平台上【' + taskName + '】测试任务已完成，结束时间：' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            content = '自动化测试平台任务已完成\n' + '提交人：' + optUser + '\n' + '任务名称：' + taskName + '\n' + '结束时间：' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logger.info('任务完成发送消息：' + content)
            try:
                # 待补充
                pass
                # msgSend(cfgdir, content)
            except BaseException as msg:
                logger.error('发送消息异常')
                logger.error(msg)

        sqlcls(connBridge)
        sqlcls(connCtl)
    except BaseException as msg:
        logger.error(msg)

if __name__ == '__main__':
    try:
        lastTaskId = 0
        login(cfgdir)
        pjtdir, report_dir, currentdir = parsepjt(cfgdir)
        while True:
            with open("token.txt", "r") as tk:
                token = tk.read()
            nowTime = datetime.datetime.now().strftime('%H:%M')
            resgtrs = getTestRunStart(cfgdir, token)
            print(nowTime + "---" + str(resgtrs))
            if resgtrs['runningFlag'] == 'True' and lastTaskId != resgtrs['taskId']:
                runTime = resgtrs['runTime']
                runTimeFlag = True
                if runTime == None:
                    runTimeFlag = False
                if runTime == '':
                    runTimeFlag = False
                if runTimeFlag:
                    while True:
                        nowTime = datetime.datetime.now().strftime('%H:%M')
                        if nowTime == runTime:
                            runTask(cfgdir, pjtdir, report_dir, currentdir, resgtrs, token)
                            lastTaskId = resgtrs['taskId']
                        else:
                            logger.info("未到达任务启动时间")
                            sleep(1)
                        break
                else:
                    runTask(cfgdir, pjtdir, report_dir, currentdir, resgtrs, token)
                    lastTaskId = resgtrs['taskId']
            elif resgtrs['runningFlag'] == 'True' and lastTaskId == resgtrs['taskId']:
                updateOldTestTask(cfgdir, token, lastTaskId, "False")
            else:
                sleep(1)
    except BaseException as msg:
        logger.error(str(msg))

    # lastReport_dir = r'C:\projects\oneCtl\lastReport'
    # collectFailedCases(lastReport_dir)
