#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
 Create On: October 27, 2016
    Author: corvo
"""

import re
import time

# POST /api/pe HTTP/1.1\
# "GET /herald/api/v1/huodong/get HTTP/1.1"
apiP = r"(.*(POST|GET)\ /(api|uc)/(?P<api>.*)\ HTTP.*)|" \
        "(.*(?P<huodong>huodong))"

# Android
#
# "okhttp/3.1.2" (之后会换掉)
# "7.1:Pixel XL:25"  获取android版本及手机型号
#
# IOS难的令人发指
#
# "xiao hou tou mi/com.heraldstudio.ios (50; OS Version 9.3.5 (Build 13G36))"
# "Herald/3.4 (iPhone; iOS 9.3.2; Scale/2.00)"
deviceP = r"(?P<android>.*okhttp.*)|"  \
          r"((?P<android_version>.*):.*:.*)|" \
          r"(((.*\ iOS\ )|(.*OS\ Version\ ))(?P<ios_version>.*)((\ \(Build.*)|(;\ Scale.*)))|"\
          r"(?P<ios>.*iOS.*)|" \
          r"((?P<chrome>).*Chrome.*)|" \
          r"((?P<mozilla>).*Mozilla.*)|" \
          r"(?P<all>.*)"

# 将uuid提出
#1. uuid=509d5e28ca9a583d47d4a78f45acebf252160779        uuid 为40位长
#
#2. name=\x22uuid\x22\x0D\x0A\x0D\x0Adba4f9dbc2c2340e345eab91b1068595f1a80a57\x0D\x0A
# ------WebKitFormBoundaryaYJq41RbvRjBX8yu--\x0D\x0A
# 在尚未开始进行时, 其中的'\'在内存中为'\\', 测试时请额外注意
# 正则表达式思路: 将\x22替换为=, 再将参数中的\0D\0A替换为空格
uuidP = r"(.*)uuid=(?P<uuid>.{40})(\&*.*)|(.*user.*)" 

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
        parm = parm.replace('\\x22',"=")
        parm = parm.replace('\\x0D\\x0A', "")
        device = device.replace('\\x22', "")
        device = device.replace('"', "")

        matchs = (apiPattern.match(api))   #匹配api接口
        if matchs != None:
            if matchs.group('api') != None:
                self.api = matchs.group('api')
                if len(self.api) > 18:
                    print("The api is %s" % self.api)
                    self.api = 'error'
            elif matchs.group('huodong')!= None:
                self.api = 'huodong'
                
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

        # 如果是在调用api, 则对uuid进行记录, 还有ip
        if self.api != 'auth' and self.api != 'update' and self.api != 'huodong':
            matchs = (uuidPattern.match(parm))
            if matchs != None:
                if matchs.group('uuid') != None:
                    self.uuid= matchs.group('uuid')
            else:
                if parm == '\"-\"':             # 未知参数, 仅在print标准输出中记录
                    print("%d:%d uid-error in api %s, ip %s,  parm %s, device %s" \
                          % (time.tm_hour, time.tm_min, api, ip, parm, device))
                else:
                    print("%d:%d uid-error in api %s, ip %s,  parm %s, device %s" \
                          % (time.tm_hour, time.tm_min, api, ip, parm, device))

                    # logging 简略信息
                    #logging.error("%d:%d uid-error in api %s, device %s" \
                    #              % (time.tm_hour, time.tm_min, api, device))

                self.parm = parm
        else:
            self.parm = parm

        matchs = (devicePattern.match(device))          # 匹配设备信息
        if matchs != None:  
            if matchs.group('android') != None:         # android 设备
                self.device = 'android'
            elif matchs.group('android_version') != None:
                self.device = 'android'
                self.android_version = matchs.group('android_version')
            elif matchs.group('ios_version') != None or matchs.group('ios'): # ios 设备
                self.device = 'ios'
                self.ios_version = matchs.group('ios_version')
            elif matchs.group('chrome') != None or matchs.group('mozilla') != None:  # web 设备
                self.device = 'web'
            elif matchs.group('all') == '\"-\"':            # 未知设备, 在标准输出中记录, 不在logging中记录
                self.device = '-'
                # print 详细信息
                print("%d:%d dev-error in api %s, parm %s, device %s" \
                    % (time.tm_hour, time.tm_min, api, parm, device)) 
            elif matchs.group('all') != None:          
                self.device = 'other'
                # print 详细信息
                print("%d:%d dev-error in api %s, parm %s, device %s" \
                    % (time.tm_hour, time.tm_min, api, parm, device))

                # logging 简略信息
                #logging.error("%d:%d dev-error in api %s, device %s" \
                #    % (time.tm_hour, time.tm_min, api, device))

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
        "GET /herald/api/v1/huodong/get HTTP/1.1",
        "7.1:Pixel XL:25",
     "------WebKitFormBoundarygflshEy0ij6cJAld\\x0d\\x0AContent-Disposition: form-data; name=\\x22uuid\\x22\\x0D\\x0A\\x0D\\x0Adba4f9dbc2c2340e345eab91b1068595f1a80a57\x0D\x0A------WebKitFormBoundarygflshEy0ij6cJAld--\x0D\x0A",
        '200'
            ) 

    print(logItem.device)
    print(logItem.api)
    #print(logItem.parm)
    print("The uuid is %s " % logItem.uuid)
    print(logItem.ios_version)
    print(logItem.android_version)

if __name__ == "__main__":
    main()
