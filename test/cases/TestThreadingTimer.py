#!/usr/bin/python3

"""
@file: TestThreadingTimer.py
@brief: 测试线程定时器
@author: feihu1996.cn
@date: 18-09-24
@version: 1.0
"""

from threading import Timer

from application import app


class TestCase():
    """
    python manager.py runtest -m TestThreadingTimer
    测试用例
    """
    def __init__( self ):
        pass

    def run( self, params ):
        app.logger.info( 'executing %s' % ( __name__ ) )

        self.__printHello()

        import time
        time.sleep(10)
        print( "非阻塞的Timer" )

        app.logger.info( "finished %s" % ( __name__ ) )

    def __printHello( self ):
        """
        每3秒打印一次Hello, World
        """
        print( "Hello, World" )
        Timer( 2, self.__printHello).start()
        return 
