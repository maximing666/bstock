from time import sleep
import baostock as bs
import pandas as pd

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
    print("nonono") 
    sleep(111111)   
result_dupont = pd.DataFrame(dupont_list, columns=rs_dupont.fields)
# 打印输出
print(result_dupont)
# 结果集输出到csv文件
#result_dupont.to_csv("D:\\bstock\\download\\dupont\\dupont_data.csv", encoding="gbk", index=False)

# 登出系统
bs.logout()