##获取日期
# import datetime
# nowday=datetime.date.today()
# nday=(datetime.date.today() + datetime.timedelta(days = -3)).strftime("%Y-%m-%d")
# print("今天日期：",nowday)
# print("n天前日期：",nday)
#

#pandas读取csv文件
import pandas as pd
df = pd.read_csv("D:\\2021-12-31demo_assignDayData.csv")
print(df.to_string())