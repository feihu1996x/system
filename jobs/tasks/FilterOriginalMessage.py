#!/usr/bin/python3

"""
@file: FilterOriginalMessage.py
@brief: 过滤原始消息记录：
    当QQ/微信群爬虫在本地运行时，需要将爬取到的原始消息推送到服务器，此时服务器应执行此脚本过滤原始消息更新消息表
@author: feihu1996.cn
@date: 18-10-08
@version: 1.0
"""

import time

import requests

from application import app, db
from common.libs.messages.MessagesService import MessagesService


class JobTask():
    """
    python manager.py runjob -m FilterOriginalMessage
    过滤原始消息记录
    """
    def __init__(self):          
        app.config.from_pyfile( 'config/procurement_simulation_push_setting.py' )
        self.interval = app.config['INTERVAL']

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
            self.task()
            time.sleep( self.interval )

    def task( self ):
        """
        执行任务
        """
        app.logger.info( "launching %s ..." % ( __name__ ) )

        # 一次过滤，first_filter_keys表， 并保存到数据库（messages表），调用公共方法
        app.logger.info( "正在根据关键词过滤原始消息记录表..." )
        MessagesService.filter_by_keys()

        # 二次过滤，second_filter_qqnumber表、second_filter_groupnumber表， 并保存到数据库（messages表），调用公共方法
        app.logger.info( "根据给定的QQ群号码或者QQ号过滤消息记录表" )
        MessagesService.filter_by_numbers()            

        app.logger.info( "finished %s" % ( __name__ ) )
