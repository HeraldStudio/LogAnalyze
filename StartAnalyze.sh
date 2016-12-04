#/bin/sh

# 将操作重定向到test.log文件中, 文件已被加入gitignore
python3 main.py &>> test.log
