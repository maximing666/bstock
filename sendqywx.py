# -*- coding: UTF-8 –*-
import result_days_upcopy
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
sendresult= str(result_days_upcopy.fetch())
#t=['sh.600766', 'sh.603768', 'sh.688196', 'sh.688381', 'sh.688557', 'sh.688622', 'sz.001259', 'sz.002987'] 
#sendresult=str(t)
print(sendresult)
send_qyweixin(datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + " " + str(sendresult), webhook)

