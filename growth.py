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
import t3

t3.Logger()
#生成configparser对象
config = configparser.ConfigParser()
#读取配置文件
#conffilename = r'D:\github\bstock\config\config.ini'
conffilename = './config/config.ini'
config.read(conffilename, encoding='utf-8')
#获取配置文件变量值
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
tbs = [i[0] for i in cur.fetchall()]

filetb = 'growth'
# sql="drop table `%s`;"%(filetb)
# print(sql)
# cur.execute(sql)

if filetb not in tbs: 
    sql="CREATE TABLE `"+mysqldb+"`.`%s`(\
        `code` varchar(255) NOT NULL COMMENT '股票代码', \
        `year` varchar(255) NOT NULL COMMENT '年', \
        `quarter` varchar(255) NOT NULL COMMENT '季度', \
        `pubdate` date Default NULL COMMENT '发布日期', \
        `statdate` date Default NULL COMMENT '统计到最后一天日期', \
        `yoyequity` decimal(20, 10)  DEFAULT 0 COMMENT '净资产同比增长率',  \
        `yoyasset` decimal(20, 10)  DEFAULT 0 COMMENT '总资产同比增长率', \
        `yoyni` decimal(20, 10)  DEFAULT 0 COMMENT '净利润同比增长率', \
        `yoyepsbasic` decimal(20, 10)  DEFAULT 0 COMMENT '基本每股收益同比增长率', \
        `yoypni` decimal(20, 10)  DEFAULT 0 COMMENT '归属母公司股东净利润同比增长率', \
        PRIMARY KEY (`code`,`year`,`quarter`));"%(filetb)
    print(sql)
    cur.execute(sql)
else:
    tbs.remove('dupont')
    tbs.remove('growth')
i = 1
while(i<1000):
    k = str(i)        
    j = 'sh.' + k.zfill(6)
    try:
        tbs.remove(j)  
    except ValueError:
        print('tbs list have no this value:', j)
    finally:
        i = i + 1

# 登陆系统
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

nowyear = datetime.date.today().year
i = nowyear
while(i <= nowyear):
    j = 3
    while(j >= 1):
        for code in tbs:
            # 查询杜邦指数
            growth_list = []
            rs_growth = bs.query_growth_data(code=code, year=i, quarter=j)
            while (rs_growth.error_code == '0') & rs_growth.next():
                growth_list.append(rs_growth.get_row_data())
            
            if len(growth_list) > 0: 
                for m in growth_list[0]:
                    if m == '':
                        growth_list[0][growth_list[0].index(m)] = 0
                sql = "insert into `"+mysqldb+"`.`%s`(code,year,quarter,pubdate,statdate,yoyequity,yoyasset,yoyni,yoyepsbasic,yoypni) values ('%s','%s','%s','%s','%s',%s,%s,%s,%s,%s);"%(filetb,growth_list[0][0],i,j,growth_list[0][1],growth_list[0][2],growth_list[0][3],growth_list[0][4],growth_list[0][5],growth_list[0][6],growth_list[0][7])
                print(sql)
                try:
                    cur.execute(sql)
                except IntegrityError as duplicate_err:
                    print("主键已存在。")
            else:
                print(code, i, j, "Have no data..")
                #break 
        connection.commit()           
        j = j - 1
    i = i + 1
    

#关闭mysql连接
connection.close()
# 登出系统
bs.logout()