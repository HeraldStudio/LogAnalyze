#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
 Create On: October 27, 2016
    Author: corvo
"""

import re
import time

#POST /api/pe HTTP/1.1\
apiP = r".*(POST|GET)\ /(api|uc)/(?P<api>.*)\ HTTP.*"

# Android
#
# "okhttp/3.1.2" 
# IOS难的令人发指
#
# "xiao hou tou mi/com.heraldstudio.ios (50; OS Version 9.3.5 (Build 13G36))"
# "Herald/3.4 (iPhone; iOS 9.3.2; Scale/2.00)"
deviceP = r"(?P<android>.*okhttp.*)|"  \
           "(((.*\ iOS\ )|(.*Version\ ))(?P<ios_version>.*)(\ \(Build.*|;\ Scale.*))|"\
           "(?P<ios>.*iOS.*)|"\
           "(?P<all>.*)"

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
        """ 初始化函数中, 因为有过多的错误需要处理, 
            需要认真阅读日志文件不断进行优化

        """
        self.time = time
        self.ip = ip

        matchs = (apiPattern.match(api))   #匹配api接口
        if matchs != None:  
            self.api = matchs.group('api')  
        else:
            self.api = 'error'
            # Api error
            print("%d:%d api-error in api %s, parm %s, device %s" \
                    % (time.tm_hour, time.tm_min, api, parm, device)) 

        # 空教室端口仅使用本服务器转发数据, 故而直接返回
        if self.api == 'emptyroom':
            self.device = 'web'
            self.uuid = '0'
            self.code = 'code'
            return

        # 如果是在调用api, 则对uuid进行记录, 暂时uuid不进行使用
        if self.api != 'auth' or self.api != 'update':    
            matchs = (uuidPattern.match(parm))
            if matchs != None:
                self.parm = matchs.group('uuid')
            else:
                print("%d:%d uid-error in api %s, parm %s, device %s" \
                    % (time.tm_hour, time.tm_min, api, parm, device)) 
                self.parm = parm
        else:
            self.parm = parm
            
        matchs = (devicePattern.match(device))          # 匹配设备信息
        if matchs != None:  
            if matchs.group('android') != None:
                self.device = 'android'
            elif matchs.group('ios_version') != None or matchs.group('ios'):
                self.device = 'ios'
                self.ios_version = matchs.group('ios_version')
            elif matchs.group('all') != None:
                self.device = 'other'
                print("%d:%d dev-error in api %s, parm %s, device %s" \
                    % (time.tm_hour, time.tm_min, api, parm, device)) 
            else:
                print("%d:%d dev-error in api %s, parm %s, device %s" \
                    % (time.tm_hour, time.tm_min, api, parm, device)) 
        else:
            if device == '\"-\"':
                self.device = 'empty_room'
            else:
                print("%d:%d dev-error in api %s, parm %s, device %s" \
                    % (time.tm_hour, time.tm_min, api, parm, device)) 
                exit()

        self.code = code

def main():
    """ 
    测试主函数, 遇到有问题的log时, 将数据取出并在此进行测试
    """
    logItem = LogItem(
        time.localtime(), 
        '203.208.60.230',
        'POST /api/card HTTP/1.1', 
        'Herald/3.4 (iPhone; iOS 9.3.2; Scale/2.00)',
        '"uuid=7e0064c27402554da094aee6c9761a45c2979103&timedelta=1"',
        '200')

    logItem = LogItem(
        time.localtime(), 
        '203.208.60.230',
        'POST /api/card HTTP/1.1', 
     "xiao hou tou mi/com.heraldstudio.ios (50; OS Version 9.3.5 (Build 13G36))",
        '"uuid=7e0064c27402554da094aee6c9761a45c2979103&timedelta=1"',
        '200'
            ) 

    print(logItem.device)
    print(logItem.api)
    print(logItem.parm)
    print(logItem.ios_version)
    print(logItem.android_version)

if __name__ == "__main__":
    main()
