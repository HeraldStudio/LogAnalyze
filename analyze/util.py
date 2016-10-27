#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
 Create On: October 27, 2016
    Author: corvo
"""

def parse_file(file):
    """解析传入的文件

    Args:
        file: 文件名称, 相对地址或绝对地址

    Returns: TODO

    """
    matchs = logFilePattern.match(file)
    date = matchs.group('date')
    logging.info("process file %s, file date is %s" % \
                    (file, date))   # 解析日期 

    for line in fileinput.input(os.path.join(file)):  
        matchs = nginxLogPattern.match(line)  
        if matchs != None:  
            allGroups = matchs.groups()  
            ip = matchs.group("ip")
            time = processTime(matchs.group("time"), timeAnalyzePattern) # 解析时间
            request = matchs.group("request")  
            status =  matchs.group("status")
            refer = matchs.group("refer")
            userAgent = matchs.group("userAgent")  

#            print (ip)
#           print (time)
#           print (request)
#           print (status)
#           print (refer)
#           print (userAgent)

            #统计HTTP状态码的数量  
            GetResponseStatusCount(userAgent)  
            #在这里补充其他任何需要的分析代码  
        else:  
            raise Exception  
              
    fileinput.close()

