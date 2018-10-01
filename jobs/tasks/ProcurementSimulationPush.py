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
import requests
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
        self.push_url = app.config['PUSH_URL']
        self.headers = {  # 请求头部
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

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

        procurement_model_list = Procurement.query.filter( Procurement.posted != 1 ).all()  # 未推送或推送失败的政采项目model列表

        app.logger.info( "政采项目model列表总长度为：%d" % ( len( procurement_model_list ) ) )
        
        for procurement_model in procurement_model_list:  # 遍历政采项目model列表
            params_dict = {
                'title': procurement_model.name[0:29],
                'description': ( procurement_model.publish_time + ' ' + procurement_model.desc )[0:1999],
                'spider_url': procurement_model.source,
                'delivery_way': 'qq',
                'budget': 1,
                'cate_id': 1,
                'tag_id': 100,
                'delivery_time': '2018-10-30',
                'user_id': 2,
                'contact_way': 'qq',
            }
            app.logger.info( params_dict )
            # """  # TODO
            push_response = requests.post( self.push_url, headers=self.headers, data=params_dict )
            if 0 != push_response.json()['code']:
                app.logger.info( "项目推送失败" )
                app.logger.info( push_response.json() )
                procurement_model.posted = -1
                db.session.add( procurement_model )
                db.session.commit()
            else:
                app.logger.info( "项目推送成功" )
                app.logger.info( push_response.json() )
                procurement_model.posted = 1
                db.session.add( procurement_model )
                db.session.commit()  
            # """  # TODO

            # break # TODO         

        app.logger.info( "finished %s" % ( __name__ ) )
