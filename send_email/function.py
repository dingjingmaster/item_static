#!/usr/bin/env python
# -*- coding=utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf8")

#################################    共有    ####################################
# 解析获取的hadoop信息
def parse_info(logPath, logList):
    gid = ""
    name = ""
    author = ""
    maskLevel = ""
    feeFlag = ""
    by = ""
    tf = ""
    ncp = ""
    fc = ""
    userNum = ""
    chapterNum = ""
    bysByuUserNum = ""
    bysByuChapterNum = ""
    bysFbyuUserNum = ""
    bysFbyuChapterNum = ""
    fR = open(logPath, "r")
    """
        gid, name, author, cp, mask, fee, by, tf, fc, ii, ci
        userNum, chapterNum
        bysByuUserNum, bysByuChapterNum
        bysFByuUserNum, bysFBYuChapterNum
    """
    for line in fR.readlines():
        line = line.strip()
        arr = line.split("\t")
        gid = arr[0]
        name = arr[1]
        author = arr[2]
        ncp = arr[3]
        maskLevel = arr[4]
        feeFlag = arr[5]
        by = arr[6]
        tf = arr[7]
        fc = arr[8]
        ii = arr[9]
        ci = arr[10]
        userNum = arr[11]
        chapterNum = arr[12]
        bysByuUserNum = arr[13]
        bysByuChapterNum = arr[14]
        bysFbyuUserNum = arr[15]
        bysFbyuChapterNum = arr[16]
        logList.append((gid, name, author, ncp, maskLevel, feeFlag, by, tf, fc, ii, ci\
                , userNum, chapterNum\
                , bysByuUserNum, bysByuChapterNum\
                , bysFbyuUserNum, bysFbyuChapterNum))
    return logList

# 开始
def mask_level_list(logList, ifmaskList, app):
    maskBookNum = 0
    maskBookUserNum = 0             # 购买用户数
    maskChargeChapterNum = 0        # 章节购买量
    unmaskBookNum = 0
    unmaskBookUserNum = 0
    unmaskChargeChapterNum = 0
    allBookNum = 0
    allBookUserNum = 0
    allChargeChapterNum = 0
    for i in logList:
        usernumTemp = 0
        userChargeTemp = 0
        gid, name, author, ncp, maskLevel, feeFlag, by, tf, fc, ii, ci \
            , userNum, chapterNum \
            , bysByuUserNum, bysByuChapterNum \
            , bysFbyuUserNum, bysFbyuChapterNum = i
        apparr = gid.split("_")
        if apparr[2] != app:
            continue
        usernumTemp = int(userNum) + int(bysByuUserNum) + int(bysFbyuUserNum)
        userChargeTemp = int(chapterNum) + int(bysByuChapterNum) + int(bysFbyuChapterNum)
        allBookNum += 1
        allBookUserNum += int(usernumTemp)
        allChargeChapterNum += int(userChargeTemp)
        if maskLevel == u'1':
            maskBookNum += 1
            maskBookUserNum += int(usernumTemp)
            maskChargeChapterNum += int(userChargeTemp)
        elif maskLevel == u'0':
            unmaskBookNum += 1
            unmaskBookUserNum += int(usernumTemp)
            unmaskChargeChapterNum += int(userChargeTemp)
    if allBookNum == 0:
        allBookNum = 1
    if allBookUserNum == 0:
        allBookUserNum = 1
    if allChargeChapterNum == 0:
        allChargeChapterNum = 1
    ifmaskList.append(("屏蔽书", maskBookNum, float(maskBookNum)/allBookNum * 100\
            , maskBookUserNum, float(maskBookUserNum)/allBookUserNum * 100\
            , maskChargeChapterNum, float(maskChargeChapterNum)/allChargeChapterNum * 100))
    ifmaskList.append(("非屏蔽书", unmaskBookNum, float(unmaskBookNum)/allBookNum * 100\
            , unmaskBookUserNum, float(unmaskBookUserNum)/allBookUserNum * 100\
            , unmaskChargeChapterNum, float(unmaskChargeChapterNum)/allChargeChapterNum * 100))
    ifmaskList.append(("总计", allBookNum, 100, allBookUserNum, 100, allChargeChapterNum, 100))
    return ifmaskList

