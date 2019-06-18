#!/usr/bin/env python
# -*- coding=utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf8")

from function import *

if __name__ == '__main__':
    if len(sys.argv) != 4:
        exit(-1)
    logPath = sys.argv[1]
    resultPath = sys.argv[2]
    app = sys.argv[3]

    # logPath = "../aa.txt"
    # resultPath = "./easou.txt"
    # app = "easou"

    # 输出结果链表
    outBufG = ""
    logListG = []                   # 日志
    ifmaskListG = []                # 是否屏蔽
    maskFeeListG = []               # 屏蔽-状态
    unmaskFeeListG = []             # 屏蔽书籍
    bysbyuListG = []
    bysfbyuListG = []
    monthListG = []
    chargeListCIG = []              # 按章付费
    chargeListFCG = []              # 免费阅读
    chargeListIIG = []              # 互联网书

    cpListG = []                    # 各个cp排行榜

    tfListG = []                    # 限免榜单 ???
    byListG = []                    # 包月榜单
    fcListG = []                    # 免费榜单
    iiListG = []                    # 互联网榜单
    ciListG = []                    # 按章计费榜单
    pubTopG = []                    # 公版榜单 ???

    """
    gid, name, author, cp, mask, fee, by, tf, fc, ii, ci
    userNum, chapterNum
    bysByuUserNum, bysByuChapterNum
    bysFByuUserNum, bysFBYuChapterNum
    """
    ## easou
    parse_info(logPath, logListG)

    mask_level_list(logListG, ifmaskListG, app)
    mask_fee_flag(logListG, maskFeeListG, app)
    unmask_fee_flag(logListG, unmaskFeeListG, app)
    tf_num(logListG, tfListG, app)                                              # 限免
    charge_ci_num(logListG, chargeListCIG, app)                                 # 按章计费情况
    charge_ii_num(logListG, chargeListIIG, app)                                 # 互联网书情况
    charge_fc_num(logListG, chargeListFCG, app)                                 # 免费CP情况
    month_num(logListG, bysbyuListG, bysfbyuListG, monthListG, app)             # 包月


    logListG, tfListG, byListG, fcListG, iiListG, ciListG, pubTopG = \
        top_list(logListG, tfListG, byListG, fcListG, iiListG, ciListG, pubTopG, app)
    cpListG = cp_top(logListG, cpListG, app)

    ### 宜搜
    outBufG += print_list(ifmaskListG,                    "屏蔽情况",     ("屏蔽/非屏蔽", "书籍量", "阅读量", "阅读章节数"))
    outBufG += print_list(maskFeeListG,             "屏蔽书阅读情况",        ("付费情况", "书籍量", "阅读量", "阅读章节数"))
    outBufG += print_list(unmaskFeeListG,         "非屏蔽书阅读情况",        ("付费情况", "书籍量", "阅读量", "阅读章节数"))
    outBufG += '<br/>'

    outBufG += print_list(chargeListCIG,     "非屏蔽&按章付费书情况",      ("阅读量分段", "书籍量", "阅读量", "阅读章节数"))
    outBufG += print_list(chargeListFCG,     "非屏蔽&免费CP阅读情况",      ("阅读量分段", "书籍量", "阅读量", "阅读章节数"))
    outBufG += print_list(bysbyuListG,     "非屏蔽&包月用户看包月书",      ("阅读量分段", "书籍量", "阅读量", "阅读章节数"))
    outBufG += print_list(bysfbyuListG,  "非屏蔽&非包月用户看包月书",      ("阅读量分段", "书籍量", "阅读量", "阅读章节数"))
    outBufG += print_list(chargeListIIG,       "非屏蔽&互联网书情况",      ("阅读量分段", "书籍量", "阅读量", "阅读章节数"))
    outBufG += '<br/>'

    outBufG += print_cp_top(cpListG,              "各cp阅读量top-10",  ("排名", "cp名", "阅读量及占比", "阅读章节数及占比"))
    outBufG += '<br/>'

    outBufG += print_book_top(ciListG,            "按章付费书排行榜",     ("排名", "书籍ID", "书籍名", "作者名", "阅读量", "阅读章节数"))
    outBufG += print_book_top(fcListG,        "全免书(免费CP)排行榜",     ("排名", "书籍ID", "书籍名", "作者名", "阅读量", "阅读章节数"))
    outBufG += print_book_top(byListG,                "包月书排行榜",     ("排名", "书籍ID", "书籍名", "作者名", "阅读量", "阅读章节数"))
    outBufG += print_book_top(tfListG,                "限免书排行榜",     ("排名", "书籍ID", "书籍名", "作者名", "阅读量", "阅读章节数"))
    outBufG += print_book_top(iiListG,              "互联网书排行榜",     ("排名", "书籍ID", "书籍名", "作者名", "阅读量", "阅读章节数"))
    outBufG += print_book_top(pubTopG,                "公版书排行榜",     ("排名", "书籍ID", "书籍名", "作者名", "阅读量", "阅读章节数"))

    save_file(resultPath, outBufG)
 
    exit(0)
