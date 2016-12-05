#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
 Create On: October 27, 2016
    Author: corvo
"""

import re

#POST /api/pe HTTP/1.1\
apiP = r".*(POST|GET)\ /(api|uc)/(?P<api>.*)\ HTTP.*"

# "okhttp/3.1.2" 
# "xiao hou tou mi/com.heraldstudio.ios (50; OS Version 9.3.5 (Build 13G36))"
# ""
#deviceP = r"((okhttp.*)|(xiao\ hou\ tou\ mi\/com.heraldstudio.ios))"
deviceP = r"(?P<android>.*okhttp.*)|(.*xiao.*(?P<ios_version>OS\ Version.*)\ \(Build.*\))|(?P<ios>.*IOS.*)|(?P<all>.*)"

# uuid=509d5e28ca9a583d47d4a78f45acebf252160779        uuid 为40位长
uuidP = r"(.*)uuid=(?P<uuid>.{40})(\&*.*)|(.*user.*)"   # 将uuid提出

apiPattern = re.compile(apiP)
devicePattern = re.compile(deviceP)
uuidPattern = re.compile(uuidP)

class LogItem():
    """日志中每一条记录"""
    time            = None # 请求时间
    ip              = ""   # 请求IP
    api             = ""   # 请求API
    device          = ""   # 请求终端设备
    parm            = ""   # 请求参数
    code            = ""   # 返回码
    uuid            = ""   # 用户uuid
    ios_version     = ""   # ios 版本
    android_version = ""   # android 版本

    def __init__(self, time, ip, api, device, parm, code):
        self.time = time
        self.ip = ip
        self.api = api
        matchs = (apiPattern.match(self.api))   #匹配api接口

        if matchs != None:  
            self.api = matchs.group('api')  
        else:
            self.api = 'error'
            print(api)
            print("error in api" + parm) 
            
        if self.api != 'auth' or self.api != 'update':
            matchs = (uuidPattern.match(parm))
            if matchs != None:
                self.parm = matchs.group('uuid')
            else:
                print('error in par ' + parm)
                self.parm = parm
        else:
            self.parm = parm

        matchs = (devicePattern.match(device))
        if matchs != None:  
            if matchs.group('android') != None:
                self.device = 'android'
            elif matchs.group('ios_version') != None or matchs.group('ios'):
                self.device = 'ios'
                self.ios_version = matchs.group(3)
            elif matchs.group('all') != None:
                self.device = 'other'
            else:
                print('error')
                exit()
        else:
            if device == '\"-\"':
                self.device = 'empty_room'
            else:
                print("error") 
                print(device)
                exit()
        self.code = code
