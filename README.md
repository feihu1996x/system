system
=====================

## 环境要求
### Windows：32位QQ(v8.9.6.22427) + 32位Python(v3.6)
### Linux：

## 实时获取鼠标坐标py脚本
import time;import pyautogui;time.sleep(10);print(pyautogui.position())

```bash

# 安装依赖（for windows）
pip install -r requirements.txt

# 安装依赖（for linux）
pip install -r requirements.linux.txt

# 初始化数据库
mysql -uroot -p system < system.sql

#  将初始化过滤关键词导入数据库
python manager.py runjob -m ImportFilterKeys

# 执行自动导出QQ群消息记录任务脚本
python manager.py runjob -m spiders/messages/AutoExportGroupMsgs

# 执行自动获取QQ群信息任务脚本
python manager.py runjob -m spiders/messages/AutoGetGroupInfo

# 启动 开发服务器
python manager.py runserver

# 启动 生产服务器（only for linux）
python server.py

```
