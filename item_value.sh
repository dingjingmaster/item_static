#!/usr/bin/env bash
source ~/.bash_profile
source ~/.bashrc
source shell_function

days=30
year=`date -d "-1 day" +%Y`
today=`date -d "-1 day" +%Y-%m-%d`
workDir=$(cd $(dirname $0); pwd)

sparkRun="spark-submit --total-executor-cores=30 --executor-memory=20g "
itemInfoPath=`hadoop fs -ls "hdfs://10.26.26.145:8020/rs/iteminfo/${year}-*/item_*" | tail -n 1 | awk -F' ' '{print $8}'`
biReadLog="hdfs://10.26.29.210:8020/user/hive/warehouse/event_info.db/b_read_chapter/ds="
itemValuePath="hdfs://10.26.26.145:8020/rs/dingjing/item_value/${today}/"

# 检查是否可以开始执行
for((i=0;i<2;++i))
do
    hdfs_exist "${itemValuePath}"
    if [ $? -ne 0 ]
    then
        cd ${workDir}
        hadoop fs -rmr "${itemValuePath}"
        ${sparkRun} --class ItemValue ./jar/*.jar "${itemInfoPath}" "${biReadLog}" "${today}" "${days}" "${itemValuePath}"
        sleep 3
        continue
    fi
    break
done

# 结果注入 hbase

