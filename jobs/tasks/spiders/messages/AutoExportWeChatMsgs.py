#!/usr/bin/python3

"""
@file: AutoExportWeChatMsgs.py
@brief: 自动抓取微信消息
@author: feihu1996.cn
@date: 18-09-29
@version: 1.0
"""

import time

from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from application import app, db
from common.libs.messages.MessagesService import MessagesService  


class JobTask():
    """
    python manager.py runjob -m spiders/messages/AutoExportWeChatMsgs
    自动抓取微信消息
    """
    def __init__(self):  
        app.config.from_pyfile( 'config/auto_export_wechat_msgs_setting.py' )
        self.interval = app.config['INTERVAL']
        self.desired_capability = app.config['DESIREED_CAPABILITY']
        self.appium_server = app.config['APPIUM_SERVER']
        self.timeout = app.config['TIMEOUT']
        
        app.logger.info( "正在建立Appium会话..." )
        self.driver = webdriver.Remote( self.appium_server, self.desired_capability )  # Appium会话配置

        self.wait=WebDriverWait(self.driver, self.timeout)

    def run ( self, params ):
        """
        运行任务
        """
        if self.interval: 
            app.logger.info( "定时器已开启，频率是%s秒..." %( str( self.interval ) ) ) 
            self.timer_task() 
        else:
            app.logger.info( "定时器未开启" )
            self.task()

    def timer_task( self ):
        """
        定时任务
        """
        while True:
            time.sleep( self.interval )
            self.task()
            time.sleep( self.interval )

    def task( self ):
        """
        自动抓取微信消息
        """
        app.logger.info( 'executing %s' % ( __name__ ) )

        app.logger.info( "自动抓取微信消息" )

        app.logger.info( "finished %s" % ( __name__ ) )
