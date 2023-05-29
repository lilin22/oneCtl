from configparser import ConfigParser

def parselgn(cfgdir):
    cfp = ConfigParser()
    cfp.read(cfgdir, encoding="utf-8-sig")
    uri = cfp.get('baseuri', 'uri')
    login = cfp.get('login', 'login_uri')
    login_uri = uri + login
    username = cfp.get('login', 'username')
    password = cfp.get('login', 'password')
    return login_uri,username,password

def parsegtrs(cfgdir):
    cfp = ConfigParser()
    cfp.read(cfgdir, encoding="utf-8-sig")
    uri = cfp.get('baseuri', 'uri')
    getTestRunStart = cfp.get('gtrs', 'getTestRunStart_uri')
    getTestRunStart_uri = uri + getTestRunStart
    appId = cfp.get('gtrs','appId')
    return getTestRunStart_uri,appId

def parsegtcrl(cfgdir):
    cfp = ConfigParser()
    cfp.read(cfgdir, encoding="utf-8-sig")
    uri = cfp.get('baseuri', 'uri')
    getTestcasesRunList = cfp.get('gtcrl', 'getTestcasesRunList_uri')
    getTestcasesRunList_uri = uri + getTestcasesRunList
    project_id = cfp.get('gtcrl','project_id')
    return getTestcasesRunList_uri,project_id

def parsedcecf(cfgdir):
    cfp = ConfigParser()
    cfp.read(cfgdir, encoding="utf-8-sig")
    cachedir = cfp.get('destroyCache', 'cachedir')
    return cachedir

def parseuott(cfgdir):
    cfp = ConfigParser()
    cfp.read(cfgdir, encoding="utf-8-sig")
    uri = cfp.get('baseuri', 'uri')
    updateOldTestTask = cfp.get('updateOldTestTask', 'uott')
    updateOldTestTask_uri = uri + updateOldTestTask
    return updateOldTestTask_uri

def parserrf(cfgdir):
    cfp = ConfigParser()
    cfp.read(cfgdir, encoding="utf-8-sig")
    failedCases_dir = cfp.get('reRunFailed', 'failedCases')
    return failedCases_dir

def parseutt(cfgdir):
    cfp = ConfigParser()
    cfp.read(cfgdir, encoding="utf-8-sig")
    uri = cfp.get('baseuri', 'uri')
    updateTestTask = cfp.get('utt', 'updateTestTask_uri')
    updateTestTask_uri = uri + updateTestTask
    dtdir = cfp.get('utt', 'dtdir')
    return updateTestTask_uri,dtdir

def parsepjt(cfgdir):
    cfp = ConfigParser()
    cfp.read(cfgdir, encoding="utf-8-sig")
    project_dir = cfp.get('project', 'project_dir')
    report_dir = cfp.get('project', 'report_dir')
    current_dir = cfp.get('project', 'current_dir')
    return project_dir,report_dir,current_dir

def parsepjenv(cfgdir):
    cfp = ConfigParser()
    cfp.read(cfgdir, encoding="utf-8-sig")
    projectEnv = cfp.get('projectEnv', 'projectEnv_dir')
    return projectEnv

def parsedbcf(cfgdir):
    cfp = ConfigParser()
    cfp.read(cfgdir, encoding="utf-8-sig")
    host = cfp.get('mysql', 'host')
    username = cfp.get('mysql', 'username')
    password = cfp.get('mysql', 'password')
    dbnameBridge = cfp.get('mysql', 'dbnameBridge')
    dbnameCtl = cfp.get('mysql', 'dbnameCtl')
    port = cfp.get('mysql', 'port')
    return host,username,password,dbnameBridge,dbnameCtl,port