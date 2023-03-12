---
title: "文章标题"
output:
    word_document:
        path: xxx.docx
        toc: true
        toc_depth: 6
        number_sections: true
---
## 1. 数据结构
##### 1.1 数据表

mysql root 123456;webuser 123456
CREATE TABLE `bstock`.`Untitled`  (
  `tdate` date NOT NULL COMMENT '交易日期',
  `code` varchar(255) NOT NULL COMMENT '股票代码',
  `open` double(255, 4) NOT NULL,
  `high` double(255, 4) NOT NULL,1. 
mysql root 123456;webuser 123456
CREATE TABLE `bstock`.`Untitled`  (
  `tdate` date NOT NULL COMMENT '交易日期',
  `code` varchar(255) NOT NULL COMMENT '股票代码',
  `open` double(255, 4) NOT NULL,
  `high` double(255, 4) NOT NULL,
  `low` double(255, 4) NOT NULL,
  `close` double(255, 4) NOT NULL,
  PRIMARY KEY (`tdate`)
);

### 2. dayk_one.py 获取某天前到某天前的数据。
| 参数名称 |参数描述 |算法说明 |
| --- | --- | --- |
| date |交易所行情日期 | |
| code |	证券代码 |	 |
| open |	开盘价 |	 |
| high |	最高价 |	 |
| low |	最低价 |	 |
| close |	收盘价 |	 |
| preclose |	前收盘价 |	见表格下方详细说明 |
| volume |	成交量（累计  单位：股） |	|
| amount |	成交额（单位：人民币元） |	 |
| adjustflag |	复权状态 ( 1：后复权， 2：前复权，3：不复权）||	
| turn |	换手率 |	[指定交易日的成交量 (股)/指定交易日的股票的流通股总股数(股)]*100%|
| tradestatus |	交易状态 ( 1：正常交易 0：停牌）||	
| pctChg |	涨跌幅（百分比） |	日涨跌幅 =[(指定交易日的收盘价-指定交易日前收盘价)/指定交易日前收盘价]*100%|
| peTTM |	滚动市盈率 |	(指定交易日的股票收盘价 /指定交易日的每股盈余TTM)=(指定交易日的股票收盘价*截至当日公司总股本)/归属母公司股东净利润TTM|
| pbMRQ |	市净率 |	(指定交易日的股票收盘价/指定交易日的每股净资产)=总市值/(最近披露的归属母公司股东的权益-其他权益工具) |
| psTTM |	滚动市销率 |	(指定交易日的股票收盘价/指定交易日的每股销售额)=(指定交易日的股票收盘价*截至当日公司总股本)/营业总收入TTM |
|pcfNcfTTM |	滚动市现率 |	(指定交易日的股票收盘价/指定交易日的每股现金流TTM)=(指定交易日的股票收盘价*截至当日公司总股本)/现金以及现金等价物净增加额TTM|
| isST |	是否ST股，1是，0否 |	 |
3. writedb.py 读取excel后，再写入mysql数据库。

4. bi.py读取mysql数据绘制图形。

5. dupont.py 杜邦指标。
dupontNitogr  净利润/营业总收入=净利率，反映企业销售获利率。
dupontROE	净资产收益率，说明企业利用净资产赚钱的能力越强，越高说明越暴利。
dupontTaxBurden	净利润/利润总额，反映企业税负水平，该比值高则税负较低。净利润/利润总额=1-所得税/利润总额

6. growth.py 成长能力，同比数据。

7. codeinfo.py 基本资料

8.result_choice.py 收益高查询结果。
  result_days_up.py 近期连涨查询结果。
  result_5days_up.py 近期5日线连涨查询结果。
    

9. sendqywx.py 发送结果到企微。

10.main.py 主程序。


原则：
1. 杜邦指数：dupontTaxBurden税负低>0，净利率高，净资产收益率高的。
select dupont.code,codeinfo.codename 股票名称,year 年份,`quarter` 季度,pubdate 发布日期,dupontroe 净资产收益率,dupontnitogr 净利率 from dupont,codeinfo where dupont.code = codeinfo.code and year='2022' and quarter='3' and duponttaxburden > 0 and dupontroe > 0.3 and dupontnitogr> 0.2 and dupont.code not like 'sh.688%'  ORDER BY dupontnitogr desc  limit 20; 
  `low` double(255, 4) NOT NULL,
  `close` double(255, 4) NOT NULL,
  PRIMARY KEY (`tdate`)
);

2. dayk_one.py 获取某天前到某天前的数据。


3. writedb.py 读取excel后，再写入mysql数据库。

4. bi.py读取mysql数据绘制图形。

5. dupont.py 杜邦指标。
dupontNitogr  净利润/营业总收入=净利率，反映企业销售获利率。
dupontROE	净资产收益率，说明企业利用净资产赚钱的能力越强，越高说明越暴利。
dupontTaxBurden	净利润/利润总额，反映企业税负水平，该比值高则税负较低。净利润/利润总额=1-所得税/利润总额

6. growth.py 成长能力，同比数据。

7. codeinfo.py 基本资料

8.result_choice.py 收益高查询结果。
  result_days_up.py 近期连涨查询结果。
  result_5days_up.py 近期5日线连涨查询结果。
    

9. sendqywx.py 发送结果到企微。

10.main.py 主程序。

