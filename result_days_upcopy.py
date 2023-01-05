# -*- coding: UTF-8 –*-
from logging import exception
from time import sleep
import datetime
import configparser
import pymysql
from pymysql import IntegrityError
# import t3


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
    cur.execute(sql)
    tbs1 = [i[0] for i in cur.fetchall()]
    tbs = []
    for i in tbs1:
        if i.startswith("sh.") or i.startswith("sz."):
            tbs.append(i)
          
    # 去除sh.000001到sh.100000
    # i = 1
    # while(i<1000):
    #     k = str(i)        
    #     j = 'sh.' + k.zfill(6)
    #     try:
    #         tbs.remove(j)  
    #     except ValueError:
    #         print('tbs list have no this value:', j)
    #     finally:
    #         i = i + 1
    
    code_list=[]    
    while len(code_list) >= 0 :
        for tb  in tbs: 
            sql="select date_format(tdate,'%Y-%m-%d'),a.code,b.codename,a.pctchg,a.amount,a.close from `"+mysqldb+"`.`%s` a,codeinfo b where  a.code = b.code order by a.tdate desc limit %s;"%(tb,updays)
            cur.execute(sql)
            r=cur.fetchall()
            r_len=len(r)
            #print(r)
            if r_len == updays: 
                #  涨跌幅、成交金额连续上涨     
                if all([r[n][3]>0  for n in range(r_len)]) and all([r[n][3] > r[n+1][3] and r[n][4] > r[n+1][4] for n in range(r_len -1)]):
                    # print(tb,'true')
                    code_list.append((r[0][1],r[0][2],'%.2f%%'%((r[0][5]/r[updays-1][5]-1)*100)))
        code_list.sort(key=lambda x:x[2],reverse=True)
        print(updays,"days,result long:",len(code_list),code_list)
        sleep(5)
        if len(code_list) > 1:            
            updays = updays + 1
            code_list_tmp = code_list.copy()
            code_list.clear()
        elif len(code_list) == 0:
            code_list = code_list_tmp
            updays = updays - 1
            break
        else:
            break

    #关闭mysql连接
    connection.close()
    viewresult = str(updays)+"日涨"+str(len(code_list))+"只：)",code_list  
    return(viewresult) 

def put_viewrecommend():
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
    cur.execute(sql)
    tbs = [i[0] for i in cur.fetchall()]
    #创建推荐表
    viewtb='viewrecommend'
    # sql="drop table `%s`;"%(filetb)
    # print(sql)
    # cur.execute(sql)
    vtext1 = str(fetch())
    vtext = vtext1.replace("'","")
    #print(vtext)
    if viewtb not in tbs:
        #print("out",tbs) 
        sql="CREATE TABLE `"+mysqldb+"`.`%s`  (\
            `vdate` date NOT NULL COMMENT '推荐日期', \
            `vtext` varchar(1024) NOT NULL COMMENT '推荐内容';"%(viewtb)
        cur.execute(sql)
    sql="insert into `"+mysqldb+"`.`%s`(vdate,vtext) values ('%s','%s'); "%(viewtb,datetime.datetime.now().strftime('%Y-%m-%d'),vtext)
    #print(sql) 
    try:
        cur.execute(sql)
    except IntegrityError as duplicate_err:
        print("主键已存在。")
    finally:
        connection.commit()
    connection.close()
    return(vtext)
    
 

if __name__ == '__main__':
    # t3.Logger()
    # fetch()
    put_viewrecommend()