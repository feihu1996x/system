system
=====================

## 环境要求

### Windows：
- 32位QQ(v8.9.6.22427) 
- 32位Python(v3.6) 
- chromedriver_win32(v70.0.3538.16, http://chromedriver.storage.googleapis.com/70.0.3538.16/chromedriver_win32.zip, 安装路径需要添加到PATH中) 
- 64位Google Chrome(v69.0.3497.100)
- JDK 1.8.0_181 x64
- Android SDK
- 夜神安卓模拟器（ v6.0.7.5 ）
- Android v5.1.1
- 微信app（v6.6.7）
- Node.js( v8.12.0 )
- Appium( V1.9.1 )
- appium-desktop( v1.7.1 )
- appium-doctor( v1.5.0 )

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

# 执行自动导出QQ群消息记录任务脚本(可在配置文件中配置定时执行周期)
python manager.py runjob -m spiders/messages/AutoExportGroupMsgs

# 执行自动获取QQ群信息任务脚本
python manager.py runjob -m spiders/messages/AutoGetGroupInfo

# 数据库初始化：插入采购领域及其对应的关键词
python manager.py runjob -m ImportProcurementField

# 爬取中国政府采购网公开招标项目信息(可在配置文件中配置定时执行周期)
python manager.py runjob -m spiders/procurement/guojia/GuojiaPublic

# 爬取中国政府采购网询价公告项目信息(可在配置文件中配置定时执行周期)
python manager.py runjob -m spiders/procurement/guojia/GuojiaEnquiry

# 政采项目模拟推送(可在配置文件中配置定时执行周期)
python manager.py runjob -m ProcurementSimulationPush

# 自动抓取微信群消息(可在配置文件中配置定时执行周期)
python manager.py runjob -m spiders/messages/AutoExportWeChatMsgs

# 过滤原始消息记录(可在配置文件中配置定时执行周期)
python manager.py runjob -m FilterOriginalMessage

# 原始消息记录模拟推送
python manager.py runjob -m OriginalMessageSimulationPush

# 启动 开发服务器
python manager.py runserver

# 启动 生产服务器（only for linux）
python server.py
```

## Demo Link
[http://dev.feihu1996.cn/qqGroupNeeds/](http://dev.feihu1996.cn/qqGroupNeeds/ "system")