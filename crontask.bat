::每日21:30执行。
::获取当前时间
set d=%date:~0,10%
set t=%time:~0,8%
echo %d% %t%
::开启网卡
netsh interface set interface "WLAN" enable
ping -n 5 www.baidu.com
::执行程序
cd /d D:\github\bstock && conda activate bstock && python download_dayk_one.py && python write_dayk_one.py && python sendqywx.py && python write_dayk_avg_three.py
::
::cd /d D:\github\bstock && conda activate bstock && python sendqywx.py
::关闭网卡
ping -n 5 www.baidu.com
::netsh interface set interface "WLAN" disable
::pause
@cmd /k