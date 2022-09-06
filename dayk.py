import baostock as bs
import pandas as pd
import datetime

nday=(datetime.date.today() + datetime.timedelta(days = -16)).strftime("%Y-%m-%d")

def download_data(date):
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:'+lg.error_code)
    print('login respond  error_msg:'+lg.error_msg)

    # 获取指定日期的指数、股票数据
    stock_rs = bs.query_all_stock(date)
    stock_df = stock_rs.get_data()
    data_df = pd.DataFrame()
    for code in stock_df["code"]:
        print("Downloading :" + code)
        k_rs = bs.query_history_k_data_plus(code, "date,code,open,high,low,close", date, date)
        data_df = data_df.append(k_rs.get_data())
    bs.logout()
    data_df.to_csv("D:\\bstock\\"+nday+"demo_assignDayData.csv", encoding="gbk", index=False)
    print(data_df)


if __name__ == '__main__':
    # 获取指定日期全部股票的日K线数据
    #download_data("2021-12-31")
    download_data(nday)