# 天阅读-屏蔽书情况
def mask_fee_flag(logList, maskFeeList, app):
    maskBookCharge = 0                      # 按章付费 - -
    maskBookUserCharge = 0
    maskBookChapterCharge = 0

    maskBookFreeCharge = 0                  # 免费 CP - -
    maskBookFreeUserCharge = 0
    maskBookFreeChapterCharge = 0

    maskBookTFreeCharge = 0                 # 互联网 - -
    maskBookTFreeUserCharge = 0
    maskBookTFreeChapterCharge = 0

    maskBookMonthus = 0                     # 包月用户包月书 - -
    maskBookUserMonthus = 0
    maskBookChapterMonthus = 0

    maskBookMonth = 0                       # 包月书非包月用户 - -
    maskBookUserMonth = 0
    maskBookChapterMonth = 0

    maskBookPublic = 0                      # 公版 - -
    maskBookUserPublic = 0
    maskBookChapterPublic = 0

    maskBooktf = 0                          # 限免 - -
    maskBookUsertf = 0
    maskBookChaptertf = 0

    allBook = 0
    allBookUser = 0
    allBookChapter = 0

    for i in logList:
        usernumTemp = 0
        userChargeTemp = 0
        gid, name, author, ncp, maskLevel, feeFlag, by, tf, fc, ii, ci \
            , userNum, chapterNum \
            , bysByuUserNum, bysByuChapterNum \
            , bysFbyuUserNum, bysFbyuChapterNum = i
        apparr = gid.split("_")
        if apparr[2] != app or maskLevel == u'0':
            continue
        usernumTemp = int(userNum) + int(bysByuUserNum) + int(bysFbyuUserNum)
        userChargeTemp = int(chapterNum) + int(bysByuChapterNum) + int(bysFbyuChapterNum)
        if tf == u'1':                                              # 限免
            allBook += 1
            allBookUser += int(usernumTemp)
            allBookChapter += int(userChargeTemp)

            maskBooktf += 1
            maskBookUsertf += int(usernumTemp)
            maskBookChaptertf += int(userChargeTemp)
        if int(by) == 1:                                             # 包月
            if int(bysByuUserNum) > 0:
                allBook += 1
                allBookUser += int(bysByuUserNum)
                allBookChapter += int(bysByuChapterNum)

                maskBookMonthus += 1
                maskBookUserMonthus += int(bysByuUserNum)
                maskBookChapterMonthus += int(bysByuChapterNum)
            if int(bysFbyuUserNum) > 0:
                allBook += 1
                allBookUser += int(bysFbyuUserNum)
                allBookChapter += int(bysFbyuChapterNum)

                maskBookMonth += 1
                maskBookUserMonth += int(bysFbyuUserNum)
                maskBookChapterMonth += int(bysFbyuChapterNum)
        if int(fc) == 0:                                            # 免费CP
            allBook += 1
            allBookUser += int(usernumTemp)
            allBookChapter += int(userChargeTemp)

            maskBookFreeCharge += 1
            maskBookFreeUserCharge += int(usernumTemp)
            maskBookFreeChapterCharge += int(userChargeTemp)
        if int(ci) == 1:                                            # 按章付费
            allBook += 1
            allBookUser += int(usernumTemp)
            allBookChapter += int(userChargeTemp)

            maskBookCharge += 1
            maskBookUserCharge += int(usernumTemp)
            maskBookChapterCharge += int(userChargeTemp)
        if int(ii) == 1:                                            # 互联网
            allBook += 1
            allBookUser += int(usernumTemp)
            allBookChapter += int(userChargeTemp)

            maskBookTFreeCharge += 1
            maskBookTFreeUserCharge += int(usernumTemp)
            maskBookTFreeChapterCharge += int(userChargeTemp)
        if int(feeFlag) == 10:                                      # 公版书
            allBook += 1
            allBookUser += int(usernumTemp)
            allBookChapter += int(userChargeTemp)

            maskBookPublic += 1
            maskBookUserPublic += int(usernumTemp)
            maskBookChapterPublic += int(userChargeTemp)
    if allBook == 0:
        allBook = 1
    if allBookUser == 0:
        allBookUser = 1
    if allBookChapter == 0:
        allBookChapter = 1
    maskFeeList.append(("限免书", maskBooktf, float(maskBooktf) / allBook * 100 \
                              , maskBookUsertf, float(maskBookUsertf) / allBookUser * 100 \
                              , maskBookChaptertf, float(maskBookChaptertf) / allBookChapter * 100))
    maskFeeList.append(("公版书", maskBookPublic, float(maskBookPublic) / allBook * 100 \
                              , maskBookUserPublic, float(maskBookUserPublic) / allBookUser * 100 \
                              , maskBookChapterPublic, float(maskBookChapterPublic) / allBookChapter * 100))
    maskFeeList.append(("包月书（非包月用户读）", maskBookMonth, float(maskBookMonth) / allBook * 100 \
                              , maskBookUserMonth, float(maskBookUserMonth) / allBookUser * 100 \
                              , maskBookChapterMonth, float(maskBookChapterMonth) / allBookChapter * 100))
    maskFeeList.append(("包月书（包月用户读）", maskBookMonthus, float(maskBookMonthus) / allBook * 100 \
                              , maskBookUserMonthus, float(maskBookUserMonthus) / allBookUser * 100 \
                              , maskBookChapterMonthus, float(maskBookChapterMonthus) / allBookChapter * 100))
    maskFeeList.append(("免费CP", maskBookFreeCharge, float(maskBookFreeCharge) / allBook * 100 \
                              , maskBookFreeUserCharge, float(maskBookFreeUserCharge) / allBookUser * 100 \
                              , maskBookFreeChapterCharge, float(maskBookFreeChapterCharge) / allBookChapter * 100))
    maskFeeList.append(("按章付费", maskBookCharge, float(maskBookCharge) / allBook * 100 \
                              , maskBookUserCharge, float(maskBookUserCharge) / allBookUser * 100 \
                              , maskBookChapterCharge, float(maskBookChapterCharge) / allBookChapter * 100))
    maskFeeList.append(("互联网书", maskBookTFreeCharge, float(maskBookTFreeCharge) / allBook * 100 \
                              , maskBookTFreeUserCharge, float(maskBookTFreeUserCharge) / allBookUser * 100 \
                              , maskBookTFreeChapterCharge, float(maskBookTFreeChapterCharge) / allBookChapter * 100))

    return maskFeeList

                
 
