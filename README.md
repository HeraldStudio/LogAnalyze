# 小猴阿里云nginx日志分析

## 请手动创建配置文件及脚本

```bash
cp config.py.example config.py
cp SendMail.sh.example SendMail.sh
```

## crontab配置

```crontab
# m h  dom mon dow   command

# 每天凌晨2点进行数据统计
0 2 * * *  cd  <You Path> && ./StartAnalyze.sh     # 请自行修改路径

# 每天凌晨3点发送邮件
0 3 * * *  cd  <You Path> && ./SendMail.sh         # 请自行修改路径
```
## 项目日志记录方式

> 此项目中, 将logging打印出的日志与print打印出的信息分开来
> logging 输出文件用于邮件发送后端管理员用户(错误信息较为简略)
> print 标准输出用于将所得问题日志记录(错误信息完整)


## 声明

本程序仅供参考, 只提供小猴偷米数据分析, 请勿进行其他非法操作
