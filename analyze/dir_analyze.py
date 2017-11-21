#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
 Create On: November 01, 2016
    Author: corvo
"""
import os
import re

from config import logging
from databases.tables import DayLogAnalyze
from analyze.util import parse_file
from analyze.day_log import DayLog, session

#  我们的日志文件名称 access_api.log-20160921.gz
fileP = r'access_api.log-(?P<date>\d*).gz'   # date别名为日志的时间尾巴, 例如20160921

# 日志文件名称, date为时间
logFilePattern = re.compile(fileP)

# 每天晚上最多执行3天的日志分析
max_analyze = 3


def process_dir(dir_proc):
    """ 解析某个目录中的所有日志文件并保存在数据库中

    Args:
        dir_proc: 日志文件目录

    Returns: TODO

    """
    #add_head()
    for file in os.listdir(dir_proc):
        if os.path.isdir(os.path.join(dir_proc, file)):
            print("%s is a directory" % file)
            continue

        matchs = logFilePattern.match(file)
        if matchs is not None:
            process_every_file(os.path.join(dir_proc, file), matchs.group('date'))



def process_every_file(_file_path, _date):
    """ 处理每个文件

    Args:
        file_path: 文件路径
        date     : 日志文件日期, 如果 date=='tmp', 则表明是临时测试使用

    """

    old = session.query(DayLogAnalyze).filter(DayLogAnalyze.date == _date).all()
    print("current file is " + _file_path)

    # 查询数据库, 如果当前日期对应的日志已被解析, 则直接进行返回
    if old:
        # print("current date has been analyzed")
        return

    global max_analyze      # 全局变量, 在main.py中定义
    max_analyze -= 1
    if max_analyze == 0:
        return

    logging.info("current file is " + _file_path)
    dayLog = DayLog(_date)
    parse_file(dayLog, _file_path)

    dayLog.create_logging_header()
    dayLog.get_every_hour_called()
    dayLog.get_most_ip()
    dayLog.get_most_called()
    dayLog.get_device_called()
    dayLog.get_ios_version()
    dayLog.get_android_version()

    dayLog.create_logging()
    add_sign()
    if _date == 'tmp':      # 临时检验的文件不保存到数据库, 只做分析使用
        print(dayLog.date)
        print(dayLog.api_count)
        print(dayLog.ip_count)
        print(dayLog.every_hour_count)
        print(dayLog.device_distribute)
        print(dayLog.ios_version)
        return

    dayLog.store_data()


def add_head():
    """ 为邮件添加头部信息
    """
    logging.info("From: heraldstudio < heraldstudio@sina.com >")
    logging.info("Subject: 小猴偷米日志记录")
    logging.info("")
    logging.info("邮件为自动生成, 请勿回复")
    logging.info("")


def add_sign():
    """ 邮件末尾签名
    """
    logging.info("")
    logging.info("")
    logging.info("")
    logging.info("---------------------------------------------------------")
    logging.info("愿天下有情人, 我喜欢的人, 都是你这个样")