# 天阅读-非屏蔽书情况
def unmask_fee_flag(logList, unmaskFeeList, app):
    unmaskBookCharge = 0                                        # 按章付费 - -
    unmaskBookUserCharge = 0
    unmaskBookChapterCharge = 0

    unmaskBookFreeCharge = 0                                    # 免费 CP - -
    unmaskBookFreeUserCharge = 0
    unmaskBookFreeChapterCharge = 0

    unmaskBookTFreeCharge = 0                                   # 互联网 - -
    unmaskBookTFreeUserCharge = 0
    unmaskBookTFreeChapterCharge = 0

    unmaskBookMonthus = 0                                       # 包月用户包月书 - -
    unmaskBookUserMonthus = 0
    unmaskBookChapterMonthus = 0

    unmaskBookMonth = 0                                         # 包月书非包月用户 - -
    unmaskBookUserMonth = 0
    unmaskBookChapterMonth = 0

    unmaskBookPublic = 0                                        # 公版书 - -
    unmaskBookUserPublic = 0
    unmaskBookChapterPublic = 0

    unmaskBooktf = 0                                            # 限免 - -
    unmaskBookUsertf = 0
    unmaskBookChaptertf = 0

    allBook = 0
    allBookUser = 0
    allBookChapter = 0

    for i in logList:
        usernumTemp = 0
        userChargeTemp = 0
        gid, name, author, ncp, maskLevel, feeFlag, by, tf, fc, ii, ci \
            , userNum, chapterNum \
            , bysByuUserNum, bysByuChapterNum \
            , bysFbyuUserNum, bysFbyuChapterNum = i
        apparr = gid.split("_")
        if apparr[2] != app or int(maskLevel) == 1:
            continue
        usernumTemp = int(userNum) + int(bysByuUserNum) + int(bysFbyuUserNum)
        userChargeTemp = int(chapterNum) + int(bysByuChapterNum) + int(bysFbyuChapterNum)
        if tf == u'1':  # 限免
            allBook += 1
            allBookUser += int(usernumTemp)
            allBookChapter += int(userChargeTemp)

            unmaskBooktf += 1
            unmaskBookUsertf += int(usernumTemp)
            unmaskBookChaptertf += int(userChargeTemp)
        if int(by) == 1:  # 包月
            if int(bysByuUserNum) > 0:
                allBook += 1
                allBookUser += int(bysByuUserNum)
                allBookChapter += int(bysByuChapterNum)

                unmaskBookMonthus += 1
                unmaskBookUserMonthus += int(bysByuUserNum)
                unmaskBookChapterMonthus += int(bysByuChapterNum)
            if int(bysFbyuUserNum) > 0:
                allBook += 1
                allBookUser += int(bysFbyuUserNum)
                allBookChapter += int(bysFbyuChapterNum)

                unmaskBookMonth += 1
                unmaskBookUserMonth += int(bysFbyuUserNum)
                unmaskBookChapterMonth += int(bysFbyuChapterNum)
        if int(fc) == 0:  # 免费CP
            allBook += 1
            allBookUser += int(usernumTemp)
            allBookChapter += int(userChargeTemp)

            unmaskBookFreeCharge += 1
            unmaskBookFreeUserCharge += int(usernumTemp)
            unmaskBookFreeChapterCharge += int(userChargeTemp)
        if int(ci) == 1:  # 按章付费
            allBook += 1
            allBookUser += int(usernumTemp)
            allBookChapter += int(userChargeTemp)

            unmaskBookCharge += 1
            unmaskBookUserCharge += int(usernumTemp)
            unmaskBookChapterCharge += int(userChargeTemp)
        if int(ii) == 1:  # 互联网
            allBook += 1
            allBookUser += int(usernumTemp)
            allBookChapter += int(userChargeTemp)

            unmaskBookTFreeCharge += 1
            unmaskBookTFreeUserCharge += int(usernumTemp)
            unmaskBookTFreeChapterCharge += int(userChargeTemp)
        if int(feeFlag) == 10:  # 公版书
            allBook += 1
            allBookUser += int(usernumTemp)
            allBookChapter += int(userChargeTemp)

            unmaskBookPublic += 1
            unmaskBookUserPublic += int(usernumTemp)
            unmaskBookChapterPublic += int(userChargeTemp)
    if allBook == 0:
        allBook = 1
    if allBookUser == 0:
        allBookUser = 1
    if allBookChapter == 0:
        allBookChapter = 1
    unmaskFeeList.append(("限免书", unmaskBooktf, float(unmaskBooktf) / allBook * 100 \
            , unmaskBookUsertf, float(unmaskBookUsertf) / allBookUser * 100 \
            , unmaskBookChaptertf, float(unmaskBookChaptertf) / allBookChapter * 100))
    unmaskFeeList.append(("公版书", unmaskBookPublic, float(unmaskBookPublic) / allBook * 100 \
            , unmaskBookUserPublic, float(unmaskBookUserPublic) / allBookUser * 100 \
            , unmaskBookChapterPublic, float(unmaskBookChapterPublic) / allBookChapter * 100))
    unmaskFeeList.append(("包月书（非包月用户读）", unmaskBookMonth, float(unmaskBookMonth) / allBook * 100 \
            , unmaskBookUserMonth, float(unmaskBookUserMonth) / allBookUser * 100 \
            , unmaskBookChapterMonth, float(unmaskBookChapterMonth) / allBookChapter * 100))
    unmaskFeeList.append(("包月书（包月用户读）", unmaskBookMonthus, float(unmaskBookMonthus) / allBook * 100 \
            , unmaskBookUserMonthus, float(unmaskBookUserMonthus) / allBookUser * 100 \
            , unmaskBookChapterMonthus, float(unmaskBookChapterMonthus) / allBookChapter * 100))
    unmaskFeeList.append(("免费CP", unmaskBookFreeCharge, float(unmaskBookFreeCharge) / allBook * 100 \
            , unmaskBookFreeUserCharge, float(unmaskBookFreeUserCharge) / allBookUser * 100 \
            , unmaskBookFreeChapterCharge, float(unmaskBookFreeChapterCharge) / allBookChapter * 100))
    unmaskFeeList.append(("按章付费", unmaskBookCharge, float(unmaskBookCharge) / allBook * 100 \
            , unmaskBookUserCharge, float(unmaskBookUserCharge) / allBookUser * 100 \
            , unmaskBookChapterCharge, float(unmaskBookChapterCharge) / allBookChapter * 100))
    unmaskFeeList.append(("互联网书", unmaskBookTFreeCharge, float(unmaskBookTFreeCharge) / allBook * 100 \
            , unmaskBookTFreeUserCharge, float(unmaskBookTFreeUserCharge) / allBookUser * 100 \
            , unmaskBookTFreeChapterCharge, float(unmaskBookTFreeChapterCharge) / allBookChapter * 100))
    return unmaskFeeList

