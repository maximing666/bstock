#!/bin/bash
while true; do
    now=$(date +%Y%m%d%H%M%S)
    echo "当前时间: $now"
    now_hms=$(date +%H%M%S)  #时分秒
    now_d=$(date +%d)        #日
    # 如果当日时间大于等于21:30:00，则执行下载数据
    if [[ "$now_hms" > "213000" ]] || [[ "$now_hms" == "213000" ]]; then 
        cd /opt/conda/bstock/ && pip install -r requirements_copy.txt
        echo "开始下载数据"
        python download_dayk_one.py
        sleep 10
        echo "开始写入数据"
        python write_dayk_one.py
        echo "写入完成:"$(date +%H%M%S)

        echo "开始执行result_days_up_one.py"
        python result_days_up_one.py
        echo "完成执行result_days_up_one.py"

        if [[ "$now_d" == "01" || "$now_d" == "15" ]]; then
            echo "开始执行growth.py"
            python growth.py
            echo "完成执行growth.py"
        fi

        #sleep 9000使得时间到第二天。
        sleep 9000
    else
        echo "等待1800秒"
        sleep 1800
    fi

done