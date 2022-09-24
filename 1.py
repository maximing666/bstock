##获取日期
# import datetime
# nowday=datetime.date.today()
# nday=(datetime.date.today() + datetime.timedelta(days = -3)).strftime("%Y-%m-%d")
# print("今天日期：",nowday)
# print("n天前日期：",nday)


#pandas读取csv文件
# import pandas as pd
# df = pd.read_csv("D:\\2021-12-31demo_assignDayData.csv")
# print(df.to_string())

#configparser模块
import configparser
#生成configparser对象
config = configparser.ConfigParser()
#读取配置文件
# conffilename = r'E:\github\bstock\config\config.ini'
conffilename = r'.\\config\\config.ini'
config.read(conffilename, encoding='utf-8')
#获取节点sections
all_sections = config.sections()
print('sections:', all_sections)
#检查option是否存在
print(config.has_option('dayk','startday'))
#获取指定section中option的值
startday = config.get('dayk','startday')
print(startday)
