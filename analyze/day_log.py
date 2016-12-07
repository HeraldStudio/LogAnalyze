#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
 Create On: October 27, 2016
    Author: corvo
"""
from analyze.log_item import LogItem 
from databases.tables import DayLogAnalyze
from main import session
from config import logging
import json

class DayLog():

    """每日日志记录集合及每日日志简单操作"""

    def __init__(self, date):
        """ 初始化当日记录
        Args:
            date: 该条记录的日期

        """
        self.date = date
        self.log_list = []
        self.api_count = {}
        self.ip_count = {}
        self.every_hour_count = {}
        self.device_distribute = {}
        self.ios_version = {}
        self.android_version = {}

    def add_log_item(self, log_item):
        """ 向某天的日志中添加记录

        Args:
            log_item: 日志项

        """
        self.log_list.append(log_item)

    def get_most_called(self):
        """ 获取每日的接口调用前三十

        """
        #logging.INFO("每日API调用前十")
        for logItem in self.log_list:
            if logItem.api in self.api_count:
                self.api_count[logItem.api] += 1
            else:
                self.api_count[logItem.api] = 1

        data = sorted(self.api_count.items(), key=lambda d:d[1], reverse=True) # 排序

        self.api_count = dict((x, y) for x, y in data)    # 保存前十的数据

    def get_most_ip(self):
        """ 获取当日IP访问前3o

        """
        #print("每日ip接口调用前30")
        for logItem in self.log_list:
            if logItem.ip in self.ip_count:
                self.ip_count[logItem.ip] += 1
            else:
                self.ip_count[logItem.ip] = 1
        
        data = sorted(self.ip_count.items(), key=lambda d:d[1], reverse=True)   # 排序
        self.ip_count = dict((x, y) for x, y in data[-30:])

    def get_every_hour_called(self):
        """  获取每小时访问量

        """
        #print("每小时访问量")
        for logItem in self.log_list:
            if logItem.time.tm_hour in self.every_hour_count:
                self.every_hour_count[logItem.time.tm_hour] += 1
            else:
                self.every_hour_count[logItem.time.tm_hour] = 1
        
        # 每小时数据不需要排序
#        data =  sorted(self.every_hour_count.items(), key=lambda d:d[1], reverse=True)
        #print(self.every_hour_count)

    def get_device_called(self):
        """ 获取当日设备分布

        """
        #print("当日设备分布")
        for logItem in self.log_list:
            if logItem.device in self.device_distribute:
                self.device_distribute[logItem.device] += 1
            else:
                self.device_distribute[logItem.device] = 1
                
        data = sorted(self.device_distribute.items(), key=lambda d:d[1], reverse=True)

        #for item in data:
        #    print(item)
        self.device_distribute= dict((x, y) for x, y in data[-20:])    # 保存前十的数据
        #print(self.device_distribute)

    def get_ios_version(self):
        """ 获取当日ios设备版本分布

        """
        for logItem in self.log_list:
            if logItem.device == 'ios':
                if logItem.ios_version in self.ios_version:
                    self.ios_version[logItem.ios_version] += 1
                else:
                    self.ios_version[logItem.ios_version] = 1

    def get_android_version(self):
        """获取当日android设备版本分布

        """
        for logItem in self.log_list:
            if logItem.device == 'android':
                if logItem.android_version in self.android_version:
                    self.android_version[logItem.android_version] += 1
                else:
                    self.android_version[logItem.android_version] = 1
    
    def store_data(self):
        """ 将数据存储在数据库中

        """
        _api_count_json = json.dumps(self.api_count)
        _ip_count_json = json.dumps(self.ip_count)
        _every_hour_json = json.dumps(self.every_hour_count)
        _device_distribute_json = json.dumps(self.device_distribute)
        _ios_version = json.dumps(self.ios_version)
        _android_version = json.dumps(self.android_version)

        old = session.query(DayLogAnalyze).filter(DayLogAnalyze.date == self.date).all()

        if old:     # 如果该日日志已经存在
            print("Old Has Already Exists")
            return

        dayLog = DayLogAnalyze(
            date = self.date,
            api_order = _api_count_json,
            ip_order = _ip_count_json,
            every_hour_count = _every_hour_json,
            device_distribute = _device_distribute_json,
            call_count = len(self.log_list),
            ios_version = _ios_version,
            android_version = _android_version
            )
        session.add(dayLog)

        try:
            pass
            session.commit()
        except:
            session.rollback()
