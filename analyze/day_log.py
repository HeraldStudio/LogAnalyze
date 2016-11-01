#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
 Create On: October 27, 2016
    Author: corvo
"""
from analyze.log_item import LogItem 
from config import mysql_host
from config import mysql_user
from config import mysql_password
from config import mysql_database


import pymysql 
import json

conn = pymysql.connect(host=mysql_host, 
                       user=mysql_user,
                       passwd=mysql_password, 
                       charset='utf8', 
                       database=mysql_database)
cur = conn.cursor()

INSERT_STR = """
    INSERT INTO day_log_analyze 
    (date, api_order, ip_order, every_hour_count, device_distribute)
    VALUES (%(date)s, %(api)s, %(ip)s, %(every_hour)s, %(device)s)
"""

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
        print("每日API调用前十")
        for logItem in self.log_list:
            if logItem.api in self.api_count:
                self.api_count[logItem.api] += 1
            else:
                self.api_count[logItem.api] = 1

        data = sorted(self.api_count.items(), key=lambda d:d[1], reverse=True) # 排序

        self.api_count = dict((x, y) for x, y in data[-10:])    # 保存前十的数据
        print(self.api_count)

    def get_most_ip(self):
        """ 获取当日IP访问前3o
        Returns: TODO

        """
        print("每日ip接口调用前30")
        for logItem in self.log_list:
            if logItem.ip in self.ip_count:
                self.ip_count[logItem.ip] += 1
            else:
                self.ip_count[logItem.ip] = 1
        
        data = sorted(self.ip_count.items(), key=lambda d:d[1], reverse=True)   # 排序
        self.ip_count = dict((x, y) for x, y in data[-30:])
        print(self.ip_count)
        jsonArray = dict((x, y) for x, y in data[-30:])
        jsonArray = json.dumps(jsonArray)

    def get_every_hour_called(self):
        """  获取每小时访问量
        Returns: TODO

        """
        print("每小时访问量")
        for logItem in self.log_list:
            if logItem.time.tm_hour in self.every_hour_count:
                self.every_hour_count[logItem.time.tm_hour] += 1
            else:
                self.every_hour_count[logItem.time.tm_hour] = 1
        
        # 每小时数据不需要排序
#        data =  sorted(self.every_hour_count.items(), key=lambda d:d[1], reverse=True)
        print(self.every_hour_count)

    def get_device_called(self):
        """ 获取当日设备分布
        Returns: TODO

        """
        print("当日设备分布")
        for logItem in self.log_list:
            if logItem.device in self.device_distribute:
                self.device_distribute[logItem.device] += 1
            else:
                self.device_distribute[logItem.device] = 1
                
        data = sorted(self.device_distribute.items(), key=lambda d:d[1], reverse=True)

        self.device_distribute= dict((x, y) for x, y in data[-20:])    # 保存前十的数据
        print(self.device_distribute)
    
    def store_data(self):
        """ 获取当日设备分布
        Returns: TODO

        """
        api_count_json = json.dumps(self.api_count)
        ip_count_json = json.dumps(self.ip_count)
        every_hour_json = json.dumps(self.every_hour_count)
        device_distribute_json = json.dumps(self.device_distribute)
        d = dict(date=self.date, 
                 api = api_count_json,
                 ip = ip_count_json,
                 every_hour = every_hour_json,
                 device = device_distribute_json)
        
        cur.execute(INSERT_STR, d)
        conn.commit()