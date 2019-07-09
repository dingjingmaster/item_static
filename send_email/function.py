#!/usr/bin/env python2.7
# -*- coding=utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding("utf8")


# 解析获取的hadoop信息
def read_data(log_path, app):
    ml = []
    fr = open(log_path, "r")
    """
        gid{]app{]name{]author{]cp{]read_type{]userlevel \t uid|sort{]...
    """
    for line in fr.readlines():
        line = line.strip()
        arr = line.split('\t')
        if len(arr) < 2:
            print 'error line' + line
            continue
        book_info = arr[0].split('{]')
        user_info = arr[1]
        if app != book_info[1]:
            continue
        ml.append((book_info[0], book_info[1], book_info[2], book_info[3],
                   book_info[4], book_info[5], book_info[6], user_info))
    return ml


# 各个类别分段统计
def category_analysis_list(log_list, category):
    top = []
    ml = []
    md = {}
    id = {}

    bt_0_10b = 0
    bt_10_100b = 0
    bt_100_1kb = 0
    bt_1k_10kb = 0
    gt_10kb = 0

    bt_0_10u = 0
    bt_10_100u = 0
    bt_100_1ku = 0
    bt_1k_10ku = 0
    gt_10ku = 0

    bt_0_10c = 0
    bt_10_100c = 0
    bt_100_1kc = 0
    bt_1k_10kc = 0
    gt_10kc = 0

    all_b = 0
    all_u = 0
    all_c = 0

    for i in log_list:
        gid, app, name, author, cp, type, level, user_info = i
        id[gid] = (name, author, cp, level)
        if category != type:
            continue
        arr = user_info.split('{]')
        for k in arr:
            arr1 = k.split('|')
            if md.has_key(gid):
                user, chapter = md[gid]
                user[arr1[0]] = True
                chapter[k] = True
            else:
                user, chapter = {arr1[0]: True}, {k: True}
                md[gid] = (user, chapter)
    for gid, iv in md.items():
        u = len(iv[0])
        c = len(iv[1])
        all_b += 1
        all_u += u
        all_c += c
        info = id[gid]
        top.append((gid, info[0], info[1], info[2], info[3], u, c))
        if (u > 0) and (u <= 10):
            bt_0_10b += 1
            bt_0_10u += u
            bt_0_10c += c
        elif (u > 10) and (u <= 100):
            bt_10_100b += 1
            bt_10_100u += u
            bt_10_100c += c
        elif (u > 100) and (u <= 1000):
            bt_100_1kb += 1
            bt_100_1ku += u
            bt_100_1kc += c
        elif (u > 1000) and (u <= 10000):
            bt_1k_10kb += 1
            bt_1k_10ku += u
            bt_1k_10kc += c
        else:
            gt_10kb += 1
            gt_10ku += u
            gt_10kc += c
    ml.append(("(0 ~ 10)",
               bt_0_10b, float(bt_0_10b) / all_b * 100,
               bt_0_10u, float(bt_0_10u) / all_u * 100,
               bt_0_10c, float(bt_0_10c) / all_c * 100))
    ml.append(("[10 ~ 100)",
               bt_10_100b, float(bt_10_100b) / all_b * 100,
               bt_10_100u, float(bt_10_100u) / all_u * 100,
               bt_10_100c, float(bt_10_100c) / all_c * 100))
    ml.append(("[100 ~ 1000)",
               bt_100_1kb, float(bt_100_1kb) / all_b * 100,
               bt_100_1ku, float(bt_100_1ku) / all_u * 100,
               bt_100_1kc, float(bt_100_1kc) / all_c * 100))
    ml.append(("[1000 ~ 10000)",
               bt_1k_10kb, float(bt_1k_10kb) / all_b * 100,
               bt_1k_10ku, float(bt_1k_10ku) / all_u * 100,
               bt_1k_10kc, float(bt_1k_10kc) / all_c * 100))
    ml.append(("[10000 ~ ∞)",
               gt_10kb, float(gt_10kb) / all_b * 100,
               gt_10ku, float(gt_10ku) / all_u * 100,
               gt_10kc, float(gt_10kc) / all_c * 100))
    return top, ml


