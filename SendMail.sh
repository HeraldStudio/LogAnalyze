#!/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

source /etc/profile

mail -s 'HeraldStido日志'  \
    corvofeng@163.com   \
    corvofeng@gmail.com   \
    < py.log

