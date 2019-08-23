#!/usr/bin/env python2.7
# -*- coding=utf-8 -*-
import sys
import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.ticker import MultipleLocator
reload(sys)
sys.setdefaultencoding("utf8")


if __name__ == '__main__':

    plt.figure(figsize=(10, 5))
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y = [100, 110, 120, 130, 140, 120, 110, 110, 220, 100, 120]
    # p.yaxis.set_major_locator(MultipleLocator(100000))
    plt.plot(x, y)
    plt.xlabel('date')
    plt.ylabel('value')
    plt.legend()
    # plt.show()
    plt.savefig('./a.png')
