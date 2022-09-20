from asyncio.windows_events import NULL
from time import sleep
import pymysql
from pymysql import IntegrityError
import pandas as pd

connection = pymysql.connect(host = 'localhost', #host属性
                             user = 'root', #用户名 
                             password = 'mxm123',  #此处填登录数据库的密码
                             db = 'bstock' #数据库名
                             )
#创建光标对象，一个连接可以有很多光标，一个光标跟踪一种数据状态。
#光标对象作用是：、创建、删除、写入、查询等等
cur = connection.cursor()

# 文件路径
path = r'D:\bstock\2022-09-19demo_assignDayData.csv'
df = pd.read_csv(path,encoding='utf-8')
linenum = df.shape[0]
#读取文件内容，插入MySQL中。
for i in range(0,linenum):
    tdate = df.iloc[i][0]
    code = df.iloc[i][1]
    open = df.iloc[i][2]
    high = df.iloc[i][3]
    low = df.iloc[i][4]
    close = df.iloc[i][5]
    volume = df.iloc[i][6]
    if volume == NULL:
        volume = 0
        print("==================")
    amount = df.iloc[i][7]
    if amount == NULL:
        amount = 0
    turn = df.iloc[i][8]
    if turn == NULL:
        turn = 0    
    tradestatus = df.iloc[i][9]
    if tradestatus == NULL:
        tradestatus = 0    
    pctchg = df.iloc[i][10]
    if pctchg == NULL:
        pctchg = 0    
    pettm = df.iloc[i][11]
    if pettm == NULL:
        pettm = 0    
    #获取所有表名称
    sql = "show tables;"
    cur.execute(sql)
    tbs=cur.fetchall()
    
    filetb=(code,)
    # sql="drop table `%s`;"%(filetb)
    # print(sql)
    # cur.execute(sql)
    
    if filetb not in tbs:
        #print("out",tbs) 
        sql="CREATE TABLE `bstock`.`%s`  (`tdate` date NOT NULL COMMENT '交易日期',  `code` varchar(255) NOT NULL COMMENT '股票代码',  `open` double(255, 4) NOT NULL COMMENT '开盘',  `high` double(255, 4) NOT NULL COMMENT '最高',  `low` double(255, 4) NOT NULL COMMENT '最低',  `close` double(255, 4) NOT NULL COMMENT '收盘', `volume` bigint(255) COMMENT '成交数量', `amount` double(255, 4) COMMENT '成交金额', `turn` double(255, 6) COMMENT '换手率', `tradestatus` int(4) NOT NULL COMMENT '交易状态', `pctchg` double(255, 6) COMMENT '涨跌幅', `pettm` double(255, 6) NOT NULL COMMENT '滚动市盈率',  PRIMARY KEY (`tdate`));"%(filetb)
        cur.execute(sql)
    sql="insert into `bstock`.`%s`(tdate,code,open,high,low,close,volume,amount,turn,tradestatus,pctchg,pettm) values ('%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s); "%(code,tdate,code,open,high,low,close,volume,amount,turn,tradestatus,pctchg,pettm)
    print(sql)
    try :
        cur.execute(sql)
    except IntegrityError as duplicate_entry_err:
        #print(duplicate_entry_err.__str__())
        pass
    finally:
    #关闭数据库连接            
        connection.close()