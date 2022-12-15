# -*- coding: UTF-8 –*-
from logging import exception
from time import sleep
from tkinter import SCROLL
import baostock as bs
import pandas as pd
import datetime
import configparser
import pymysql
from pymysql import IntegrityError
import os


#生成configparser对象
config = configparser.ConfigParser()
#读取配置文件
#conffilename = r'D:\github\bstock\config\config.ini'
conffilename = './config/config.ini'
config.read(conffilename, encoding='utf-8')
#获取配置文件变量值
print('配置文件信息：', config.sections())
mysqlhost = config.get('mysql', 'host')
mysqluser = config.get('mysql', 'user')
mysqlpwd = config.get('mysql', 'password')
mysqldb = config.get('mysql', 'daykdb')

#连接MySQL数据库
connection = pymysql.connect(host = mysqlhost, #host属性
                             user = mysqluser, #用户名 
                             password = mysqlpwd,  #此处填登录数据库的密码
                             db = mysqldb #数据库名
                             )
#创建光标对象，一个连接可以有很多光标，一个光标跟踪一种数据状态。
#光标对象作用是：、创建、删除、写入、查询等等
cur = connection.cursor()
sql = "show tables;"
codes = cur.execute(sql)
tbs1 = [i[0] for i in cur.fetchall()]

filetb = 'codeinfo'
# sql="drop table `%s`;"%(filetb)
# print(sql)
# cur.execute(sql)

if filetb not in tbs1: 
    sql="CREATE TABLE `"+mysqldb+"`.`%s`  (\
        `code` varchar(255) NOT NULL COMMENT '股票代码', \
        `codename` varchar(255) NULL COMMENT '股票名称', \
        `ipodate` date Default NULL COMMENT '上市日期', \
        `outdate` varchar(255) Default NULL COMMENT '退市日期', \
        `type` varchar(255) NULL COMMENT '证券类型。其中1股票2指数3其它4可转债5ETF', \
        `status` varchar(255) NULL COMMENT '上市状态。其中1上市0退市', \
        PRIMARY KEY (`code`));"%(filetb)
    cur.execute(sql)

#去除tbs表名列表中非证券名。
tbs = []
for i in tbs1:
    if i.startswith("sh.") or i.startswith("sz."):
        tbs.append(i)

# 登陆系统
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

for code in tbs:
    print(code)
    # 获取证券基本资料
    rs = bs.query_stock_basic(code)
    data_list = []
    while  (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
        #导入数据库
        if len(data_list) > 0: 
                for m in data_list[0]:
                    if m == '':
                        data_list[0][data_list[0].index(m)] = 0
                sql = "insert into `"+mysqldb+"`.`%s`(code,codename,ipodate,outdate,type,status) values ('%s','%s','%s','%s','%s',%s);"%(filetb,data_list[0][0],data_list[0][1],data_list[0][2],data_list[0][3],data_list[0][4],data_list[0][5])
                print(sql)
                try:
                    cur.execute(sql)
                except IntegrityError as duplicate_err:
                    print("主键已存在。")
        else:
            print(code,  "Have no data..")
            #break            
    #mysql提交修改
    connection.commit()
#关闭mysql连接
connection.close()
# 登出系统
bs.logout()