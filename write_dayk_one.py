# -*- encoding:utf-8 -*-
from asyncio.windows_events import NULL
from time import sleep
import pymysql
from pymysql import IntegrityError
import pandas as pd
import os
import shutil
import configparser
# import t3


#生成configparser对象
config = configparser.ConfigParser()
#读取配置文件
# conffilename = r'E:\github\bstock\config\config.ini'
conffilename = './config/config.ini'
config.read(conffilename, encoding='utf-8')
#获取配置文件变量值
mysqlhost = config.get('mysql', 'host')
mysqluser = config.get('mysql', 'user')
mysqlpwd = config.get('mysql', 'password')
mysqldb = config.get('mysql', 'daykdb')
downloadpath = config.get('dayk', 'downloadpath')
importedpath = config.get('dayk', 'importedpath')

connection = pymysql.connect(host = mysqlhost, #host属性
                            user = mysqluser, #用户名 
                            password = mysqlpwd,  #此处填登录数据库的密码
                            db = mysqldb #数据库名
                            )
#创建光标对象，一个连接可以有很多光标，一个光标跟踪一种数据状态。
#光标对象作用是：、创建、删除、写入、查询等等
cur = connection.cursor()

#遍历指定目录，显示目录下所有文件名称。
def eachFile(filepath):
    pathDir = os.listdir(filepath)
    list1 = []
    for allDir in pathDir:
        child = os.path.join('%s\%s' % (filepath, allDir))
        list1.append(child )
    return list1

if __name__ == '__main__':
    # t3.Logger()
    # 文件路径
    # downloadpath = r"D:\\bstock\\download\\dayk\\"
    # importedpath = r'D:\\bstock\\imported\\dayk\\'
    print("源文件：",eachFile(downloadpath))  
    for fpath in eachFile(downloadpath):
        print(fpath)
        df0 = pd.read_csv(fpath,encoding='utf-8',keep_default_na=True)
        #将表格中空值补充为0
        df = df0.fillna(0)

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
            amount = df.iloc[i][7]
            turn = df.iloc[i][8]
            tradestatus = df.iloc[i][9]
            pctchg = df.iloc[i][10]
            pettm = df.iloc[i][11]
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
                sql="CREATE TABLE `"+mysqldb+"`.`%s`  (\
                    `tdate` date NOT NULL COMMENT '交易日期', \
                    `code` varchar(255) NOT NULL COMMENT '股票代码',  \
                    `open` double(255, 4) NOT NULL COMMENT '开盘',  \
                    `high` double(255, 4) NOT NULL COMMENT '最高',  \
                    `low` double(255, 4) NOT NULL COMMENT '最低',  \
                    `close` double(255, 4) NOT NULL COMMENT '收盘', \
                    `volume` bigint(255) Default NULL COMMENT '成交数量', \
                    `amount` double(255, 4) Default NULL COMMENT '成交金额', \
                    `turn` double(255, 6) Default NULL COMMENT '换手率', \
                    `tradestatus` int(4) NOT NULL COMMENT '交易状态', \
                    `pctchg` double(255, 6) Default NULL COMMENT '涨跌幅', \
                    `pettm` double(255, 6) NOT NULL COMMENT '滚动市盈率',  \
                    `close_avg_three` double(255, 4) Default NULL COMMENT '收盘3日均价', \
                    `volume_avg_three` bigint(255) Default NULL COMMENT '成交数量3日均价', \
                    `amount_avg_three` double(255, 4) Default NULL COMMENT '成交金额3日均价', \
                    PRIMARY KEY (`tdate`));"%(filetb)
                cur.execute(sql)
            sql="insert into `"+mysqldb+"`.`%s`(tdate,code,open,high,low,close,volume,amount,turn,tradestatus,pctchg,pettm) values ('%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s); "%(code,tdate,code,open,high,low,close,volume,amount,turn,tradestatus,pctchg,pettm)
            print(sql)

            try:
                cur.execute(sql)
            except IntegrityError as duplicate_err:
                print("主键已存在。")
            finally:
                connection.commit()
        #处理完文件后，将文件迁移到新目录
        try:
            shutil.move(fpath,importedpath)
        except OSError:
            fname = fpath.split('/')[-1]
            os.remove(importedpath + fname)
            shutil.move(fpath,importedpath)
        sleep(3)
    connection.close()

