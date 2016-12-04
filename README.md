# 小猴阿里云nginx日志分析

## 请手动创建配置文件

```bash
cp config.py.example config.py
```

## crontab配置

```crontab
# m h  dom mon dow   command

# 每天凌晨2点进行数据统计
0 2 * * *  <You Path>/StartAnalyze.sh     # 请自行修改路径
```


## 声明

本程序仅供参考, 只提供小猴偷米数据分析, 请勿进行其他非法操作
