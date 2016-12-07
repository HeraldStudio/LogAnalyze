#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
 Create On: October 27, 2016
    Author: corvo
"""

from config import logging
import fileinput
import re
import os
import time
from analyze.log_item import LogItem
import gzip

#使用的nginx日志格式 如下 
# log_format access  '$remote_addr [$time_local] "$request" $status "$request_body" "$http_user_agent"';
#日志分析正则表达式  

#  我们的日志文件名称 access_api.log-20160921
fileP = '.*\.log-(?P<date>\d*)'   # date别名为日志的时间尾巴, 例如20160921

#203.208.60.230   
ipP = r"?P<ip>[\d.]*";  
  
#[21/Jan/2011:15:04:41 +0800]  
timeP = r"""?P<time>\[           #以[开始 
            [^\[\]]* # 除[]以外的任意字符  防止匹配上下个[]项目(也可以使用非贪婪匹配*?)  
                     # 不在中括号里的.可以匹配换行外的任意字符  
                     #  *这样地重复是"贪婪的“ 表达式引擎会试着重复尽可能多的次数。 
            \]       #以]结束 
        """  

#"GET /EntpShop.do?method=view&shop_id=391796 HTTP/1.1"  
requestP = r"""?P<request>\"          #以"开始 
            [^\"]* #除双引号以外的任意字符 防止匹配上下个""项目(也可以使用非贪婪匹配*?) 
            \"          #以"结束 
            """  

statusP = r"?P<status>\d+"  

bodyBytesSentP = r"?P<bodyByteSent>\d+"  

#"http://test.myweb.com/myAction.do?method=view&mod_id=&id=1346"  
referP = r"""?P<refer>\"          #以"开始 
            [^\"]* #除双引号以外的任意字符 防止匹配上下个""项目(也可以使用非贪婪匹配*?) 
            \"          #以"结束 
        """  

#"Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"'  
userAgentP = r"""?P<userAgent>\"              #以"开始 
        [^\"]* #除双引号以外的任意字符 防止匹配上下个""项目(也可以使用非贪婪匹配*?) 
        \"              #以"结束 
            """  

#原理: 主要通过空格和-来区分各不同项目，各项目内部写各自的匹配表达式, 更换日志格式请重新生成该串
nginxLogPattern =       \
        re.compile(r"(%s)\ (%s)\ (%s)\ (%s)\ (%s)\ (%s)" %  \
                   (ipP, timeP, requestP, statusP, referP, userAgentP), re.VERBOSE)  

# 解析时间 '[20/Sep/2016:07:49:11 +0800]'
timeAnalyzePattern = '[%d/%b/%Y:%H:%M:%S %z]' 

# 日志文件名称, date为时间
logFilePattern = re.compile(fileP)  

def parse_file(dayLog, file):
    """解析传入的文件

    Args:
        dayLog: 日志集合对象
        file: 文件名称, 相对地址或绝对地址

    Returns: TODO

    """
    matchs = logFilePattern.match(file)
    logging.info("process file %s." % (file)) 

    f_in = gzip.open(os.path.join(file), "rb")
    for line in f_in:
        line = bytes.decode(line)  
        matchs = nginxLogPattern.match(line)  
        if matchs != None:  
            ip = matchs.group("ip")
            time = processTime(matchs.group("time"), timeAnalyzePattern) # 解析时间
            request = matchs.group("request")  
            status =  matchs.group("status")
            refer = matchs.group("refer")
            userAgent = matchs.group("userAgent")  

            logItem = LogItem(time, ip, request, userAgent, refer, status) 
            dayLog.add_log_item(logItem)                                # 向对象中添加元素

        else:  
            raise Exception  
              
    fileinput.close()
    
def processDir(dir_proc):  
    """传入文件夹, 从中筛选日志记录, 并进行读取 

    Args:
        dir_proc: 需要处理的日志文件夹

    Returns: TODO

    """

    for file in os.listdir(dir_proc):  
        if os.path.isdir(os.path.join(dir_proc, file)):  
            logging.warning("%s is a directory" %(file))
            processDir(os.path.join(dir_proc, file))  
            continue  
    
        matchs = logFilePattern.match(file)
        if matchs == None:
            logging.warning("%s is not a log file" %(file))
            continue  

        logging.info("process file %s, file date is %s" %(file, matchs.group('date'))) 
        
allStatusDict = {}
#统计HTTP状态码的数量  
def GetResponseStatusCount(status):  
    if status in allStatusDict:  
        allStatusDict[status] += 1;  
    else:  
        allStatusDict[status] = 1;  


def processTime(time_str, timePattern):
    """ 通过时间字符串解析时间

    Args:
        time_str:    日期字符串 '[20/Sep/2016:07:49:11 +0800]'
        timePattern: 匹配字符串 '[%d/%b/%Y:%H:%M:%S %z]' 

    Returns: 格式化之后的时间对象
    """
    return time.strptime(time_str, timePattern)
