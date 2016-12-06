#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
 Create On: October 26, 2016
    Author: corvofeng@gmail.com
"""

import logging
from analyze.util import parse_file
from databases.db import engine
from sqlalchemy.orm import sessionmaker
from getopt import getopt
import sys
from analyze import dir_analyze

Session = sessionmaker()        # 生成会话
Session.configure(bind=engine)
session = Session()

import analyze.dir_analyze 
from analyze.day_log import DayLog


# 每天晚上最多执行3天的日志分析
max_analyze = 3

# Python 日志记录
log_format = '%(filename)s [%(asctime)s] [%(levelname)s] %(message)s' 
logging.basicConfig(format=log_format, level=logging.DEBUG)
  
#日志的位置  
dir_log  = r"/var/log/nginx"

def usage():
    print("help")

if __name__ == "__main__":  
    #processDir(dir_log)  
    #parse_file("../access_api.log-20160921")

    #dayLog = DayLog('log.example')
    #parse_file(dayLog, "./log.example")
    #parse_file("./log/access_api.log-20160921")
    #dayLog.get_every_hour_called()
    #dayLog.get_most_ip()
    #dayLog.get_most_called()
    #dayLog.get_device_called()
    opts, args = getopt(sys.argv[1:], "hi:l:d:")
    for op, value in opts:
        if op == "-l":
            analyze.dir_analyze.process_every_file(value, 'tmp')
        elif op == "-d":
            analyze.dir_analyze.process_dir(value)
            session.commit()
            session.close()
        elif op == "-h":
            usage()
        else:
            usage()
    #dayLog.store_data()
    