def cp_top(log_list):
    out_list = []
    cp_list = []
    all_book = 0
    all_user = 0
    all_chapter = 0
    oth_book = 0
    oth_user = 0
    oth_chap = 0
    cp_dict = {}
    for i in log_list:
        gid, app, name, author, cp, type, level, user_info = i
        arr = user_info.split('{]')
        for k in arr:
            arr1 = k.split('|')
            if cp_dict.has_key(cp):
                book, user, chapter = cp_dict[cp]
                book[gid] = True
                user[arr1[0]] = True
                chapter[k] = True
                cp_dict[cp] = (book, user, chapter)
            else:
                book, user, chapter = {gid: True}, {arr1[0]: True}, {k: True}
                cp_dict[cp] = (book, user, chapter)
    for cp, iv in cp_dict.items():
        b = len(iv[0])
        u = len(iv[1])
        c = len(iv[2])
        all_book += b
        all_user += u
        all_chapter += c
        cp_list.append((cp, b, u, c))
    # 按阅读人数排序
    cp_list.sort(key=lambda x: int(x[2]), reverse=True)
    index = 0
    for i in cp_list:
        index += 1
        if index < 10:
            out_list.append((i[0], i[1], float(i[1]) / all_book * 100,
                             i[2], float(i[2]) / all_user * 100,
                             i[3], float(i[3]) / all_chapter * 100))
        else:
            oth_book += i[1]
            oth_user += i[2]
            oth_chap += i[3]
    out_list.append(('其它cp', oth_book, float(oth_book) / all_book * 100,
                     oth_user, float(oth_user) / all_user * 100,
                     oth_chap, float(oth_chap) / all_chapter * 100))
    return out_list


def print_cp_top(mlist, title, titleTup):
    out_buf = ""
    out_buf += '<h4>' + title + '</h4>\n'
    out_buf += '<table width="80%">\n'
    out_buf += '<tr align="center">'
    for i in titleTup:
        out_buf += '<th align="center">' + i + '</th>\n'
    out_buf += '</tr>\n'
    rank = 1
    for i in mlist:
        out_buf += '<tr align="center">'
        for j in range(len(i)):
            if j >= len(i) - 1:
                break
            if j == 0:
                out_buf += '<td align="left">' + str(rank) + '</td>\n'
                out_buf += '<td align="left">' + str(i[j]) + '</td>\n'
                rank += 1
                continue
            if j % 2:
                out_buf += '<td align="left">' + str(i[j]) + "(" + str('%.3f' % i[j + 1]) + "%)" + '</td>\n'
        out_buf += '</tr>\n'
    out_buf += "</table>"
    return out_buf


def top_list_sort(ls):
    ls.sort(key=lambda x: int(x[4]), reverse=True)
    return ls[:10]


# 书籍排行榜
def print_book_top(mlist, title, titleTup):
    if len(mlist) == 0:
        return ""
    outBuf = ""
    outBuf += '<h4>' + title + '</h4>\n'
    outBuf += '<table width="80%">\n'
    outBuf += '<tr align="center">'
    for i in titleTup:
        outBuf += '<th align="center">' + i + '</th>\n'
    outBuf += '</tr>\n'
    rank = 1
    for i in mlist:
        outBuf += '<tr align="center">'
        for j in range(len(i)):
            if j == 0:
                outBuf += '<td align="left">' + str(rank) + '</td>\n'
                outBuf += '<td align="left">' + str(i[j]) + '</td>\n'
                rank += 1
                continue
            outBuf += '<td align="left">' + str(i[j]) + '</td>\n'
        outBuf += '</tr>\n'
    outBuf += "</table>"
    return outBuf


def print_list(mlist, title, titleTup):
    outBuf = ""
    outBuf += '<h4>' + title + '</h4>\n'
    outBuf += '<table width="80%">\n'
    outBuf += '<tr align="center">'
    for i in titleTup:
        outBuf += '<th align="center">' + i + '</th>\n'
    outBuf += '</tr>\n'
    mlist.sort(key=lambda x: int(x[3]), reverse=True)
    for i in mlist:
        outBuf += '<tr align="left">\n'
        for j in range(0, len(i), 2):
            if j == 0:
                outBuf += '<td align="left">' + str(i[j]) + '</td>\n'
            else:
                outBuf += '<td align="left">' + str(i[j - 1]) + '(' + str("%.3f" % i[j]) + '%)' + '</td>\n'
        outBuf += "</tr>\n"
    outBuf += "</table>"
    return outBuf


def save_file(path, string):
    fw = open(path, "w")
    fw.write(string)
    fw.close()
    return
