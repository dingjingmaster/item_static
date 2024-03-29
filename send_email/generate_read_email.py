#!/usr/bin/env python2.7
# -*- coding=utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding("utf8")

from function import *

if __name__ == '__main__':
    if len(sys.argv) != 4:
        exit(-1)
    log_path = sys.argv[1]
    result_path = sys.argv[2]
    app = sys.argv[3]

    # log_path = "../day_detail.txt"
    # result_path = "../easou.txt"
    # app = "10001"

    # 输出结果链表
    out_str = ""
    log_list_g = []             # 日志数据

    cp_top_list_g = []          # cp 阅读排行榜

    charge_top_g = []           # 付费排行榜
    free_top_g = []             # 免费排行榜
    free_charge_top_g = []      # 按章计费免费排行榜
    limit_free_top_g = []       # 限免排行榜
    baoyue_top_g = []           # 包月排行榜
    hulianwang_top_g = []       # 互联网排行榜
    bys_free_top_g = []

    charge_list_g = []          # 付费阅读情况
    free_list_g = []            # 免费阅读情况
    free_charge_list_g = []     # 免费 按章计费阅读情况
    limit_free_list_g = []      # 限免阅读情况
    baoyue_list_g = []          # 包月阅读情况
    bys_free_list_g = []
    hulianwang_list_g = []      # 互联网阅读情况

    """ 数据读取 """
    log_list_g = read_data(log_path, app)

    charge_top_g, charge_list_g = category_analysis_list(log_list_g, '付费')
    free_top_g, free_list_g = category_analysis_list(log_list_g, '免费(免费cp)')
    free_charge_top_g, free_charge_list_g = category_analysis_list(log_list_g, '免费(按章计费)')
    limit_free_top_g, limit_free_list_g = category_analysis_list(log_list_g, '限免')
    baoyue_top_g, baoyue_list_g = category_analysis_list(log_list_g, '包月')
    bys_free_top_g, bys_free_list_g = category_analysis_list(log_list_g, '免费(包月书)')
    hulianwang_top_g, hulianwang_list_g = category_analysis_list(log_list_g, '互联网')

    # 输出分段阅读情况
    out_str += print_list(charge_list_g,            "按章计费付费章节阅读情况",      ("阅读量分段", "书籍量", "阅读量", "阅读章节数"))
    out_str += print_list(free_list_g,              "免费cp章节阅读情况",           ("阅读量分段", "书籍量", "阅读量", "阅读章节数"))
    out_str += print_list(free_charge_list_g,       "按章计费免费章节阅读情况",     ("阅读量分段", "书籍量", "阅读量", "阅读章节数"))
    out_str += print_list(bys_free_list_g,       "包月书非包月用户阅读免费章节",     ("阅读量分段", "书籍量", "阅读量", "阅读章节数"))
    out_str += print_list(limit_free_list_g,        "限免阅读情况",               ("阅读量分段", "书籍量", "阅读量", "阅读章节数"))
    out_str += print_list(baoyue_list_g,            "包月阅读情况",               ("阅读量分段", "书籍量", "阅读量", "阅读章节数"))
    out_str += print_list(hulianwang_list_g,        "互联网阅读情况",              ("阅读量分段", "书籍量", "阅读量", "阅读章节数"))
    out_str += "<br/>"

    # 输出排行榜
    out_str += print_book_top(top_list_sort(charge_top_g),
                              "付费排行榜",          ("排名", "gid", "书名", "作者名", "cp", "用户地区", "阅读量", "阅读章节量"))
    del charge_top_g
    del charge_list_g

    out_str += print_book_top(top_list_sort(free_top_g),
                              "免费cp排行榜",        ("排名", "gid", "书名", "作者名", "cp", "用户地区", "阅读量", "阅读章节量"))
    del free_top_g
    del free_list_g

    out_str += print_book_top(top_list_sort(free_charge_top_g),
                              "按章付费免费阅读排行榜", ("排名", "gid", "书名", "作者名", "cp", "用户地区", "阅读量", "阅读章节量"))
    del free_charge_top_g
    del free_charge_list_g

    out_str += print_book_top(top_list_sort(limit_free_top_g),
                              "限免排行榜",          ("排名", "gid", "书名", "作者名", "cp", "用户地区", "阅读量", "阅读章节量"))
    del limit_free_top_g
    del limit_free_list_g

    out_str += print_book_top(top_list_sort(bys_free_top_g),
                              "包月书非包月用户阅读免费章节",
                                                    ("排名", "gid", "书名", "作者名", "cp", "用户地区", "阅读量", "阅读章节量"))
    del bys_free_top_g
    del bys_free_list_g

    out_str += print_book_top(top_list_sort(baoyue_top_g),
                              "包月排行榜",          ("排名", "gid", "书名", "作者名", "cp", "用户地区", "阅读量", "阅读章节量"))
    del baoyue_top_g
    del baoyue_list_g

    out_str += print_book_top(top_list_sort(hulianwang_top_g),
                              "互联网排行榜",         ("排名", "gid", "书名", "作者名", "cp", "用户地区", "阅读量", "阅读章节量"))
    del hulianwang_top_g
    del hulianwang_list_g
    out_str += "<br/>"

    cp_top_list_g = cp_top(log_list_g)
    out_str += print_cp_top(cp_top_list_g,
                            "各cp阅读量top10", ("排名", "cp", "书籍量", "阅读量", "阅读章节量"))
    del cp_top_list_g

    save_file(result_path, out_str)

    exit(0)
