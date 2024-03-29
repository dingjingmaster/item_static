#!/bin/bash
source ~/.bash_profile
source ~/.bashrc
. shell_function

workDir=$(cd $(dirname $0); pwd)
today=`date -d "-1 day" +%Y-%m-%d`
year=`date -d "-1 day" +%Y`
thisday=`date -d "-1 day" +%Y%m%d`
d7ago=`date -d "-8 day" +%Y%m%d`
#today="2019-06-27"

itemInfoPath=`hadoop fs -ls "hdfs://10.26.26.145:8020/rs/iteminfo/${year}-*/item_*" | tail -n 1 | awk -F' ' '{print $8}'`
sparkRun="spark-submit --total-executor-cores=30 --executor-memory=20g "
biReadLog="hdfs://10.26.29.210:8020/user/hive/warehouse/event_info.db/b_read_chapter/ds=${today}/*"
itemChapterReadPath="hdfs://10.26.26.145:8020/rs/dingjing/day_detail/${today}/"
biVisitedPath="hdfs://10.26.29.210:8020/user/hive/warehouse/applog.db/distinct_activity_user/ds=${today}/*"
localSummaryPath="data/read_summary.txt"
localReadPath="data/read_info.txt"
easouSummaryResultPath="data/easou_summary.txt"
weijuanSummaryResultPath="data/weijuan_summary.txt"
easouResultPath="data/easou.txt"
weijuanResultPath="data/weijuan.txt"

###################     开始执行      ###########################
for((i=0;i<20;++i))
do
    # 解析日志 阅读
    hdfs_exist "${itemChapterReadPath}/summary/"
    if [ $? -ne 0 ]
    then
        cd ${workDir}
        hadoop fs -rmr "${itemChapterReadPath}"
        ${sparkRun} --class ItemRead ./jar/*.jar "${itemInfoPath}" "${biReadLog}" "${biVisitedPath}" "${itemChapterReadPath}"
        sleep 3
        continue
    fi
    break
done

# 统计邮件
cd ${workDir}
rm -fr data && mkdir data
hadoop fs -cat "${itemChapterReadPath}/summary/*" > ${localSummaryPath}
hadoop fs -cat "${itemChapterReadPath}/base_info/*" > ${localReadPath}
python send_email/summary.py "${localSummaryPath}" "${easouSummaryResultPath}" "${weijuanSummaryResultPath}" "${d7ago}" "${thisday}"
python send_email/generate_read_email.py "${localReadPath}" "${easouResultPath}" "10001"
python send_email/generate_read_email.py "${localReadPath}" "${weijuanResultPath}" "20001"

if true
then
file_empty "${easouResultPath}"
if [ $? -eq 0 ]
then
    summary1="
        <style>div p{font-weight:400;font-size:13px;}</style>
        <h3>说明</h3>
        <ul>
            <li>本邮件统计源数据来源于BI日志(${today})</li>
            <li>各统计维度的书籍量、用户量、章节量都是在该维度内去过重的</li>
            <li>关于付费、免费、限免、包月、互联网维度的统计粒度为章节</li>
            <li>
                <div>
                    <h4>阅读类型解释</h4>
                    <p>&nbsp;&nbsp;付费：阅读按章付费书籍的付费章节</p>
                    <p>&nbsp;&nbsp;免费(免费cp)：阅读免费CP书籍</p>
                    <p>&nbsp;&nbsp;免费(免费包月书)：非包月用户阅读包月书免费章节</p>
                    <p>&nbsp;&nbsp;免费(按章付费)：阅读按章付费免费章节部分</p>
                    <p>&nbsp;&nbsp;包月：包月用户读包月书</p>
                    <p>&nbsp;&nbsp;限免：阅读限免书籍</p>
                    <p>&nbsp;&nbsp;互联网：阅读互联网书籍</p>
                </div>
            </li>
            <li>
                <div>
                    <h4>统计指标解释</h4>
                    <p>&nbsp;&nbsp;书籍量：对应阅读类型涉及到的书籍量</p>
                    <p>&nbsp;&nbsp;用户量：对应阅读类型涉及到的用户量</p>
                    <p>&nbsp;&nbsp;章节量：对应阅读类型涉及到的阅读章节量</p>
                    <p>&nbsp;&nbsp;用户地区(书籍)：对应书籍被这些地区用户阅读</p>
                    <p>&nbsp;&nbsp;阅读量(书籍)：阅读的用户数</p>
                    <p>&nbsp;&nbsp;阅读章节量(书籍)：(书籍)被阅读的章节量</p>
                </div>
            </li>
        </ul><hr/>\n"
    summary="${summary1}\n$(cat ${easouSummaryResultPath})"
    sh send_email/auto_email.sh "宜搜小说(10001)天阅读量统计" "${today}" "${easouResultPath}" "${summary}"
    summary="${summary1}\n$(cat ${weijuanSummaryResultPath})"
    sh send_email/auto_email.sh "微卷(20001)天阅读量统计" "${today}" "${weijuanResultPath}" "${summary}"
fi
fi
exit 0