def tf_num(logList, tfList, app):
    tfBt0t10b = 0                   # 书籍数
    tfBt10t100b = 0
    tfBt100t1000b = 0
    tfBt1000t10000b = 0
    tfgt10000b = 0
    tfBt0t10u = 0                   # 用户数
    tfBt10t100u = 0
    tfBt100t1000u = 0
    tfBt1000t10000u = 0
    tfgt10000u = 0
    tfBt0t10c = 0                   # 付费章节
    tfBt10t100c = 0
    tfBt100t1000c = 0
    tfBt1000t10000c = 0
    tfgt10000c = 0

    allBook = 0
    allBookUser = 0
    allBookChapter = 0

    for i in logList:
        gid, name, author, ncp, maskLevel, feeFlag, by, tf, fc, ii, ci \
            , userNum, chapterNum \
            , bysByuUserNum, bysByuChapterNum \
            , bysFbyuUserNum, bysFbyuChapterNum = i
        apparr = gid.split("_")
        if apparr[2] != app or maskLevel == u'1':
            continue
        usernumTemp = int(userNum) + int(bysByuUserNum) + int(bysFbyuUserNum)
        userChargeTemp = int(chapterNum) + int(bysByuChapterNum) + int(bysFbyuChapterNum)
        if int(tf) == 1:
            allBook += 1
            allBookUser += int(usernumTemp)
            allBookChapter += int(userChargeTemp)
            if int(usernumTemp) > 0 and int(usernumTemp) < 10:
                tfBt0t10b += 1
                tfBt0t10u += int(usernumTemp)
                tfBt0t10c += int(userChargeTemp)
            elif int(usernumTemp) >= 10 and int(usernumTemp) < 100:
                tfBt10t100b += 1
                tfBt10t100u += int(usernumTemp)
                tfBt10t100c += int(userChargeTemp)
            elif int(usernumTemp) >= 100 and int(usernumTemp) < 1000:
                tfBt100t1000b += 1
                tfBt100t1000u += int(usernumTemp)
                tfBt100t1000c += int(userChargeTemp)
            elif int(usernumTemp) >= 1000 and int(usernumTemp) < 10000:
                tfBt1000t10000b += 1
                tfBt1000t10000u += int(usernumTemp)
                tfBt1000t10000c += int(userChargeTemp)
            elif int(usernumTemp) >= 10000:
                tfgt10000b += 1
                tfgt10000u += int(usernumTemp)
                tfgt10000c += int(userChargeTemp)
    if allBook == 0:
        allBook = 1
    if allBookUser == 0:
        allBookUser = 1
    if allBookChapter == 0:
        allBookChapter = 1
    tfList.append(("[0,10)", tfBt0t10b, float(tfBt0t10b)/allBook * 100\
            , tfBt0t10u, float(tfBt0t10u)/allBookUser * 100\
            , tfBt0t10c, float(tfBt0t10c)/allBookChapter * 100))
    tfList.append(("[10,100)", tfBt10t100b, float(tfBt10t100b)/allBook * 100\
            , tfBt10t100u, float(tfBt10t100u)/allBookUser * 100\
            , tfBt10t100c, float(tfBt10t100c)/allBookChapter * 100))
    tfList.append(("[100,1000)", tfBt100t1000b, float(tfBt100t1000b)/allBook * 100\
            , tfBt100t1000u, float(tfBt100t1000u)/allBookUser * 100\
            , tfBt100t1000c, float(tfBt100t1000c)/allBookChapter * 100))
    tfList.append(("[1000,10000)", tfBt1000t10000b, float(tfBt1000t10000b)/allBook * 100\
            , tfBt1000t10000u, float(tfBt1000t10000u)/allBookUser * 100\
            , tfBt1000t10000c, float(tfBt1000t10000c)/allBookChapter * 100))
    tfList.append(("[10000, ...)", tfgt10000b, float(tfgt10000b)/allBook * 100\
            , tfgt10000u, float(tfgt10000u)/allBookUser * 100\
            , tfgt10000c, float(tfgt10000c)/allBookChapter * 100))
    return tfList

