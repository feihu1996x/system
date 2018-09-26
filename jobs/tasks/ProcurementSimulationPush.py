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
        self.push_url = 'http://m.dev.baozizhuli.com/api/requirement/issue'  # 接口地址

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

        procurement_model_list = Procurement.query.filter( Procurement.posted != 1 ).all()  # 未推送或推送失败的政采项目model列表

        app.logger.info( "政采项目model列表总长度为：%d" % ( len( procurement_model_list ) ) )
        for procurement_model in procurement_model_list:  # 遍历政采项目model列表
            # TODO: 填充请求参数，调用孢子推送接口
            params = {
                'title': "", # str_title[0:50] 
                'delivery_way': "",
                'description': "",
                'budget': '',
                'cate_id': '',
                'tag_id': '',
                'delivery_time': '',
                'user_id': 2,
                'contact_way': '',
                'spider_url': '' 
            }
        app.logger.info( "finished %s" % ( __name__ ) )
