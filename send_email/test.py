#!/usr/bin/env python2.7
# -*- coding=utf-8 -*-
import sys
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
    y1 = [36.867, 36.955, 37.075, 36.725, 36.826]

    plt.figure(figsize=(10, 5))
    p = plt.subplot(121)
    # p.yaxis.set_major_locator(MultipleLocator(100000))
    plt.plot(x, y)
    plt.xticks(x, x, rotation=45)
    p.set_ylim(bottom=100000, top=8000000)

    # p.set_xlim(20190817, 20190821)
    # p.axis([20190817, 20190821, 1000000, 10000000])
    plt.xlabel('date')
    plt.ylabel('value')
    plt.legend()
    p = plt.subplot(122)
    plt.plot(x, y1)
    plt.xticks(x, x, rotation=45)
    # plt.ylim(xmin=0)
    plt.legend()

    plt.show()
    # plt.savefig('./a.png')
