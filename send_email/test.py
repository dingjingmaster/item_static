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

    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y = [100, 110, 120, 130, 140, 120, 110, 110, 220, 100, 120]
    y1 = [0.1, 0.11, 0.12, 0.13, 0.14, 0.12, 0.11, 0.11, 0.22, 0.1, 0.12]

    plt.figure(figsize=(10, 5))
    p = plt.subplot(121)
    # p.yaxis.set_major_locator(MultipleLocator(100000))
    plt.plot(x, y)
    plt.axis([0, 1000, 100, 1000])
    plt.xlabel('date')
    plt.ylabel('value')
    plt.legend()
    p = plt.subplot(122)
    plt.plot(x, y1)
    plt.legend()

    plt.show()
    # plt.savefig('./a.png')
