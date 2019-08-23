#!/usr/bin/env python2.7
# -*- coding=utf-8 -*-
import sys
import time
import datetime
import matplotlib
# matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.ticker import MultipleLocator
reload(sys)
sys.setdefaultencoding("utf8")


if __name__ == '__main__':

    x = [20190817, 20190818, 20190819, 20190820, 20190821]
    y = [4513043, 4546706, 4557366, 4479018, 4465836]

    plt.figure(figsize=(10, 5))
    p = plt.subplot(121)
    plt.xticks(x, x, rotation=45)
    p.set_ylim(bottom=1000000, top=8000000)
    plt.plot(x, y)
    for a, b in zip(x, y):
        plt.text(a, b, b, ha='center', va='bottom', fontsize=10)

    # p.set_xlim(20190817, 20190821)
    # p.axis([20190817, 20190821, 1000000, 10000000])
    plt.xlabel('date')
    plt.ylabel('value')
    plt.legend()
    p = plt.subplot(122)
    y = [36.867, 36.955, 37.075, 36.725, 36.826]
    plt.plot(x, y)
    plt.xticks(x, x, rotation=45)
    p.set_ylim(bottom=10, top=60)
    for a, b in zip(x, y):
        plt.text(a, b, b, ha='center', va='bottom', fontsize=10)

    plt.legend()

    plt.show()
    # start = "20190817"
    # end = "20190820"
    # fs = time.strptime(start, "%Y%m%d")
    # fe = time.strptime(end, "%Y%m%d")
    #
    # print fs
    # print fe
    #
    # td = datetime.date.fromtimestamp(time.mktime(fs))
    # te = datetime.date.fromtimestamp(time.mktime(fe))
    #
    # print td.strftime("%Y%m%d")
    # print te.strftime("%Y%m%d")
    #
    # print td + datetime.timedelta(days=2)