def month_num(logList, bysbyuList, bysfbyuList, monthList, app):
    bysbyuBt0t10b = 0                   # 书籍数
    bysbyuBt10t100b = 0
    bysbyuBt100t1000b = 0
    bysbyuBt1000t10000b = 0
    bysbyugt10000b = 0

    bysbyuBt0t10u = 0                   # 用户数
    bysbyuBt10t100u = 0
    bysbyuBt100t1000u = 0
    bysbyuBt1000t10000u = 0
    bysbyugt10000u = 0

    bysbyuBt0t10c = 0                   # 付费章节
    bysbyuBt10t100c = 0
    bysbyuBt100t1000c = 0
    bysbyuBt1000t10000c = 0
    bysbyugt10000c = 0

    bysfbyuBt0t10b = 0
    bysfbyuBt10t100b = 0
    bysfbyuBt100t1000b = 0
    bysfbyuBt1000t10000b = 0
    bysfbyugt10000b = 0

    bysfbyuBt0t10u = 0
    bysfbyuBt10t100u = 0
    bysfbyuBt100t1000u = 0
    bysfbyuBt1000t10000u = 0
    bysfbyugt10000u = 0

    bysfbyuBt0t10c = 0
    bysfbyuBt10t100c = 0
    bysfbyuBt100t1000c = 0
    bysfbyuBt1000t10000c = 0
    bysfbyugt10000c = 0

    monthBt0t10b = 0                   # 书籍数
    monthBt10t100b = 0
    monthBt100t1000b = 0
    monthBt1000t10000b = 0
    monthgt10000b = 0

    monthBt0t10u = 0                   # 用户数
    monthBt10t100u = 0
    monthBt100t1000u = 0
    monthBt1000t10000u = 0
    monthgt10000u = 0

    monthBt0t10c = 0                   # 付费章节
    monthBt10t100c = 0
    monthBt100t1000c = 0
    monthBt1000t10000c = 0
    monthgt10000c = 0

    allbyusbook = 0
    allbyusbookuser = 0
    allbyusbookchapter = 0

    allbyufsbook = 0
    allbyufsbookuser = 0
    allbyufsbookchapter = 0
    
    for i in logList:
        gid, name, author, ncp, maskLevel, feeFlag, by, tf, fc, ii, ci \
            , userNum, chapterNum \
            , bysByuUserNum, bysByuChapterNum \
            , bysFbyuUserNum, bysFbyuChapterNum = i
        apparr = gid.split("_")
        if apparr[2] != app or maskLevel == u'1':
            continue
        monthusernumtemp = int(bysByuUserNum) + int(bysFbyuUserNum)
        monthchapternumtemp = int(bysByuChapterNum) + int(bysFbyuChapterNum)
        if int(by) == 1:
            if int(bysByuUserNum) >= 0 and int(bysByuUserNum) < 10:
                bysbyuBt0t10b += 1
                bysbyuBt0t10u += int(bysByuUserNum)
                bysbyuBt0t10c += int(bysByuChapterNum)
                allbyusbook += 1
                allbyusbookuser += int(bysByuUserNum)
                allbyusbookchapter += int(bysByuChapterNum)
            elif int(bysByuUserNum) >= 10 and int(bysByuUserNum) < 100:
                bysbyuBt10t100b += 1
                bysbyuBt10t100u += int(bysByuUserNum)
                bysbyuBt10t100c += int(bysByuChapterNum)
                allbyusbook += 1
                allbyusbookuser += int(bysByuUserNum)
                allbyusbookchapter += int(bysByuChapterNum)
            elif int(bysByuUserNum) >= 100 and int(bysByuUserNum) < 1000:
                bysbyuBt100t1000b += 1
                bysbyuBt100t1000u += int(bysByuUserNum)
                bysbyuBt100t1000c += int(bysByuChapterNum)
                allbyusbook += 1
                allbyusbookuser += int(bysByuUserNum)
                allbyusbookchapter += int(bysByuChapterNum)
            elif int(bysByuUserNum) >= 1000 and int(bysByuUserNum) < 10000:
                bysbyuBt1000t10000b += 1
                bysbyuBt1000t10000u += int(bysByuUserNum)
                bysbyuBt1000t10000c += int(bysByuChapterNum)
                allbyusbook += 1
                allbyusbookuser += int(bysByuUserNum)
                allbyusbookchapter += int(bysByuChapterNum)
            else:
                bysbyugt10000b += 1
                bysbyugt10000u += int(bysByuUserNum)
                bysbyugt10000c += int(bysByuChapterNum)
                allbyusbook += 1
                allbyusbookuser += int(bysByuUserNum)
                allbyusbookchapter += int(bysByuChapterNum)

            if int(bysFbyuUserNum) >= 0 and int(bysFbyuUserNum) < 10:
                bysfbyuBt0t10b += 1
                bysfbyuBt0t10u += int(bysFbyuUserNum)
                bysfbyuBt0t10c += int(bysFbyuChapterNum)
                allbyufsbook += 1
                allbyufsbookuser += int(bysFbyuUserNum)
                allbyufsbookchapter += int(bysFbyuChapterNum)
            elif int(bysFbyuUserNum) >= 10 and int(bysFbyuUserNum) < 100:
                bysfbyuBt10t100b += 1
                bysfbyuBt10t100u += int(bysFbyuUserNum)
                bysfbyuBt10t100c += int(bysFbyuChapterNum)
                allbyufsbook += 1
                allbyufsbookuser += int(bysFbyuUserNum)
                allbyufsbookchapter += int(bysFbyuChapterNum)
            elif int(bysFbyuUserNum) >= 100 and int(bysFbyuUserNum) < 1000:
                bysfbyuBt100t1000b += 1
                bysfbyuBt100t1000u += int(bysFbyuUserNum)
                bysfbyuBt100t1000c += int(bysFbyuChapterNum)
                allbyufsbook += 1
                allbyufsbookuser += int(bysFbyuUserNum)
                allbyufsbookchapter += int(bysFbyuChapterNum)
            elif int(bysFbyuUserNum) >= 1000 and int(bysFbyuUserNum) < 10000:
                bysfbyuBt1000t10000b += 1
                bysfbyuBt1000t10000u += int(bysFbyuUserNum)
                bysfbyuBt1000t10000c += int(bysFbyuChapterNum)
                allbyufsbook += 1
                allbyufsbookuser += int(bysFbyuUserNum)
                allbyufsbookchapter += int(bysFbyuChapterNum)
            else:
                bysfbyugt10000b += 1
                bysfbyugt10000u += int(bysFbyuUserNum)
                bysfbyugt10000c += int(bysFbyuChapterNum)
                allbyufsbook += 1
                allbyufsbookuser += int(bysFbyuUserNum)
                allbyufsbookchapter += int(bysFbyuChapterNum)

    if allbyusbook == 0:
        allbyusbook = 1
    if allbyusbookuser == 0:
        allbyusbookuser = 1
    if allbyusbookchapter == 0:
        allbyusbookchapter = 1
    if allbyufsbook == 0:
        allbyufsbook = 1
    if allbyufsbookuser == 0:
        allbyufsbookuser = 1
    if allbyufsbookchapter == 0:
        allbyufsbookchapter = 1

    bysbyuList.append(("(0,10)", bysbyuBt0t10b, float(bysbyuBt0t10b)/allbyusbook * 100\
            , bysbyuBt0t10u, float(bysbyuBt0t10u)/allbyusbookuser * 100\
            , bysbyuBt0t10c, float(bysbyuBt0t10c)/allbyusbookchapter * 100))
    bysbyuList.append(("[10,100)", bysbyuBt10t100b, float(bysbyuBt10t100b)/allbyusbook * 100\
            , bysbyuBt10t100u, float(bysbyuBt10t100u)/allbyusbookuser * 100\
            , bysbyuBt10t100c, float(bysbyuBt10t100c)/allbyusbookchapter * 100))
    bysbyuList.append(("[100,1000)", bysbyuBt100t1000b, float(bysbyuBt100t1000b)/allbyusbook * 100\
            , bysbyuBt100t1000u, float(bysbyuBt100t1000u)/allbyusbookuser * 100\
            , bysbyuBt100t1000c, float(bysbyuBt100t1000c)/allbyusbookchapter * 100))
    bysbyuList.append(("[1000,10000)", bysbyuBt1000t10000b, float(bysbyuBt1000t10000b)/allbyusbook * 100\
            , bysbyuBt1000t10000u, float(bysbyuBt1000t10000u)/allbyusbookuser * 100\
            , bysbyuBt1000t10000c, float(bysbyuBt1000t10000c)/allbyusbookchapter * 100))
    bysbyuList.append(("[10000, ...)", bysbyugt10000b, float(bysbyugt10000b)/allbyusbook * 100\
            , bysbyugt10000u, float(bysbyugt10000u)/allbyusbookuser * 100\
            , bysbyugt10000c, float(bysbyugt10000c)/allbyusbookchapter * 100))

    bysfbyuList.append(("[0,10)", bysfbyuBt0t10b, float(bysfbyuBt0t10b)/allbyufsbook * 100\
            , bysfbyuBt0t10u, float(bysfbyuBt0t10u)/allbyufsbookuser * 100\
            , bysfbyuBt0t10c, float(bysfbyuBt0t10c)/allbyufsbookchapter * 100))
    bysfbyuList.append(("[10,100)", bysfbyuBt10t100b, float(bysfbyuBt10t100b)/allbyufsbook * 100\
            , bysfbyuBt10t100u, float(bysfbyuBt10t100u)/allbyufsbookuser * 100\
            , bysfbyuBt10t100c, float(bysfbyuBt10t100c)/allbyufsbookchapter * 100))
    bysfbyuList.append(("[100,1000)", bysfbyuBt100t1000b, float(bysfbyuBt100t1000b)/allbyufsbook * 100\
            , bysfbyuBt100t1000u, float(bysfbyuBt100t1000u)/allbyufsbookuser * 100\
            , bysfbyuBt100t1000c, float(bysfbyuBt100t1000c)/allbyufsbookchapter * 100))
    bysfbyuList.append(("[1000,10000)", bysfbyuBt1000t10000b, float(bysfbyuBt1000t10000b)/allbyufsbook * 100\
            , bysfbyuBt1000t10000u, float(bysfbyuBt1000t10000u)/allbyufsbookuser * 100\
            , bysfbyuBt1000t10000c, float(bysfbyuBt1000t10000c)/allbyufsbookchapter * 100))
    bysfbyuList.append(("[10000, ...)", bysfbyugt10000b, float(bysfbyugt10000b)/allbyufsbook * 100\
            , bysfbyugt10000u, float(bysfbyugt10000u)/allbyufsbookuser * 100\
            , bysfbyugt10000c, float(bysfbyugt10000c)/allbyufsbookchapter * 100))
    return (bysbyuList, bysfbyuList, monthList)


