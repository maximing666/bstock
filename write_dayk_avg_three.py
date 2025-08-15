# -*- encoding:utf-8 -*-
from asyncio.windows_events import NULL
from time import sleep
import pymysql
from pymysql import IntegrityError
import datetime
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
mysqlport = config.get('mysql', 'port')

connection = pymysql.connect(host = mysqlhost, #host属性
                            user = mysqluser, #用户名 
                            password = mysqlpwd,  #此处填登录数据库的密码
                            db = mysqldb, #数据库名
                            port = int(mysqlport) #端口
                            )
#创建光标对象，一个连接可以有很多光标，一个光标跟踪一种数据状态。
#光标对象作用是：、创建、删除、写入、查询等等
cur = connection.cursor()



if __name__ == '__main__':
    #获取所有表名称
    sql = "show tables;"
    cur.execute(sql)
    tbs=[i[0] for i in cur.fetchall()]
    
    # print(tbs)
    for tb in tbs:
        if "sh.6" in tb or "sz." in tb:
            print(tb)
            # 添加数据库3日均值列字段
            # sql_close_avg_three="alter table `"+tb+"` add column close_avg_three double(255, 4) Default NULL COMMENT '收盘3日均价';"
            # sql_volume_avg_three="alter table `"+tb+"` add column volume_avg_three bigint(255) Default NULL COMMENT '成交数量3日均价';"
            # sql_amount_avg_three="alter table `"+tb+"` add column amount_avg_three double(255, 4) Default NULL COMMENT '成交金额3日均价';"
            # cur.execute(sql_close_avg_three)
            # cur.execute(sql_volume_avg_three)
            # cur.execute(sql_amount_avg_three)

            # 计算3日均值，并插入数据表中。
            #for n in (range(3,41)):
            n=0
            td=(datetime.date.today() + datetime.timedelta(days = -n)).strftime("%Y-%m-%d")
            sql_update_close_avg_three="update `"+tb+"` set close_avg_three=(SELECT AVG(a.close) FROM (select * from `"+tb+"` where tdate<='"+td+"' order by tdate  desc limit 3) a) where tdate='"+td+"';"
            sql_update_volume_avg_three="update `"+tb+"` set volume_avg_three=(SELECT AVG(a.volume) FROM (select * from `"+tb+"` where tdate<='"+td+"' order by tdate desc  limit 3) a) where tdate='"+td+"';"
            sql_update_amount_avg_three="update `"+tb+"` set amount_avg_three=(SELECT AVG(a.amount) FROM (select * from `"+tb+"` where tdate<='"+td+"' order by tdate desc  limit 3) a) where tdate='"+td+"';"
            cur.execute(sql_update_close_avg_three)
            cur.execute(sql_update_volume_avg_three)
            cur.execute(sql_update_amount_avg_three)
            connection.commit()
    connection.close()

