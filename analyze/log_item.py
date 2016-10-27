#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
 Create On: October 27, 2016
    Author: corvo
"""

class LogItem():
    """日志中每一条记录"""
    time   = None # 请求时间
    ip     = ""   # 请求IP
    api    = ""   # 请求API
    device = ""   # 请求终端设备
    parm   = ""   # 请求参数
    code   = ""   # 返回码
    

    def __init__(self, time, ip, api, device, parm, code):
        self.time = time
        self.ip = ip
        self.api = api
        self.device = device
        self.parm = parm
        self.code = code

