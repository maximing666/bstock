import baostock as bs
import pandas as pd
import datetime
import time


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
        k_rs = bs.query_history_k_data_plus(code, "date,code,open,high,low,close,volume,amount,turn,tradestatus,pctChg,peTTM", date, date)
        data_df = data_df.append(k_rs.get_data())
    bs.logout()
    data_df.to_csv("D:\\bstock\\download\\dayk\\"+nday+"demo_assignDayData.csv", encoding="gbk", index=False)
    print(data_df)


if __name__ == '__main__':
    #开始时间
    starttime = time.time()
    
    #获取从startday天前到endday天前的数据。startday=-1表示昨天，startday=-2表示前天
    startday = 0
    endday = 0
    while (startday <= endday):
        nday = (datetime.date.today() + datetime.timedelta(days = startday)).strftime("%Y-%m-%d")
        print(nday)
        try:
            # 获取指定日期全部股票的日K线数据
            #download_data("2022-09-06")
            download_data(nday)
        except:
            print(nday, "该日期无数据。")
        startday = startday + 1
    #结束时间
    endtime = time.time()
    #耗费时长(秒)
    usetime = endtime - starttime
    print("用时：", usetime/60, "分") 