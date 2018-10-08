#!/usr/bin/python3

"""
@file: OriginalMessageSimulationPush.py
@brief: 原始消息记录模拟推送:
    当在本地运行QQ、微信群爬虫时，
    需要单独运行此脚本将爬取到的原始消息记录推送到服务器
@author: feihu1996.cn
@date: 18-10-08
@version: 1.0
"""

import json
import time
import traceback

import requests

from application import app, db
from common.models.messages.OriginalMessages import OriginalMessage


class JobTask():
    """
    python manager.py runjob -m OriginalMessageSimulationPush
    原始消息记录模拟推送
    """
    def __init__(self):          
        app.config.from_pyfile( 'config/original_message_simulation_push_setting.py' )
        self.interval = app.config['INTERVAL']
        self.push_url = app.config['PUSH_URL']
        self.headers = {
            'Content-Type': 'application/json'
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

        original_message_model_list = OriginalMessage.query.all()

        app.logger.info( "当前原始消息记录数量为:%d" %( len( original_message_model_list ) ) )

        params_dict = {
            "original_message_list": []
        }
        for original_message_model in original_message_model_list:
            params_dict["original_message_list"].append({  # 构造post请求参数
                "group_id": original_message_model.group_id,
                "sender_name": original_message_model.sender_name,
                "qq_number": original_message_model.qq_number,
                "content": original_message_model.content,
                "send_time": str( original_message_model.send_time ),
                "fingerprint": original_message_model.fingerprint
            })

        app.logger.info( params_dict )
        app.logger.info( "正在推送原始消息记录" )
        response = requests.post( self.push_url, headers=self.headers, data=json.dumps( params_dict ) )  # 推送原始消息记录
        app.logger.info( response.json() )
        app.logger.info( response.status_code )
        if 200 == response.status_code:
            app.logger.info( "数据推送成功，共成功推送了%d条" %( len( response.json()["data"] ) ) )
            for success_pushed_message in response.json()["data"]:
                original_message_model = OriginalMessage.query.filter_by( fingerprint=success_pushed_message['fingerprint'] ).first()
                app.logger.info( "正在删除本地记录:%s" %( original_message_model.fingerprint ) )
                db.session.delete( original_message_model )
                db.session.commit()

        app.logger.info( "finished %s" % ( __name__ ) )
