#!/usr/bin/python3

"""
@file: TestWeChatAuto.py
@brief: 微信自动化控制测试
@author: feihu1996.cn
@date: 18-09-28
@version: 1.0
"""

from appium import webdriver

from application import app


class TestCase():
    """
    python manager.py runtest -m TestWeChatAuto
    微信自动化控制测试
    """
    def __init__( self ):
        self.desired_capability = {  # Appium会话 capability配置
            "platformName": "Android",
            "platformVersion": "4.4.2",
            "deviceName": "127.0.0.1:62001",  # 启动模拟器，然后执行adb connect 127.0.0.1:62001
            "appPackage": "com.tencent.mm",
            "appActivity": "com.tencent.mm.ui.LauncherUI",
            "noReset": False            
        }
        self.appium_server = "http://localhost:4723/wd/hub"  # 启动Appium Server或者Appium Desktop, 启用"Allow Session Override"
        
        self.driver = webdriver.Remote( self.appium_server, self.desired_capability )  # 与Appium Server建立会话

    def run( self, params ):
        app.logger.info( 'executing %s' % ( __name__ ) )

        app.logger.info( "微信自动化控制测试" )

        app.logger.info( "finished %s" % ( __name__ ) )
        