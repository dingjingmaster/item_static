#!/bin/bash
source ~/.bash_profile
source ~/.bashrc
. shell_function

workDir=$(cd $(dirname $0); pwd)
today=`date -d "-1 day" +%Y-%m-%d`
year=`date -d "-1 day" +%Y`
#today="2018-04-10"

itemInfoPath=`hadoop fs -ls "hdfs://10.26.26.145:8020/rs/iteminfo/${year}-*/item_*" | tail -n 1 | awk -F' ' '{print $8}'`
sparkRun="spark-submit --total-executor-cores=30 --executor-memory=20g "
biReadLog="hdfs://10.26.29.210:8020/user/hive/warehouse/event_info.db/b_read_chapter/ds=${today}/*"
itemChapterReadPath="hdfs://10.26.26.145:8020/rs/dingjing/day_detail/${today}/"
#localBuyPath="data/item_buy.txt"
#localReadPath="data/item_read.txt"
#easouBuyResultPath="data/buy_easou_result.txt"
#weijuanBuyResultPath="data/buy_weijuan_result.txt"
#easouReadResultPath="data/read_easou_result.txt"
#weijuanReadResultPath="data/read_weijuan_result.txt"

###################     开始执行      ###########################
for((i=0;i<20;++i))
do
    # 解析日志 阅读
    hdfs_exist "${itemChapterReadPath/summary/}"
    if [ $? -ne 0 ]
    then
        cd ${workDir}
        hadoop fs -rmr "${itemChapterReadPath}"
        ${sparkRun} --class ItemRead ./jar/*.jar "${itemInfoPath}" "${biReadLog}" "${itemChapterReadPath}"
        sleep 3
#        continue
    fi
#    # 解析日志 阅读
#    hdfs_exist "${itemChapterPurchase}"
#    if [ $? -ne 0 ]
#    then
#        cd ${workDir}
#        hadoop fs -rmr "${itemChapterPurchase}"
#        hadoop fs -rmr "${itemChapterRead}"
#        sleep 3
#        continue
#    fi
    break
done

# 统计邮件
#cd ${workDir}
#rm -fr data && mkdir data
#hadoop fs -cat "${itemChapterPurchase}/*" > ${localBuyPath}
#hadoop fs -cat "${itemChapterRead}/*" > ${localReadPath}
#
#python send_email/generate_buy_email.py "${localBuyPath}" "${easouBuyResultPath}" "easou"
#python send_email/generate_buy_email.py "${localBuyPath}" "${weijuanBuyResultPath}" "weijuan"
#
#python send_email/generate_read_email.py "${localReadPath}" "${easouReadResultPath}" "easou"
#python send_email/generate_read_email.py "${localReadPath}" "${weijuanReadResultPath}" "weijuan"

#if true
#then
#file_empty "${easouReadResultPath}"
#if [ $? -eq 0 ]
#then
#    summary='<br>
#    <li>不是从书架进入的阅读用户不做统计</li>
#    <li>书籍量: 天阅读的书籍总数</li>
#    <li>阅读量: 每本书籍的天阅读人数之和</li>
#    <li>阅读章节数: 每本书籍、每人的天阅读章节数之和</li>
#    <li>关于屏蔽与否：app中所有数据流都屏蔽的书籍才作为“屏蔽书籍”，否则算作“非屏蔽书籍”</li>
#    <li>关于占比：假如一本书，同时属于两个统计维度，那么在这两个统计维度中我都会统计这本书</li>
#    '
#    sh send_email/auto_email.sh "宜搜小说(10001)天阅读量统计" "${today}" "${easouReadResultPath}" "${summary}"
#    sh send_email/auto_email.sh "微卷(20001)天阅读量统计" "${today}" "${weijuanReadResultPath}" "${summary}"
#
#    sh send_email/auto_email.sh "宜搜小说(10001)天付费章节阅读量统计" "${today}" "${easouBuyResultPath}" "${summary}"
#    sh send_email/auto_email.sh "微卷(20001)天付费章节阅读量统计" "${today}" "${weijuanBuyResultPath}" "${summary}"
#fi
#fi
exit 0
