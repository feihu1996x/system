#!/usr/bin/python3

"""
@file: Test.py
@brief: 测试脚本示例
@author: feihu1996.cn
@date: 18-09-24
@version: 1.0
"""

from application import app


class TestCase():
    """
    python manager.py runtest -m Test
    测试用例
    """
    def __init__( self ):
        pass

    def run( self, params ):
        app.logger.info( 'executing %s' % ( __name__ ) )

        app.logger.info( "这是一个用例" )

        app.logger.info( "finished %s" % ( __name__ ) )
        