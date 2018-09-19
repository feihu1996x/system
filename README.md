QQ群爬虫项目
=====================

```

# 环境要求
# 32位QQ(v8.9.6)
# 32位Python(v3.6)
# 64位Windows
# QQ应当禁用来消息时自动弹出窗口

# 实时获取鼠标坐标py脚本
import time;import pyautogui;time.sleep(10);print(pyautogui.position())

# 安装依赖
pip install -r requirements.txt

# 启动 web server
python manager.py runserver

# 执行自动导出QQ群消息记录任务脚本
python manager.py runjob -m AutoExportGroupMsgs

```
