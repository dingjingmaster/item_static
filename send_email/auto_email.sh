#!/bin/bash
source ~/.bash_profile
export LANG=en_US.UTF-8

. shell_function

titles="$1"
dates="$2"
content="$3"
summary="$4"
email_send_to1="dingjing_ding@easou.cn"     #丁敬
email_send_to2="ruan_zheng@easou.cn"        # 儒安
email_send_to3="pm-r@easou.cn"
email_send_to4="mcgee_zhang@easou.cn"       # 世侠

to="${email_send_to1}, ${email_send_to2},${email_send_to3}, ${email_send_to4}"

email_head='<head><style type="text/css"> p{font-weight:bold; font-size: 18px} td{border: 0px solid; background-color: #c0c0c0} table, tr{border: 0px solid grey;} th{border: 0px solid; background-color: #a8a8a8} </style></head><body><div>'
email_buf=`cat ${content}`
email_tail="</div></body>"
message="${email_head} ${summary} <br><hr/> ${email_buf} ${email_tail}"

send_email "dingjing" "${to}" "${titles}" "${message}" "<br/>来源于BI: ${dates} 数据<hr>-- 结束 --<br/>"
