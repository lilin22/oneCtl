from mslunit import sqlConct,createTbe,sqlcls
from  parseconf import parsedbcf
import pymysql

basePath = r'C:\projects\oneCtl'
cfgdir = basePath + '\\base.conf'
casesdir = basePath + '\\taskCases.txt'

host,username,password,dbnameBridge,dbnameCtl,port = parsedbcf(cfgdir)

msd = "CREATE TABLE IF NOT EXISTS msgsend (ID int(10)  NOT NULL AUTO_INCREMENT,\
      appName varchar(100),\
      accessToken varchar(1000),\
      expires_in int(100),\
      createTime datetime,\
      updateTime datetime,\
      PRIMARY KEY (ID))"

csemsg = "CREATE TABLE IF NOT EXISTS console_msg (ID int(10)  NOT NULL AUTO_INCREMENT,\
      taskId int(10),\
      msg varchar(10000),\
      createTime datetime,\
      PRIMARY KEY (ID))"

conn = pymysql.connect(host=host, user=username, password=password, database=dbnameCtl, port=int(port))
createTbe(conn,msd)
createTbe(conn,csemsg)
sqlcls(conn)