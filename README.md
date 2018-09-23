system
=====================

## 环境要求
### windows：32位QQ(v8.9.6.22427) + 32位Python(v3.6) + Adobe Flash Player
### Linux：

## 实时获取鼠标坐标py脚本
import time;import pyautogui;time.sleep(10);print(pyautogui.position())

```bash

# 安装依赖（for windows）
pip install -r requirements.txt

# 安装依赖（for linux）
pip install -r requirements.linux.txt

# 初始化数据库
mysql -uroot -p qq_group_spider < qq_group_spider.sql

# 启动 开发服务器
python manager.py runserver

# 启动 生产服务器
python server.py

#  将一次过滤初始化关键词导入数据库
python manager.py runjob -m ImportFilterKeys

# 执行自动导出QQ群消息记录任务脚本
python manager.py runjob -m spiders/messages/AutoExportGroupMsgs

# 执行自动获取QQ群信息任务脚本
python manager.py runjob -m spiders/messages/AutoGetGroupInfo

```

## TODO

- GUI自动化控制的坑比较多，耽误时间比较多，后面需要抽时间深入学习Pyautogui和Pywinauto两个模块
- 目前QQ群消息记录保存在MySQL，随着后续抓取的QQ群消息记录越来越多，后台会扛不住，可能需要搭建Hadoop集群，将mysql中的数据迁移到Hive中
- QQ群号码需要再编写一个脚本才能获取
- 重写app.logger日志模块
- 通过增加请求拦截器，一方面可以实现统一错误处理，另一方面可以实现API权限控制并从中获取当前登录用户的信息(cookie或者json web token)
- 消息抓取和写入数据库同步进行很耗时，可以改成异步的（借助redis）