def charge_ci_num(loglist, chargelist, app):
    chargebt0t10b = 0                   # 书籍数
    chargebt10t100b = 0
    chargebt100t1000b = 0
    chargebt1000t10000b = 0
    chargegt10000b = 0
    chargebt0t10u = 0                   # 用户数
    chargebt10t100u = 0
    chargebt100t1000u = 0
    chargebt1000t10000u = 0
    chargegt10000u = 0
    chargebt0t10c = 0                   # 付费章节
    chargebt10t100c = 0
    chargebt100t1000c = 0
    chargebt1000t10000c = 0
    chargegt10000c = 0

    allbook = 0
    allbookuser = 0
    allbookchapter = 0

    for i in loglist:
        gid, name, author, ncp, maskLevel, feeFlag, by, tf, fc, ii, ci \
            , userNum, chapterNum \
            , bysByuUserNum, bysByuChapterNum \
            , bysFbyuUserNum, bysFbyuChapterNum = i
        apparr = gid.split("_")
        if apparr[2] != app or maskLevel == u'1':
            continue
        usernumtemp = int(userNum) + int(bysByuUserNum) + int(bysFbyuUserNum)
        userchargetemp = int(chapterNum) + int(bysByuChapterNum) + int(bysFbyuChapterNum)
        if ci == u'1':
            allbook += 1
            allbookuser += int(usernumtemp)
            allbookchapter += int(userchargetemp)
            if int(usernumtemp) > 0 and int(usernumtemp) < 10:
                chargebt0t10b += 1
                chargebt0t10u += int(usernumtemp)
                chargebt0t10c += int(userchargetemp)
            elif int(usernumtemp) >= 10 and int(usernumtemp) < 100:
                chargebt10t100b += 1
                chargebt10t100u += int(usernumtemp)
                chargebt10t100c += int(userchargetemp)
            elif int(usernumtemp) >= 100 and int(usernumtemp) < 1000:
                chargebt100t1000b += 1
                chargebt100t1000u += int(usernumtemp)
                chargebt100t1000c += int(userchargetemp)
            elif int(usernumtemp) >= 1000 and int(usernumtemp) < 10000:
                chargebt1000t10000b += 1
                chargebt1000t10000u += int(usernumtemp)
                chargebt1000t10000c += int(userchargetemp)
            else:
                chargegt10000b += 1
                chargegt10000u += int(usernumtemp)
                chargegt10000c += int(userchargetemp)
    if allbook == 0:
        allbook = 1
    if allbookuser == 0:
        allbookuser = 1
    if allbookchapter == 0:
        allbookchapter = 1
    chargelist.append(("(0,10)", chargebt0t10b, float(chargebt0t10b)/allbook * 100\
            , chargebt0t10u, float(chargebt0t10u)/allbookuser * 100\
            , chargebt0t10c, float(chargebt0t10c)/allbookchapter * 100))
    chargelist.append(("[10,100)", chargebt10t100b, float(chargebt10t100b)/allbook * 100\
            , chargebt10t100u, float(chargebt10t100u)/allbookuser * 100\
            , chargebt10t100c, float(chargebt10t100c)/allbookchapter * 100))
    chargelist.append(("[100,1000)", chargebt100t1000b, float(chargebt100t1000b)/allbook * 100\
            , chargebt100t1000u, float(chargebt100t1000u)/allbookuser * 100\
            , chargebt100t1000c, float(chargebt100t1000c)/allbookchapter * 100))
    chargelist.append(("[1000,10000)", chargebt1000t10000b, float(chargebt1000t10000b)/allbook * 100\
            , chargebt1000t10000u, float(chargebt1000t10000u)/allbookuser * 100\
            , chargebt1000t10000c, float(chargebt1000t10000c)/allbookchapter * 100))
    chargelist.append(("[10000, ...)", chargegt10000b, float(chargegt10000b)/allbook * 100\
            , chargegt10000u, float(chargegt10000u)/allbookuser * 100\
            , chargegt10000c, float(chargegt10000c)/allbookchapter * 100))
    return chargelist


