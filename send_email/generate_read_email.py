#!/usr/bin/env python
# -*- coding=utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf8")

from function import *

if __name__ == '__main__':
    # if len(sys.argv) != 3:
    #     exit(-1)
    # logPath = sys.argv[1]
    # resultPath = sys.argv[2]

    logPath = "../aa.txt"
    resultPath = "../"

    # 输出结果链表
    outBufG = ""
    logListG = []                # 日志
    ifmaskListG = []             # 是否屏蔽
    maskFeeListG = []            # 屏蔽-状态
    unmaskFeeListG = []          # 屏蔽书籍
    bysbyuListG = []
    bysfbyuListG = []
    monthListG = []
    chargeListCIG = []           # 按章付费
    chargeListFCG = []           # 免费书付费
    chargeListIIG = []           # 互联网书
    tfListG = []
    chargeTopG = []
    fcTopG = []
    monthTopG = []
    tfTopG = []
    freeTopG = []
    pubTopG = []
    cpListG = []

    """
    gid, name, author, cp, mask, fee, by, tf, fc, ii, ci
    userNum, chapterNum
    bysByuUserNum, bysByuChapterNum
    bysFByuUserNum, bysFBYuChapterNum
    """
    ## easou
    parse_info(logPath, logListG)

    mask_level_list(logListG, ifmaskListG, "easou")
    mask_fee_flag(logListG, maskFeeListG, "easou")
    unmask_fee_flag(logListG, unmaskFeeListG, "easou")
    tf_num(logListG, tfListG, "easou")                                              # 限免
    charge_ci_num(logListG, chargeListCIG, "easou")                                 # 按章计费情况
    charge_ii_num(logListG, chargeListIIG, "easou")                                 # 互联网书情况
    charge_fc_num(logListG, chargeListFCG, "easou")                                 # 免费CP情况
    month_num(logListG, bysbyuListG, bysfbyuListG, monthListG, "easou")             # 包月


    # chargeTopG, monthTopG, tfTopG, freeTopG, pubTopG, fcTopG\
    #        = top_list(logListG, chargeTopG, monthTopG, tfTopG, freeTopG, pubTopG)
    # cpListG = cp_top(logListG, cpListG)

    outBufG += print_list(ifmaskListG,            "屏蔽情况", ("屏蔽/非屏蔽", "书籍量", "阅读量", "阅读章节数"))
    outBufG += print_list(maskFeeListG,     "屏蔽书阅读情况", ("付费情况", "书籍量", "阅读量", "阅读章节数"))
    outBufG += print_list(unmaskFeeListG, "非屏蔽书阅读情况", ("付费情况", "书籍量", "阅读量", "阅读章节数"))

    outBufG += print_list(tfListG,      "非屏蔽&限免书阅读情况",("阅读量分段", "书籍量", "阅读量", "阅读章节数"))
    outBufG += print_list(chargeListCIG,"非屏蔽&按章付费书情况",("阅读量分段", "书籍量", "阅读量", "阅读章节数"))
    outBufG += print_list(chargeListIIG,"非屏蔽&互联网书情况",  ("阅读量分段", "书籍量", "阅读量", "阅读章节数"))
    outBufG += print_list(chargeListFCG,"非屏蔽&免费CP阅读情况",("阅读量分段", "书籍量", "阅读量", "阅读章节数"))
    outBufG += print_list(bysbyuListG,"非屏蔽&包月用户看包月书", ("阅读量分段", "书籍量", "阅读量", "阅读章节数"))
    outBufG += print_list(bysfbyuListG,"非屏蔽&非包月用户看包月书",("阅读量分段", "书籍量", "阅读量", "阅读章节数"))
    # outBufG += print_list(monthListG, "非屏蔽&包月书情况",       ("阅读量分段", "书籍量", "阅读量", "阅读章节数"))

    #outBufG += print_book_top(chargeTopG, "付费书排行榜", ("排名", "书籍ID", "书籍名", "作者名", "阅读量", "阅读章节数"))
    #outBufG += print_book_top(fcTopG, "全免书排行榜", ("排名", "书籍ID", "书籍名", "作者名", "阅读量", "阅读章节数"))
    #outBufG += print_book_top(monthTopG,  "包月书排行榜", ("排名", "书籍ID", "书籍名", "作者名", "阅读量", "阅读章节数"))
    #outBufG += print_book_top(tfTopG,     "限免书排行榜", ("排名", "书籍ID", "书籍名", "作者名", "阅读量", "阅读章节数"))
    #outBufG += print_book_top(freeTopG,   "免费书排行榜", ("排名", "书籍ID", "书籍名", "作者名", "阅读量", "阅读章节数"))
    #outBufG += print_book_top(pubTopG,    "公版书排行榜", ("排名", "书籍ID", "书籍名", "作者名", "阅读量", "阅读章节数"))

    #outBufG += print_cp_top(cpListG,  "各cp阅读量top-10", ("排名", "cp名", "阅读量及占比", "阅读章节数及占比"))

    save_file(resultPath + "easou.txt", outBufG)

    ### 微卷
 
    exit(0)
