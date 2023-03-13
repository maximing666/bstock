# -*- coding: UTF-8 –*-
import baostock as bs
import pandas as pd
import datetime
import time
import configparser
# import t3


def download_data(day):
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:'+lg.error_code)
    print('login respond  error_msg:'+lg.error_msg)

    # 获取指定日期的指数、股票数据
    stock_rs = bs.query_all_stock(day)
    stock_df = stock_rs.get_data()
    l = []
    for i in stock_df["code"]:
        print(i)
    for code in stock_df["code"]:
        print(day + " Downloading :" + code)
        #frequency：数据类型，默认为d，日k线；d=日k线、w=周、m=月、5=5分钟、15=15分钟、30=30分钟、60=60分钟k线数据，不区分大小写；指数没有分钟线数据；周线每周最后一个交易日才可以获取，月线每月最后一个交易日才可以获取
        k_rs = bs.query_history_k_data_plus(code, "date,code,open,high,low,close,volume,amount,turn,tradestatus,pctChg,peTTM", start_date=day, end_date=day,frequency="d", adjustflag="3")
        if (k_rs.error_code == '0'):
            # print("===",k_rs.get_row_data(),"---",k_rs.error_code,"++++",type(k_rs.get_row_data()))
            l.append(k_rs.get_row_data())   
            
      
    bs.logout()
    #data_df.to_csv("D:\\bstock\\download\\dayk\\"+nday+"demo_assignDayData.csv", encoding="gbk", index=False)
    
    result = pd.DataFrame(l, columns=k_rs.fields) 
    result.to_csv(downloadpath + day + "demo_assignDayData.csv", encoding="gbk", index=False)
    # print(result)


if __name__=='__main__':
    # t3.Logger()
    #开始时间
    starttime = time.time()

    #生成configparser对象
    config = configparser.ConfigParser()
    #读取配置文件
    # conffilename = r'E:\github\bstock\config\config.ini'
    conffilename = r'.\\config\\config.ini'
    config.read(conffilename, encoding='utf-8')
    #获取配置文件变量值
    startday = int(config.get('dayk', 'startday'))
    endday = int(config.get('dayk', 'endday'))
    downloadpath = config.get('dayk', 'downloadpath')
    #获取从startday天前到endday天前的数据。startday=-1表示昨天，startday=-2表示前天
    # startday = -25
    # endday = -21
    while (startday <= endday):
        nday = (datetime.date.today() + datetime.timedelta(days = startday)).strftime("%Y-%m-%d")
        print(nday)
        try:
            # 获取指定日期全部股票的日K线数据
            download_data(nday)
        except:
            print(nday, "该日期无数据。")
        startday = startday + 1
    #结束时间
    endtime = time.time()
    #耗费时长(秒)
    usetime = endtime - starttime
    print("用时：", usetime/60, "分") 