def charge_fc_num(loglist, chargelist, app):
    chargebt0t10b = 0                   # 书籍数
    chargebt10t100b = 0
    chargebt100t1000b = 0
    chargebt1000t10000b = 0
    chargegt10000b = 0
    chargebt0t10u = 0                   # 用户数
    chargebt10t100u = 0
    chargebt100t1000u = 0
    chargebt1000t10000u = 0
    chargegt10000u = 0
    chargebt0t10c = 0                   # 付费章节
    chargebt10t100c = 0
    chargebt100t1000c = 0
    chargebt1000t10000c = 0
    chargegt10000c = 0

    allbook = 0
    allbookuser = 0
    allbookchapter = 0

    for i in loglist:
        gid, name, author, ncp, maskLevel, feeFlag, by, tf, fc, ii, ci \
            , userNum, chapterNum \
            , bysByuUserNum, bysByuChapterNum \
            , bysFbyuUserNum, bysFbyuChapterNum = i
        apparr = gid.split("_")
        if apparr[2] != app or maskLevel == u'1':
            continue
        usernumtemp = int(userNum) + int(bysByuUserNum) + int(bysFbyuUserNum)
        userchargetemp = int(chapterNum) + int(bysByuChapterNum) + int(bysFbyuChapterNum)
        if fc == u'1':
            allbook += 1
            allbookuser += int(usernumtemp)
            allbookchapter += int(userchargetemp)
            if int(usernumtemp) > 0 and int(usernumtemp) < 10:
                chargebt0t10b += 1
                chargebt0t10u += int(usernumtemp)
                chargebt0t10c += int(userchargetemp)
            elif int(usernumtemp) >= 10 and int(usernumtemp) < 100:
                chargebt10t100b += 1
                chargebt10t100u += int(usernumtemp)
                chargebt10t100c += int(userchargetemp)
            elif int(usernumtemp) >= 100 and int(usernumtemp) < 1000:
                chargebt100t1000b += 1
                chargebt100t1000u += int(usernumtemp)
                chargebt100t1000c += int(userchargetemp)
            elif int(usernumtemp) >= 1000 and int(usernumtemp) < 10000:
                chargebt1000t10000b += 1
                chargebt1000t10000u += int(usernumtemp)
                chargebt1000t10000c += int(userchargetemp)
            else:
                chargegt10000b += 1
                chargegt10000u += int(usernumtemp)
                chargegt10000c += int(userchargetemp)
    if allbook == 0:
        allbook = 1
    if allbookuser == 0:
        allbookuser = 1
    if allbookchapter == 0:
        allbookchapter = 1
    chargelist.append(("(0,10)", chargebt0t10b, float(chargebt0t10b)/allbook * 100\
            , chargebt0t10u, float(chargebt0t10u)/allbookuser * 100\
            , chargebt0t10c, float(chargebt0t10c)/allbookchapter * 100))
    chargelist.append(("[10,100)", chargebt10t100b, float(chargebt10t100b)/allbook * 100\
            , chargebt10t100u, float(chargebt10t100u)/allbookuser * 100\
            , chargebt10t100c, float(chargebt10t100c)/allbookchapter * 100))
    chargelist.append(("[100,1000)", chargebt100t1000b, float(chargebt100t1000b)/allbook * 100\
            , chargebt100t1000u, float(chargebt100t1000u)/allbookuser * 100\
            , chargebt100t1000c, float(chargebt100t1000c)/allbookchapter * 100))
    chargelist.append(("[1000,10000)", chargebt1000t10000b, float(chargebt1000t10000b)/allbook * 100\
            , chargebt1000t10000u, float(chargebt1000t10000u)/allbookuser * 100\
            , chargebt1000t10000c, float(chargebt1000t10000c)/allbookchapter * 100))
    chargelist.append(("[10000, ...)", chargegt10000b, float(chargegt10000b)/allbook * 100\
            , chargegt10000u, float(chargegt10000u)/allbookuser * 100\
            , chargegt10000c, float(chargegt10000c)/allbookchapter * 100))
    return chargelist

def charge_ii_num(loglist, chargelist, app):
    chargebt0t10b = 0                   # 书籍数
    chargebt10t100b = 0
    chargebt100t1000b = 0
    chargebt1000t10000b = 0
    chargegt10000b = 0
    chargebt0t10u = 0                   # 用户数
    chargebt10t100u = 0
    chargebt100t1000u = 0
    chargebt1000t10000u = 0
    chargegt10000u = 0
    chargebt0t10c = 0                   # 付费章节
    chargebt10t100c = 0
    chargebt100t1000c = 0
    chargebt1000t10000c = 0
    chargegt10000c = 0

    allbook = 0
    allbookuser = 0
    allbookchapter = 0

    for i in loglist:
        gid, name, author, ncp, maskLevel, feeFlag, by, tf, fc, ii, ci \
            , userNum, chapterNum \
            , bysByuUserNum, bysByuChapterNum \
            , bysFbyuUserNum, bysFbyuChapterNum = i
        apparr = gid.split("_")
        if apparr[2] != app or maskLevel == u'1':
            continue
        usernumtemp = int(userNum) + int(bysByuUserNum) + int(bysFbyuUserNum)
        userchargetemp = int(chapterNum) + int(bysByuChapterNum) + int(bysFbyuChapterNum)
        if ii == u'1':
            allbook += 1
            allbookuser += int(usernumtemp)
            allbookchapter += int(userchargetemp)
            if int(usernumtemp) > 0 and int(usernumtemp) < 10:
                chargebt0t10b += 1
                chargebt0t10u += int(usernumtemp)
                chargebt0t10c += int(userchargetemp)
            elif int(usernumtemp) >= 10 and int(usernumtemp) < 100:
                chargebt10t100b += 1
                chargebt10t100u += int(usernumtemp)
                chargebt10t100c += int(userchargetemp)
            elif int(usernumtemp) >= 100 and int(usernumtemp) < 1000:
                chargebt100t1000b += 1
                chargebt100t1000u += int(usernumtemp)
                chargebt100t1000c += int(userchargetemp)
            elif int(usernumtemp) >= 1000 and int(usernumtemp) < 10000:
                chargebt1000t10000b += 1
                chargebt1000t10000u += int(usernumtemp)
                chargebt1000t10000c += int(userchargetemp)
            else:
                chargegt10000b += 1
                chargegt10000u += int(usernumtemp)
                chargegt10000c += int(userchargetemp)
    if allbook == 0:
        allbook = 1
    if allbookuser == 0:
        allbookuser = 1
    if allbookchapter == 0:
        allbookchapter = 1
    chargelist.append(("(0,10)", chargebt0t10b, float(chargebt0t10b)/allbook * 100\
            , chargebt0t10u, float(chargebt0t10u)/allbookuser * 100\
            , chargebt0t10c, float(chargebt0t10c)/allbookchapter * 100))
    chargelist.append(("[10,100)", chargebt10t100b, float(chargebt10t100b)/allbook * 100\
            , chargebt10t100u, float(chargebt10t100u)/allbookuser * 100\
            , chargebt10t100c, float(chargebt10t100c)/allbookchapter * 100))
    chargelist.append(("[100,1000)", chargebt100t1000b, float(chargebt100t1000b)/allbook * 100\
            , chargebt100t1000u, float(chargebt100t1000u)/allbookuser * 100\
            , chargebt100t1000c, float(chargebt100t1000c)/allbookchapter * 100))
    chargelist.append(("[1000,10000)", chargebt1000t10000b, float(chargebt1000t10000b)/allbook * 100\
            , chargebt1000t10000u, float(chargebt1000t10000u)/allbookuser * 100\
            , chargebt1000t10000c, float(chargebt1000t10000c)/allbookchapter * 100))
    chargelist.append(("[10000, ...)", chargegt10000b, float(chargegt10000b)/allbook * 100\
            , chargegt10000u, float(chargegt10000u)/allbookuser * 100\
            , chargegt10000c, float(chargegt10000c)/allbookchapter * 100))
    return chargelist


