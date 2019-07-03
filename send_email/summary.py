#!/usr/bin/env python2.7
# -*- coding=utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding("utf8")

summary_dict = {
    'easou_item': '宜搜'

}


if __name__ == '__main__':
    if len(sys.argv) != 3:
        exit(-1)
    summary_path = sys.argv[1]
    summary_result_path = sys.argv[2]

    # summary_path = '../summary.txt'
    # summary_result_path = '../summary_result.txt'

    dict1 = {}

    dict2_es_item = {}
    dict2_es_user = {}
    dict2_es_chapter = {}
    dict2_wj_item = {}
    dict2_wj_user = {}
    dict2_wj_chapter = {}
    out_str = ''

    with open(summary_path, 'r') as fr:
        for line in fr.readlines():
            line = line.strip('\n')
            arr = line.split('\t')
            if len(arr) == 6:
                dict1[arr[0]] = arr[1]
                dict1[arr[2]] = arr[3]
                dict1[arr[4]] = arr[5]
            elif len(arr) == 3:
                arr1 = arr[0].split('_')
                if arr[0] == 'easou_item':
                    dict2_es_item[arr[1]] = arr[2]
                elif arr[0] == 'easou_user':
                    dict2_es_user[arr[1]] = arr[2]
                elif arr[0] == 'easou_chapter':
                    dict2_es_chapter[arr[1]] = arr[2]
                elif arr1[0] == 'weijuan_item':
                    dict2_wj_item[arr[1]] = arr[2]
                elif arr1[0] == 'weijuan_user':
                    dict2_wj_user[arr[1]] = arr[2]
                elif arr1[0] == 'weijuan_chapter':
                    dict2_wj_chapter[arr[1]] = arr[2]

    out_str += '' \
               + '<h4>APP阅读情况</h4>' \
               + '<table width="80%">' \
               + '<tr align="center">' \
               + '<th align="center">书籍量</th>' \
               + '<th align="center">用户量</th>' \
               + '<th align="center">章节量</th>' \
               + '</tr>'
    out_str += '<tr align="center">'\
               + '<td align="left">' + dict1['easou_item'] + '</td>'\
               + '<td align="left">' + dict1['easou_user'] + '</td>'\
               + '<td align="left">' + dict1['easou_chapter'] + '</td>'\
               + '</tr>'
    out_str += '<tr align="center">' \
               + '<td align="left">' + dict1['easou_item'] + '</td>' \
               + '<td align="left">' + dict1['easou_user'] + '</td>' \
               + '<td align="left">' + dict1['easou_chapter'] + '</td>' \
               + '</tr>'
    out_str += '</table><br/>'

    out_str += '' \
               + '<h4>宜搜小说(10001)阅读情况</h4>' \
               + '<table width="80%">' \
               + '<tr align="center">' \
               + '<th align="center">书籍量</th>' \
               + '<th align="center">用户量</th>' \
               + '<th align="center">章节量</th>' \
               + '</tr>'
    out_str += '<tr align="center">' \
               + '<td align="left">' + dict2_es_item['付费'] + '</td>' \
               + '<td align="left">' + dict2_es_user['付费'] + '</td>' \
               + '<td align="left">' + dict2_es_chapter['付费'] + '</td>' \
               + '</tr>'
    out_str += '<tr align="center">' \
               + '<td align="left">' + dict2_es_item['限免'] + '</td>' \
               + '<td align="left">' + dict2_es_user['限免'] + '</td>' \
               + '<td align="left">' + dict2_es_chapter['限免'] + '</td>' \
               + '</tr>'
    out_str += '<tr align="center">' \
               + '<td align="left">' + dict2_es_item['包月'] + '</td>' \
               + '<td align="left">' + dict2_es_user['包月'] + '</td>' \
               + '<td align="left">' + dict2_es_chapter['包月'] + '</td>' \
               + '</tr>'
    out_str += '<tr align="center">' \
               + '<td align="left">' + dict2_es_item['免费'] + '</td>' \
               + '<td align="left">' + dict2_es_user['免费'] + '</td>' \
               + '<td align="left">' + dict2_es_chapter['免费'] + '</td>' \
               + '</tr>'
    out_str += '<tr align="center">' \
               + '<td align="left">' + dict2_es_item['互联网'] + '</td>' \
               + '<td align="left">' + dict2_es_user['互联网'] + '</td>' \
               + '<td align="left">' + dict2_es_chapter['互联网'] + '</td>' \
               + '</tr>'

    out_str += '' \
               + '<h4>微卷(20001)阅读情况</h4>' \
               + '<table width="80%">' \
               + '<tr align="center">' \
               + '<th align="center">书籍量</th>' \
               + '<th align="center">用户量</th>' \
               + '<th align="center">章节量</th>' \
               + '</tr>'
    out_str += '<tr align="center">' \
               + '<td align="left">' + dict2_wj_item['付费'] + '</td>' \
               + '<td align="left">' + dict2_wj_user['付费'] + '</td>' \
               + '<td align="left">' + dict2_wj_chapter['付费'] + '</td>' \
               + '</tr>'
    out_str += '<tr align="center">' \
               + '<td align="left">' + dict2_wj_item['限免'] + '</td>' \
               + '<td align="left">' + dict2_wj_user['限免'] + '</td>' \
               + '<td align="left">' + dict2_wj_chapter['限免'] + '</td>' \
               + '</tr>'
    out_str += '<tr align="center">' \
               + '<td align="left">' + dict2_wj_item['包月'] + '</td>' \
               + '<td align="left">' + dict2_wj_user['包月'] + '</td>' \
               + '<td align="left">' + dict2_wj_chapter['包月'] + '</td>' \
               + '</tr>'
    out_str += '<tr align="center">' \
               + '<td align="left">' + dict2_wj_item['免费'] + '</td>' \
               + '<td align="left">' + dict2_wj_user['免费'] + '</td>' \
               + '<td align="left">' + dict2_wj_chapter['免费'] + '</td>' \
               + '</tr>'
    out_str += '<tr align="center">' \
               + '<td align="left">' + dict2_wj_item['互联网'] + '</td>' \
               + '<td align="left">' + dict2_wj_user['互联网'] + '</td>' \
               + '<td align="left">' + dict2_wj_chapter['互联网'] + '</td>' \
               + '</tr>'

    with open(summary_result_path, 'w') as fw:
        fw.write(out_str + '\n')

    exit(0)
