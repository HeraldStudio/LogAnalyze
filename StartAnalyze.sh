#!/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

source /etc/profile

# 将操作重定向到test.log文件中, 文件已被加入gitignore
cpulimit -l 50 /usr/bin/python3.4  main.py -d /var/log/nginx  &>>  test.log
