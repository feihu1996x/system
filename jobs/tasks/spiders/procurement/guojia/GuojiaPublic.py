#!/usr/bin/python3

"""
@file: GuojiaPublic.py
@brief: 中国政府采购网 公开招标 项目信息爬取
@author: feihu1996.cn
@date: 18-09-17
@version: 1.0
"""

from application import app, db

class JobTask():
    """
    python manager.py runjob -m spiders/procurement/guojia/GuojiaPublic
    中国政府采购网 公开招标 项目信息爬取
    """
    def __init__(self):  
        app.config.from_pyfile( 'config/guojia_public_setting.py' )
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
        定时执行task
        """
        while True:
            time.sleep( self.interval )
            self.task()
            time.sleep( self.interval )

    def task( self ):
        """
        爬取中国政府采购网公开招标项目信息
        """
        app.logger.info( "launching %s ..." % ( __name__ ) )

        print( "爬取中国政府采购网公开招标项目信息" )

        app.logger.info( "finished %s" % ( __name__ ) )
        