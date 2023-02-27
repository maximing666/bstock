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
    updays = int(config.get('result_days_up', 'updays'))


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
    for i in ('codeinfo','dupont','growth'):
        tbs.remove(i)
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
    
    code_list=[]    
    
    for tb  in tbs: 
        sql="select date_format(tdate,'%Y-%m-%d'),code,pctchg,amount from `"+mysqldb+"`.`%s` order by tdate desc limit %s;"%(tb,updays)
        cur.execute(sql)
        r=cur.fetchall()
        r_len=len(r)
        print(r)
        if r_len == updays:
            j=0
            flag=0
            while j<updays:
                print(r,r_len,' j=',j)            
                if r[j][2]>0 :
                    if j+1<r_len:
                        flag = flag+1
                else:
                    break
                j=j+1
            if flag == updays:
                print(tb,'true')
                print(r)
                code_list.append(r[0][1])
        

    #关闭mysql连接
    connection.close()

    print("近期连续上涨：",code_list)    
    return(code_list) 
    
if __name__ == '__main__':
    fetch()