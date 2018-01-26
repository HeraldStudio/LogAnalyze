#!/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

source /etc/profile

# 将操作重定向到test.log文件中, 文件已被加入gitignore
# 阿里云的鸡肋服务器会发生CPU 100%的问题，可以安装cpulimit进行解决，注释在这里以备不时之需
# yum install cpulimit
# cpulimit -l 50 /usr/bin/python3.4  main.py -d /var/log/nginx  &>>  test.log
cpulimit -l 50 /usr/bin/python3.4  main.py -d /var/log/nginx  &>>  test.log
