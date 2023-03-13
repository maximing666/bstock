# -*- coding: UTF-8 –*-
import result_days_up
import requests
import datetime
import t3

t3.Logger()
headers = {'Content-Type': 'text/plain'}
webhook = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ba5e976c-fad4-48d4-9c09-43d077d44cbf"

#每次调用方法传你需要发送的报警信息和对应的webhook地址即可
def send_qyweixin(s, webhook):
    data = {
        "msgtype": "text",
        "text": {
            "content": s,
        }
    }
    r = requests.post(url=webhook, headers=headers, json=data)
    print(r)
sendresult= str(result_days_up.put_viewrecommend())
#t = "[(sh.000116, 上证信用债100指数), (sh.603220, 中贝通信), (sz.000055, 方大集团), (sz.002521, 齐峰新材), (sz.002839, 张家港行), (sz.300286, 安科瑞), (sz.300445, 康斯特), (sz.300711, 广哈通信)]"
#sendresult=str(t)
sendresult = sendresult.replace('),',')\n')
print(sendresult)
#发微信消息
#send_qyweixin(datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + "\n " + sendresult, webhook)

