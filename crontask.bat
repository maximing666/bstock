::获取当前时间
set d=%date:~0,10%
set t=%time:~0,8%
echo %d% %t%
::开启网卡
netsh interface set interface "WLAN" enable
ping -n 5 www.baidu.com
::执行程序
::cd /d D:\github\bstock && conda activate bstock && python daykcopy.py && python writedayk.py && python sendqywx.py
cd /d D:\github\bstock && conda activate bstock && python sendqywx.py
#cd /d D:\github\bstock && conda activate bstock  && python sendqywx.py