def cp_top(loglist, cplist, app):
    alluser = 0
    allchap = 0
    othuser = 0
    othchap = 0
    cpdict = {}
    for i in loglist:
        gid, name, author, ncp, maskLevel, feeFlag, by, tf, fc, ii, ci \
            , userNum, chapterNum \
            , bysByuUserNum, bysByuChapterNum \
            , bysFbyuUserNum, bysFbyuChapterNum = i
        apparr = gid.split("_")
        if apparr[2] != app or maskLevel == u'1':
            continue
        usernumtemp = int(userNum) + int(bysByuUserNum) + int(bysFbyuUserNum)
        userchargetemp = int(chapterNum) + int(bysByuChapterNum) + int(bysFbyuChapterNum)
        if ncp == u'免费书':
            continue
        if cpdict.has_key(ncp):
            user, chapter = cpdict[ncp]
            user += int(usernumtemp)
            chapter += int(userchargetemp)
            cpdict[ncp] = (user, chapter)
        else:
            cpdict[ncp] = (int(usernumtemp), int(userchargetemp))
    for cp, value in cpdict.items():
        usernum, chapternum = value
        alluser += int(usernum)
        allchap += int(chapternum)
        cplist.append((cp, int(usernum), int(chapternum)))
    cplist.sort(key = lambda x: int(x[1]), reverse = True)

    cplisttop = cplist[:10]
    for i in range(10, len(cplist)):
        cp, usernum, chapnum = cplist[i]
        othuser += usernum
        othchap += chapnum
    cplisttop.append((u'其它', int(othuser), int(othchap)))
    #'''
    cplist = []
    for i in cplisttop:
        cp, user, chap = i
        cplist.append((cp, user, float(user)/alluser * 100, chap, float(chap)/allchap * 100))
    return cplist


def top_list(logListG, tfListG, byListG, fcListG, iiListG, ciListG, pubListG, app):
    for i in logListG:
        gid, name, author, ncp, maskLevel, feeFlag, by, tf, fc, ii, ci \
            , userNum, chapterNum \
            , bysByuUserNum, bysByuChapterNum \
            , bysFbyuUserNum, bysFbyuChapterNum = i
        apparr = gid.split("_")
        gid = "i_" + apparr[1]
        if apparr[2] != app or maskLevel == u'1':
            continue
        usernumTemp = int(userNum) + int(bysByuUserNum) + int(bysFbyuUserNum)
        userChargeTemp = int(chapterNum) + int(bysByuChapterNum) + int(bysFbyuChapterNum)

        if tf != u'1':                                                                      # 限免
            tfListG.append((gid, name, author, usernumTemp, userChargeTemp))
        if by != u'1':                                                                      # 包月
            byListG.append((gid, name, author, usernumTemp, userChargeTemp))
        if fc == u'1':                                                                      # 免费
            fcListG.append((gid, name, author, usernumTemp, userChargeTemp))
        elif ii == u'1':                                                                    # 互联网
            iiListG.append((gid, name, author, usernumTemp, userChargeTemp))
        elif ci == u'1':                                                                    # 按章计费
            ciListG.append((gid, name, author, usernumTemp, userChargeTemp))
        elif pubListG == u'1':                                                              # 公版书
            pubListG.append((gid, name, author, usernumTemp, userChargeTemp))

    tfListG.sort(key = lambda x: x[3], reverse = True)
    byListG.sort(key = lambda x: x[3], reverse = True)
    fcListG.sort(key = lambda x: x[3], reverse = True)
    iiListG.sort(key = lambda x: x[3], reverse = True)
    ciListG.sort(key = lambda x: x[3], reverse = True)
    pubListG.sort(key = lambda x: x[3], reverse = True)
    tfListG = tfListG[:10]
    byListG = byListG[:10]
    fcListG = fcListG[:10]
    iiListG = iiListG[:10]
    ciListG = ciListG[:10]
    pubListG = pubListG[:10]
    return tfListG, byListG, fcListG, iiListG, ciListG, pubListG

def print_cp_top(mlist, title, titleTup):
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
            if j % 2:
                outBuf += '<td align="left">' + str(i[j]) + "(" + str('%.3f' % i[j + 1]) + "%)" + '</td>\n'
        outBuf += '</tr>\n'
    outBuf += "</table>"
    return outBuf

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
    mlist.sort(key = lambda x: int(x[3]), reverse = True)
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
    fW = open(path, "w")
    fW.write(string)
    fW.close()
    return


