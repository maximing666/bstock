# -*- coding: UTF-8 –*-
import result_choice
import requests

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
sendresult= result_choice.fetch()
print(sendresult)
send_qyweixin(sendresult, webhook)

