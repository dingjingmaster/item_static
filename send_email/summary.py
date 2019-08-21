#!/usr/bin/env python2.7
# -*- coding=utf-8 -*-
import sys
import base64
from mysql import Mysql
import matplotlib.pyplot as plt
reload(sys)
sys.setdefaultencoding("utf8")


def read_pic(pth):
    tmp = ''
    with open(pth, 'rb') as fr:
        tmp = base64.b64decode(fr.read())
    return tmp


def check_dict(mdict, key):
    if not mdict.has_key(key):
        return '0'
    return mdict[key]


def plot_pic(x, y, labe):
    if None is x:
        return
    tmp = []
    for i in x:
        if y.has_key(i):
            tmp.append(y[i])
        else:
            tmp.append(0)
    plt.plot(x, tmp, label=labe)
    for a, b in zip(x, tmp):
        plt.text(a, b, b, ha='center', va='bottom', fontsize=9)
    pass


if __name__ == '__main__':
    if len(sys.argv) != 6:
        exit(-1)
    summary_path = sys.argv[1]
    easou_result_path = sys.argv[2]
    weijuan_result_path = sys.argv[3]
    start_time_int = sys.argv[4]
    end_time_int = sys.argv[5]

    ad_rank = 1
    cg_rank = 5

    easou_pic = ''
    weijuan_pic = ''
    easou_average_pic = ''
    weijuan_average_pic = ''

    dict1 = {}

    dict2_es_item = {}
    dict2_es_user = {}
    dict2_es_chapter = {}
    dict2_wj_item = {}
    dict2_wj_user = {}
    dict2_wj_chapter = {}

    dau = {}
    app_earn_value = {}

    with open(summary_path, 'r') as fr:
        for line in fr.readlines():
            line = line.strip()
            arr = line.split('\t')
            if len(arr) == 6:
                dict1[arr[0]] = arr[1].strip()
                dict1[arr[2]] = arr[3].strip()
                dict1[arr[4]] = arr[5].strip()
            elif len(arr) == 3:
                arr1 = arr[0].split('_')
                if arr[0] == 'easou_item':
                    dict2_es_item[arr[1]] = arr[2]
                elif arr[0] == 'easou_user':
                    dict2_es_user[arr[1]] = arr[2]
                elif arr[0] == 'easou_chapter':
                    dict2_es_chapter[arr[1]] = arr[2]
                elif arr[0] == 'weijuan_item':
                    dict2_wj_item[arr[1]] = arr[2]
                elif arr[0] == 'weijuan_user':
                    dict2_wj_user[arr[1]] = arr[2]
                elif arr[0] == 'weijuan_chapter':
                    dict2_wj_chapter[arr[1]] = arr[2]
            elif len(arr) == 2:
                dau[arr[0]] = int(arr[1])
    # 计算广告收益价值
    app_earn_value['easou_ad'] = int(check_dict(dict2_es_chapter, '免费(免费cp)')) +\
                                 int(check_dict(dict2_es_chapter, '限免'))+\
                                 int(check_dict(dict2_es_chapter, '互联网')) * ad_rank
    app_earn_value['weijuan_ad'] = int(check_dict(dict2_wj_chapter, '免费(免费cp)')) + \
                                 int(check_dict(dict2_wj_chapter, '限免')) + \
                                 int(check_dict(dict2_wj_chapter, '互联网')) * ad_rank

    # 计算付费收益价值
    app_earn_value['easou_cg'] = int(check_dict(dict2_es_chapter, '付费')) + \
                                 int(check_dict(dict2_es_chapter, '包月')) * cg_rank
    app_earn_value['weijuan_cg'] = int(check_dict(dict2_wj_chapter, '付费')) + \
                                   int(check_dict(dict2_wj_chapter, '包月')) * cg_rank

    easou_day_earn = app_earn_value['easou_ad'] + app_earn_value['easou_cg']
    easou_aver_earn = "%.3f" % (float(app_earn_value['easou_ad']
                                        + app_earn_value['easou_cg'])/int(check_dict(dau, 'easou_dau')))
    weijuan_day_earn = app_earn_value['weijuan_ad'] + app_earn_value['weijuan_cg']
    weijuan_aver_earn = "%.3f" % (float(app_earn_value['weijuan_ad']
                                      + app_earn_value['weijuan_cg']) / int(check_dict(dau, 'weijuan_dau')))

    # 保存今天数据 并 返回历史数据
    mq = Mysql('10.26.24.87', 3306, 'item_earn', 'root', '123456')
    time_arr = []
    easou_day_arr = {}
    easou_aver_arr ={}
    weijuan_day_arr = {}
    weijuan_aver_arr = {}
    if mq.connect():
        mq.save('easou', 'earn_sum', easou_day_earn, end_time_int)
        mq.save('easou', 'earn_aver', easou_aver_earn, end_time_int)
        mq.save('weijuan', 'earn_sum', weijuan_day_earn, end_time_int)
        mq.save('weijuan', 'warn_aver', weijuan_aver_earn, end_time_int)

        easou_day_arr = mq.get_time_range_value('easou', 'earn_sum', start_time_int, end_time_int)
        easou_aver_arr = mq.get_time_range_value('easou', 'earn_aver', start_time_int, end_time_int)
        weijuan_day_arr = mq.get_time_range_value('weijuan', 'earn_sum', start_time_int, end_time_int)
        weijuan_aver_arr = mq.get_time_range_value('weijuan', 'earn_aver', start_time_int, end_time_int)
    time_arr = mq.get_time_range()

    # 绘制 宜搜天价值量 图形
    plot_pic(time_arr, easou_day_arr, "easou's value")
    plt.xlabel('date')
    plt.ylabel('value')
    plt.legend()
    plt.savefig('./.pic.png')
    easou_pic = read_pic('./.pic.png')

    # 绘制微卷天价值图
    plot_pic(time_arr, weijuan_day_arr, "weijuan's value")
    plt.xlabel('date')
    plt.ylabel('value')
    plt.legend()
    plt.savefig('./.pic.png')
    weijuan_pic = read_pic('./.pic.png')

    # 宜搜 绘制平均价值图
    plot_pic(time_arr, easou_aver_arr, "easou's Per capita value")
    plt.xlabel('date')
    plt.ylabel('value')
    plt.legend()
    plt.savefig('./.pic.png')
    easou_average_pic = read_pic('./.pic.png')

    plot_pic(time_arr, weijuan_aver_arr, "weijuan's Per capita value")
    plt.xlabel('date')
    plt.ylabel('value')
    plt.legend()
    plt.savefig('./.pic.png')
    weijuan_average_pic = read_pic('./.pic.png')

    easou_str = '' \
                '<img src="data:image/png;base64,' + easou_pic + '">' \
                '<img src="data:image/png;base64,' + easou_average_pic + '">' \
                '<br/>'\
                '<h4>APP阅读情况</h4>\n' \
                '<table width="80%">\n' \
                '<tr align="center">\n' \
                '       <th align="center">APP</th>\n' \
                '       <th align="center">书籍量</th>\n' \
                '       <th align="center">用户量</th>\n' \
                '       <th align="center">章节量</th>\n' \
                '       <th align="center">总收益价值</th>\n' \
                '       <th align="center">人均收益价值</th>\n' \
                '</tr>\n' \
                '<tr align="center">\n'\
                '       <td align="left">宜搜小说</td>\n' \
                '       <td align="left">' + dict1['easou_item'] + '</td>\n'\
                '       <td align="left">' + dict1['easou_user'] + '</td>\n'\
                '       <td align="left">' + dict1['easou_chapter'] + '</td>\n'\
                '       <td align="left">' + str(easou_day_earn) + '</td>\n'\
                '       <td align="left">' + easou_aver_earn + '</td>\n'\
                '</tr>\n' \
                '</table>\n' \
                ''\
                '<h4>宜搜小说(10001)阅读情况</h4>\n' \
                '<table width="80%">\n' \
                '   <tr align="center">\n' \
                '       <th align="center">阅读类型</th>\n' \
                '       <th align="center">书籍量</th>\n' \
                '       <th align="center">用户量</th>\n' \
                '       <th align="center">章节量</th>\n' \
                '   </tr>\n' \
                '   <tr align="center">\n' \
                '       <td align="left">付费</td>\n' \
                '       <td align="left">' + check_dict(dict2_es_item, '付费') + '</td>\n' \
                '       <td align="left">' + check_dict(dict2_es_user, '付费') + '</td>\n' \
                '       <td align="left">' + check_dict(dict2_es_chapter, '付费') + '</td>\n' \
                '   </tr>\n' \
                '   <tr align="center">\n' \
                '       <td align="left">限免</td>\n' \
                '       <td align="left">' + check_dict(dict2_es_item, '限免') + '</td>\n' \
                '       <td align="left">' + check_dict(dict2_es_user, '限免') + '</td>\n' \
                '       <td align="left">' + check_dict(dict2_es_chapter, '限免') + '</td>\n' \
                '   </tr>\n' \
                '   <tr align="center">\n' \
                '       <td align="left">包月</td>\n' \
                '       <td align="left">' + check_dict(dict2_es_item, '包月') + '</td>\n' \
                '       <td align="left">' + check_dict(dict2_es_user, '包月') + '</td>\n' \
                '       <td align="left">' + check_dict(dict2_es_chapter, '包月') + '</td>\n' \
                '   </tr>\n' \
                '   <tr align="center">\n' \
                '       <td align="left">免费(免费cp)</td>\n' \
                '       <td align="left">' + check_dict(dict2_es_item, '免费(免费cp)') + '</td>\n' \
                '       <td align="left">' + check_dict(dict2_es_user, '免费(免费cp)') + '</td>\n' \
                '       <td align="left">' + check_dict(dict2_es_chapter, '免费(免费cp)') + '</td>\n' \
                '   </tr>\n' \
                '   <tr align="center">\n' \
                '       <td align="left">免费(包月书)</td>\n' \
                '       <td align="left">' + check_dict(dict2_es_item, '免费(包月书)') + '</td>\n' \
                '       <td align="left">' + check_dict(dict2_es_user, '免费(包月书)') + '</td>\n' \
                '       <td align="left">' + check_dict(dict2_es_chapter, '免费(包月书)') + '</td>\n' \
                '   </tr>\n' \
                '   <tr align="center">\n' \
                '       <td align="left">免费(按章付费)</td>\n' \
                '       <td align="left">' + check_dict(dict2_es_item, '免费(按章计费)') + '</td>\n' \
                '       <td align="left">' + check_dict(dict2_es_user, '免费(按章计费)') + '</td>\n' \
                '       <td align="left">' + check_dict(dict2_es_chapter, '免费(按章计费)') + '</td>\n' \
                '   </tr>\n' \
                '   <tr align="center">\n' \
                '       <td align="left">互联网</td>\n' \
                '       <td align="left">' + check_dict(dict2_es_item, '互联网') + '</td>\n' \
                '       <td align="left">' + check_dict(dict2_es_user, '互联网') + '</td>\n' \
                '       <td align="left">' + check_dict(dict2_es_chapter, '互联网') + '</td>\n' \
                '   </tr>\n' \
                '</table>\n'

    weijuan_str = '' \
                  '<img src="data:image/png;base64,' + weijuan_pic + '">' \
                  '<img src="data:image/png;base64,' + weijuan_average_pic + '">' \
                  '<br/>' \
                  '<h4>APP阅读情况</h4>\n' \
                  '<table width="80%">\n' \
                  ' <tr align="center">\n' \
                  '     <th align="center">APP</th>\n' \
                  '     <th align="center">书籍量</th>\n' \
                  '     <th align="center">用户量</th>\n' \
                  '     <th align="center">章节量</th>\n' \
                  '     <th align="center">总收益价值(天)</th>\n' \
                  '     <th align="center">人均收益价值</th>\n' \
                  ' </tr>\n' \
                  ' <tr align="center">\n'\
                  '     <td align="left">微卷</td>\n' \
                  '     <td align="left">' + dict1['weijuan_item'] + '</td>\n' \
                  '     <td align="left">' + dict1['weijuan_user'] + '</td>\n' \
                  '     <td align="left">' + dict1['weijuan_chapter'] + '</td>\n' \
                  '     <td align="left">' + str(weijuan_day_earn) + '</td>\n'\
                  '     <td align="left">' + weijuan_aver_earn + '</td>\n'\
                  ' </tr>\n' \
                  ' <tr align="center">\n' \
                  '     <td align="left">漫画</td>\n' \
                  '     <td align="left">' + dict1['manhua_item'] + '</td>\n' \
                  '     <td align="left">' + dict1['manhua_user'] + '</td>\n' \
                  '     <td align="left">' + dict1['manhua_chapter'] + '</td>\n' \
                  '     <td align="left">' + '暂无统计' + '</td>\n' \
                  '     <td align="left">' + '暂无统计' + '</td>\n' \
                  ' </tr>\n' \
                  '</table>\n'\
                  '' \
                  '<h4>微卷(20001)阅读情况</h4>\n' \
                  '<table width="80%">\n' \
                  ' <tr align="center">\n' \
                  '     <th align="center">阅读类型</th>\n' \
                  '     <th align="center">书籍量</th>\n' \
                  '     <th align="center">用户量</th>\n' \
                  '     <th align="center">章节量</th>\n' \
                  ' </tr>\n' \
                  ' <tr align="center">\n' \
                  '     <td align="left">付费</td>\n' \
                  '     <td align="left">' + check_dict(dict2_wj_item, '付费') + '</td>\n' \
                  '     <td align="left">' + check_dict(dict2_wj_user, '付费') + '</td>\n' \
                  '     <td align="left">' + check_dict(dict2_wj_chapter, '付费') + '</td>\n' \
                  ' </tr>\n' \
                  ' <tr align="center">\n' \
                  '     <td align="left">限免</td>\n' \
                  '     <td align="left">' + check_dict(dict2_wj_item, '限免') + '</td>\n' \
                  '     <td align="left">' + check_dict(dict2_wj_user, '限免') + '</td>\n' \
                  '     <td align="left">' + check_dict(dict2_wj_chapter, '限免') + '</td>\n' \
                  ' </tr>\n' \
                  ' <tr align="center">\n' \
                  '     <td align="left">包月</td>\n' \
                  '     <td align="left">' + check_dict(dict2_wj_item, '包月') + '</td>\n' \
                  '     <td align="left">' + check_dict(dict2_wj_user, '包月') + '</td>\n' \
                  '     <td align="left">' + check_dict(dict2_wj_chapter, '包月') + '</td>\n' \
                  ' </tr>\n' \
                  ' <tr align="center">\n' \
                  '     <td align="left">免费(免费cp)</td>\n' \
                  '     <td align="left">' + check_dict(dict2_wj_item, '免费(免费cp)') + '</td>\n' \
                  '     <td align="left">' + check_dict(dict2_wj_user, '免费(免费cp)') + '</td>\n' \
                  '     <td align="left">' + check_dict(dict2_wj_chapter, '免费(免费cp)') + '</td>\n' \
                  ' </tr>\n' \
                  ' <tr align="center">\n' \
                  '     <td align="left">免费(免费包月书)</td>\n' \
                  '     <td align="left">' + check_dict(dict2_wj_item, '免费(包月书)') + '</td>\n' \
                  '     <td align="left">' + check_dict(dict2_wj_user, '免费(包月书)') + '</td>\n' \
                  '     <td align="left">' + check_dict(dict2_wj_chapter, '免费(包月书)') + '</td>\n' \
                  ' </tr>\n' \
                  ' <tr align="center">\n' \
                  '     <td align="left">免费(按章付费)</td>\n' \
                  '     <td align="left"> ' + check_dict(dict2_wj_item, '免费(按章计费)') + '</td >\n' \
                  '     <td align="left"> ' + check_dict(dict2_wj_user, '免费(按章计费)') + '</td>\n' \
                  '     <td align="left"> ' + check_dict(dict2_wj_chapter, '免费(按章计费)') + '</td>\n' \
                  ' </tr>\n' \
                  ' <tr align="center">\n' \
                  '     <td align="left">互联网</td>\n' \
                  '     <td align="left">' + check_dict(dict2_wj_item, '互联网') + '</td>\n' \
                  '     <td align="left">' + check_dict(dict2_wj_user, '互联网') + '</td>\n' \
                  '     <td align="left">' + check_dict(dict2_wj_chapter, '互联网') + '</td>\n' \
                  ' </tr>\n' \
                  '</table>\n'

    with open(easou_result_path, 'w') as fw:
        fw.write(easou_str + '\n')

    with open(weijuan_result_path, 'w') as fw:
        fw.write(weijuan_str + '\n')

    exit(0)
