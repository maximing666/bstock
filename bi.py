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
data = pd.read_sql("select tdate,close from `sh.000001`", con=connection)                             
#数据转化为列表
x = list(data.tdate)  #日期
y = list(data.close)  #收盘价

#设置折线样式
plt.plot(x,y, "g--")

#设置x坐标轴的范围
plt.xlim(19200,19300)
#设置y坐标轴的范围
plt.ylim(0,4000)

#设置x轴文字的标题
plt.xlabel("date")
#设置y轴文字的标题
plt.ylabel("yuan")


#设置图表的标题
plt.title("--------")

plt.show()
print(type(x))
#关闭数据库连接
connection.close()