# -*- coding: UTF-8 –*-
from logging import exception
from time import sleep
import datetime
import configparser
import pymysql
from pymysql import IntegrityError


def fetch():
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
    #select dupont.code,codeinfo.codename,year 年份,`quarter` 季度,pubdate 发布日期,dupontroe 净资产收益率,dupontnitogr 净利率 from dupont,codeinfo where dupont.code = codeinfo.code and duponttaxburden > 0 and dupontroe > 0.3 and dupontnitogr> 0.2 and dupont.code not like 'sh.688%'  ORDER BY dupont.year desc,dupont.quarter desc,dupontnitogr desc  limit 20; 
    sql1 = "select dupont.code,codeinfo.codename from dupont,codeinfo where dupont.code = codeinfo.code and duponttaxburden > 0 and dupontroe > 0.3 and dupontnitogr> 0.2 and dupont.code not like 'sh.688%'  ORDER BY dupont.year desc,dupont.quarter desc,dupontnitogr desc  limit 30; "
    cur.execute(sql1)
    result1 = cur.fetchall()
    #print(result1)
    #select growth.code,codeinfo.codename,growth.year 年,growth.quarter,growth.pubdate 发布日期,growth.yoyequity 净资产同比,growth.yoyasset 总资产同比,growth.yoyni 净利润同比,growth.yoyepsbasic 每股收益同比,growth.yoypni 归属母公司净利润同比 from growth,codeinfo where  growth.code = codeinfo.code ORDER BY growth.year desc,growth.quarter desc,yoyepsbasic desc limit 20;
    sql2 = "select growth.code,codeinfo.codename from growth,codeinfo where  growth.code = codeinfo.code ORDER BY growth.year desc,growth.quarter desc,yoyepsbasic desc limit 30;"
    cur.execute(sql2)
    result2 = cur.fetchall()
    #print(result2)

    #关闭mysql连接
    connection.close()

    #两个元组结果的交集
    focuspool = tuple(set(result1) & set(result2))
    print(focuspool)
    return(focuspool)

if __name__ == '__main__':
    fetch()