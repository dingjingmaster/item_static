#!/usr/bin/env python2.7
# -*- encoding=utf8 -*-

appid = {
    '10001': "宜搜小说",
    '10003': "10003",
    '20001': "微卷",
    '20001_1': "",
    '20002': "",
    '40001': "",
    '40002': "",
    '40003': "",
    '40004': "",
    '40005': "",
    '50001': "",
    '60001': ""
}

if __name__ == '__main__':
    item_value = '../data/item_value.txt'
    top_path = '../data/top100_list.txt'
    top100 = {}

    with open(item_value, 'r') as fr:
        for line in fr.readlines():
            line = line.strip()
            arr = line.split('\t')
            if len(arr) != 3:
                continue
            if arr[1] in top100:
                top100[arr[1]].append((arr[0], float(arr[2])))
            else:
                top100[arr[1]] = []
                top100[arr[1]].append((arr[0], float(arr[2])))

    # 排序
    for ik, iv in top100.items():
        iv.sort(key=lambda x: x[1], reverse=True)
        top100[ik] = iv

    # 输出
    fw = open(top_path, 'w')
    for ik, iv in top100.items():
        if (ik in appid) and ('' != appid[ik]):
            ik = appid[ik]
        fw.write('appid: ' + ik + ' 的top100书籍:\n')
        for gid, value in iv[:100]:
            fw.write('\t' + gid + '\t' + str(value) + '\n')
        fw.write('\n\n')
    fw.close()
