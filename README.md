QQ群爬虫项目
=====================

## 环境要求
### windows：32位QQ(v8.9.6) + 32位Python(v3.6)
### Linux：

## 实时获取鼠标坐标py脚本
import time;import pyautogui;time.sleep(10);print(pyautogui.position())

```bash

# 安装依赖
pip install -r requirements.txt

# 启动 web server
python manager.py runserver

# 执行自动导出QQ群消息记录任务脚本
python manager.py runjob -m AutoExportGroupMsgs

# 执行自动获取QQ群信息任务脚本
python manager.py runjob -m AutoGetGroupInfo

```

## TODO

- GUI自动化控制的坑比较多，耽误时间比较多，后面需要抽时间深入学习Pyautogui和Pywinauto两个模块
- 目前QQ群消息记录保存在MySQL，随着后续抓取的QQ群消息记录越来越多，后台会扛不住，可能需要搭建Hadoop集群，将mysql中的数据迁移到Hive中
- QQ群号码需要再编写一个脚本才能获取
- 消息抓取和写入数据库同步进行很耗时，可以改成异步的
- 依赖文件可以区分为Linux和Windows版本的
- 可以重写app.logger日志模块
- 需要增加请求中间件