# -*- coding: UTF-8 –*-
from logging import exception
from time import sleep
from tkinter import SCROLL
import baostock as bs
import pandas as pd
import datetime
import configparser
import pymysql

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

filetb = 'dupont'
# sql="drop table `%s`;"%(filetb)
# print(sql)
# cur.execute(sql)

if filetb not in tbs: 
    sql="CREATE TABLE `"+mysqldb+"`.`%s`  (\
        `code` varchar(255) NOT NULL COMMENT '股票代码', \
        `pubdate` date Default NULL COMMENT '发布日期', \
        `statdate` date NOT NULL COMMENT '统计到最后一天日期', \
        `dupontroe` double(20, 10) Default NULL COMMENT '净资产收益率',  \
        `dupontassetstoequity` double(20, 10) Default NULL COMMENT '权益乘数,反映企业财务杠杆效应强弱和财务风险', \
        `dupontassetturn` double(20, 10) Default NULL COMMENT '总资产周转率，反映企业资产管理效率的指标', \
        `dupontpnitoni` double(20, 10) Default NULL COMMENT '归属母公司股东的净利润/净利润，反映母公司控股子公司百分比。如果企业追加投资，扩大持股比例，则本指标会增加。', \
        `dupontnitogr` double(20, 10) Default NULL COMMENT '净利润/营业总收入，反映企业销售获利率', \
        `duponttaxburden` double(20, 10) Default NULL COMMENT '净利润/利润总额，反映企业税负水平，该比值高则税负较低。净利润/利润总额=1-所得税/利润总额', \
        `dupontintburden` double(20, 10) Default NULL COMMENT '利润总额/息税前利润，反映企业利息负担，该比值高则税负较低。利润总额/息税前利润=1-利息费用/息税前利润', \
        `dupontebittogr` double(20, 10) Default NULL COMMENT '息税前利润/营业总收入，反映企业经营利润率，是企业经营获得的可供全体投资人（股东和债权人）分配的盈利占企业全部营收收入的百分比', \
        PRIMARY KEY (`code`,`statdate`));"%(filetb)
    cur.execute(sql)
else:
    for i in ['dupont','sh.000001','sh.000002']:
        tbs.remove(i)  

# 登陆系统
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

for code in tbs:
    print(code)
    nowyear = datetime.date.today().year
    i = 2010
    while(i <= nowyear):
        j = 1
        while(j <= 4):
            # 查询杜邦指数
            dupont_list = []
            rs_dupont = bs.query_dupont_data(code=code, year=i, quarter=j)
            while (rs_dupont.error_code == '0') & rs_dupont.next():
                dupont_list.append(rs_dupont.get_row_data())
            
            if len(dupont_list) > 0: 
                print("-----", rs_dupont.fields) 
                result_dupont = pd.DataFrame(dupont_list, columns=rs_dupont.fields)
                # 打印输出
                print(result_dupont)
                sleep(111111)  
            else:
                print(code, i, j, "Have no data..") 
                i = i + 1
                break
            i = i + 1
            j = j + 1



sql="insert into `"+mysqldb+"`.`%s`(tdate,code,open,high,low,close,volume,amount,turn,tradestatus,pctchg,pettm) values ('%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s); "%(code,tdate,code,open,high,low,close,volume,amount,turn,tradestatus,pctchg,pettm)
print(sql)
sleep(100)


try:
    cur.execute(sql)
except IntegrityError as duplicate_err:
    print("主键已存在。")
finally:
    connection.commit()

print(codes)
print("==========")
sleep(100)

# 登陆系统
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)


# 查询杜邦指数
dupont_list = []
rs_dupont = bs.query_dupont_data(code="sh.600316", year=2022, quarter=2)
while (rs_dupont.error_code == '0') & rs_dupont.next():
    dupont_list.append(rs_dupont.get_row_data())
if len(dupont_list) > 0: 
    print("-----", rs_dupont.fields)   
else:
    print("Have no data..") 
    sleep(111111)   
result_dupont = pd.DataFrame(dupont_list, columns=rs_dupont.fields)
# 打印输出
print(result_dupont)
# 结果集输出到csv文件
#result_dupont.to_csv("D:\\bstock\\download\\dupont\\dupont_data.csv", encoding="gbk", index=False)

# 登出系统
bs.logout()