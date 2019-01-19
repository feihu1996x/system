# 定时执行间隔，单位是秒，若值为0，则表示一次性执行完
INTERVAL = 0

# Appium会话配置
DESIREED_CAPABILITY = {
    "platformName": "Android",
    "platformVersion": "4.4.2",
    "deviceName": "127.0.0.1:62001",
    "appPackage": "com.tencent.mm",
    "appActivity": "com.tencent.mm.ui.LauncherUI",
    "noReset": True,  # 在当前session下不要重置应用的状态
    "unicodeKeyboard": True,
    "resetKeyboard": True
}

# Appium Server
APPIUM_SERVER = "http://localhost:4723/wd/hub"

# 元素显式等待超时时间，单位是秒
TIMEOUT = 60
