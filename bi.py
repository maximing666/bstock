from fileinput import close
import matplotlib.pyplot as plt 
import pandas as pd 
import pymysql

#建立数据库连接
connection = pymysql.connect(host = 'localhost', #host属性
                             user = 'root', #用户名 
                             password = 'mxm123',  #此处填登录数据库的密码
                             db = 'bstock' #数据库名
                             )
#读取数据库表数据
data = pd.read_sql("select tdate,close from sh.000001", con=connection)                             
