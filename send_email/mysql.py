#!/usr/bin/env python2.7
# -*- coding=utf-8 -*-
import sys
import time
import datetime
import MySQLdb
reload(sys)
sys.setdefaultencoding("utf8")


class Mysql:
    def __init__(self, ip, port, db, user, passwd):
        self.__ip = ip
        self.__port = port
        self.__db = db
        self.__user = user
        self.__passwd = passwd
        self.__conn = None
        self.__time = []

    def connect(self):
        self.__conn = MySQLdb.connect(self.__ip, self.__user, self.__passwd, self.__db)
        if None is self.__conn:
            print '连接数据库失败'
            return False
        return True

    def close(self):
        self.__conn.close()

    def save(self, app, value_type, value, time_stamp):
        id = self._get_id(app, value_type, time_stamp)
        if '' == id:
            return False
        msql = "INSERT INTO `item_earn`(" \
               "`id`, `app`, `value_type`, `value`, `time_stamp`)VALUES(" \
               "'%s', '%d', '%d', '%s', '%d');" % (
            id, self.__app[app], self.__value_type[value_type], value, int(time_stamp))
        try:
            cursor = self.__conn.cursor()
            cursor.execute(msql)
            self.__conn.commit()
        except:
            print 'sql' + msql + '执行错误!'
            return False
        return True

    def get_time_range_value(self, app, value_type, start_time, end_time):
        arr_value = {}
        msql = "SELECT `value`, `time_stamp` FROM `item_earn` " \
               "WHERE app = %d AND value_type = %d AND time_stamp >= %d AND time_stamp <= %d" %\
               (self.__app[app], self.__value_type[value_type], int(start_time), int(end_time))
        try:
            cursor = self.__conn.cursor()
            cursor.execute(msql)
            data = cursor.fetchall()
            for i in data:
                self.__time.append(int(i[1]))
                arr_value[int(i[1])] = float(i[0])
        except:
            print 'sql' + msql + '执行错误!'
            return False
        return arr_value

    def get_time_range(self, start, end):
        if len(self.__time) <= 0 or None is not self.__time:
            self.__time = []
            fstart = time.strptime(start, "%Y%m%d")
            index = 0
            while True:
                ps = (datetime.date.fromtimestamp(time.mktime(fstart))
                      + datetime.timedelta(days=index)).strftime("%Y%m%d")
                if int(ps) >= int(end):
                    self.__time.append(int(end))
                    break
                self.__time.append(int(ps))
                index += 1
        self.__time = list(set(self.__time))
        self.__time.sort()
        return self.__time

    def _get_id(self, app, value_type, time_stamp):
        id = ''
        if self.__app.has_key(app) and\
            self.__value_type.has_key(value_type):
            id = str(self.__app[app]) + '-'\
                + str(self.__value_type[value_type]) + '-'\
                + str(time_stamp)
        return id

    __app = {
        'easou': 1,
        'weijuan': 2,
    }
    __value_type = {
        'earn_sum': 1,
        'earn_aver': 2
    }
    pass


if __name__ == '__main__':
    mysql = Mysql('10.26.24.87', 3306, 'item_earn', 'root', '123456')
    mysql.connect()

