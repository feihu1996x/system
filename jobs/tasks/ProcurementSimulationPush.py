#!/usr/bin/python3

"""
@file: ProcurementSimulationPush.py
@brief: 政采项目模拟推送
@author: feihu1996.cn
@date: 18-09-26
@version: 1.0
"""

import sys
import time

from lxml import etree
from selenium import webdriver

from application import app, db
from common.models.procurement.Procurement import Procurement


class JobTask():
    """
    python manager.py runjob -m ProcurementSimulationPush
    政采项目模拟推送
    """
    def __init__(self):          
        app.config.from_pyfile( 'config/procurement_simulation_push_setting.py' )
        self.interval = app.config['INTERVAL']

        self.browser = webdriver.Chrome()  # 打开浏览器
        self.browser.get( "http://www.baozizhuli.com/" )  # 访问孢子科技
        if "Y" != input('请扫码进入登录状态, 确认后输入"Y"以继续：'):
            sys.exit( 1 )

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
        定时执行任务
        """
        while True:
            time.sleep( self.interval )
            self.task()
            time.sleep( self.interval )

    def task( self ):
        """
        执行任务
        """
        app.logger.info( "launching %s ..." % ( __name__ ) )

        print( "政采项目模拟推送" )

        app.logger.info( "finished %s" % ( __name__ ) )
