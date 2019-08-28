#!/usr/bin/env bash
source ~/.bash_profile
source ~/.bashrc
source shell_function

workDir=$(cd $(dirname $0); pwd)
today=`date -d "-1 day" +%Y-%m-%d`
days=30

sparkRun="spark-submit --total-executor-cores=30 --executor-memory=20g "
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
        ${sparkRun} --class ItemValue ./jar/*.jar "${biReadLog}" "${today}" "${days}" "${itemValuePath}"
        sleep 3
        continue
    fi
    break
done

# 结果注入 hbase

