import time
import download_dayk_one, write_dayk_one

while True:
    print("开始下载数据")
    download_dayk_one()
    print("开始写入数据")
    write_dayk_one()
    print("等待10秒")
    time.sleep(10)