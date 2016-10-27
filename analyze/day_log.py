#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
 Create On: October 27, 2016
    Author: corvo
"""
from analyze.log_item import LogItem 

class DayLog():

    """每日日志记录集合及每日日志简单操作"""

    def __init__(self, date):
        """ 初始化当日记录
        Args:
            date: 该条记录的日期

        """
        self.date = date
        self.log_list = []

    def add_log_item(self, log_item):
        """ 向某天的日志中添加记录

        Args:
            log_item: 日志项

        """
        self.log_list.append(log_item)

    def get_most_called(self):
        """ 获取每日的接口调用前十
        Returns: TODO

        """
        print("每日接口调用前十")
        for logItem in self.log_list:
            pass

    def get_most_ip(self):
        """ 获取当日接口调用前十
        Returns: TODO

        """
        pass 

    def get_every_hour_called(self):
        """ 获取当日IP访问前十
        Returns: TODO

        """
        pass
    
    def get_device_called(self):
        """ 获取当日设备分布
        Returns: TODO

        """
        pass 

if __name__ == "__main__":
    dayLog = DayLog('3')
