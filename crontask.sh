#!/bin/bash
while true; do
    now=$(date +%H%M%S)
    echo "当前时间: $now"
    if [ $now -ge "213000" ]; then  
        cd /opt/conda/bstock/ && pip install -r requirements_copy.txt
        echo "开始下载数据"
        python download_dayk_one.py
        sleep 10
        echo "开始写入数据"
        python write_dayk_one.py
        echo "写入完成:"$(date +%H%M%S)
        #sleep 9000使得时间到第二天。
        sleep 9000
    else
        echo "等待1800秒"
        sleep 1800
    fi
done