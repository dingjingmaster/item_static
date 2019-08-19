#!/usr/bin/env python2.7
# -*- coding=utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding("utf8")


def check_dict(mdict, key):
    if not mdict.has_key(key):
        return '0'
    return mdict[key].strip()


if __name__ == '__main__':
    if len(sys.argv) != 4:
        exit(-1)
    summary_path = sys.argv[1]
    easou_result_path = sys.argv[2]
    weijuan_result_path = sys.argv[3]

    ad_rank = 1
    cg_rank = 5

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

    easou_str = '' \
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
