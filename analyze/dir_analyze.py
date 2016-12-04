#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
 Create On: November 01, 2016
    Author: corvo
"""
import os
import re
from main import logging, session
from databases.tables import DayLogAnalyze
from analyze.util import parse_file
from analyze.day_log import DayLog

#  我们的日志文件名称 access_api.log-20160921
fileP = 'access_api.log-(?P<date>\d*)'   # date别名为日志的时间尾巴, 例如20160921

# 日志文件名称, date为时间
logFilePattern = re.compile(fileP) 

def process_dir(dir_proc):
    """ 解析某个目录中的所有日志文件并保存在数据库中

    Args:
        dir_proc: 日志文件目录

    Returns: TODO

    """
    for file in os.listdir(dir_proc):
        if os.path.isdir(os.path.join(dir_proc, file)):
            logging.warning("%s is a directory" % file)
            continue
        
        matchs = logFilePattern.match(file)
        if matchs != None and matchs.group(0) != 'access_api.log-20160921':
            logging.info("process file %s, file date is %s" %(file, matchs.group('date'))) 
            process_every_file(os.path.join(dir_proc, file), matchs.group('date'))
        
        
        
def process_every_file(_file_path, _date):
    """TODO: Docstring for process_file.

    Args:
        file_path: 文件路径
        date     : 日志文件日期

    Returns: TODO

    """
    old = session.query(DayLogAnalyze).filter(DayLogAnalyze.date == _date).all()

    if old:
        logging.warning("current date has been analyzed")
        return 

    dayLog = DayLog(_date)
    parse_file(dayLog, _file_path)
    dayLog.get_every_hour_called()
    dayLog.get_most_ip()
    dayLog.get_most_called()
    dayLog.get_device_called()
    dayLog.get_ios_version()
    dayLog.get_android_version()
    
    dayLog.store_data()
