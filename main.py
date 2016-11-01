#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
 Create On: October 26, 2016
    Author: corvofeng@gmail.com
"""

import logging
from analyze.day_log import DayLog
from analyze.util import parse_file

# Python 日志记录
log_format = '%(filename)s [%(asctime)s] [%(levelname)s] %(message)s' 
logging.basicConfig(format=log_format, level=logging.DEBUG)
  
#日志的位置  
dir_log  = r"../"  


if __name__ == "__main__":  
    #processDir(dir_log)  
    #parse_file("../access_api.log-20160921")
    dayLog = DayLog('s');
    parse_file(dayLog, "./log.example")
    #parse_file("./log/access_api.log-20160921")

    dayLog.get_every_hour_called()
    dayLog.get_most_ip()
    dayLog.get_most_called()
    dayLog.get_device_called()
    
    dayLog.store_data()