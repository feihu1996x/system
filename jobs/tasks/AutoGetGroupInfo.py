#!/usr/bin/python3

"""
@file: AutoGetGroupInfo.py
@brief: 自动获取QQ群信息(QQ群号码)
@author: feihu1996.cn
@date: 18-09-19
@version: 1.0
"""

import time

import pyautogui
from pywinauto.application import Application

from application import app, db

# 每次函数调用后暂停1秒
pyautogui.PAUSE = 1

# 启动自动防故障功能，将鼠标移到屏幕的左上角的将导致异常
pyautogui.FAILSAFE = True    


class JobTask():
    """
    python manager.py runjob -m AutoGetGroupInfo
    自动获取QQ群信息,根据QQ群名称获取QQ群号码
    """
    def __init__(self):  
        self.screen_width, self.screen_height = pyautogui.size()
        self.qq_account_list = app.config['QQ_ACCOUNT_LIST']
        self.qq_path = app.config['QQ_PATH']

    def run(self, params):
        app.logger.info( "launching %s ..." % ( __name__ ) )
        app.logger.info( "当前屏幕宽为：" + str( self.screen_width ) + "," + "当前屏幕高为：" + str( self.screen_height ) )

        for qq_account in self.qq_account_list:
            qq_number = qq_account["qq_number"]
            qq_password = qq_account["qq_password"]

            # 打开qq
            app.logger.info( "正在打开qq ..." )
            qq = Application( backend='uia' ).start( self.qq_path )

            # qq.QQ.print_control_identifiers()

            # 输入账号    
            app.logger.info( "正在输入账号 ..." )
            qq.QQ.Pane16.child_window(title="QQ号码", control_type="ComboBox").click_input()
            qq.QQ.Pane16.child_window(title="QQ号码", control_type="ComboBox").type_keys( qq_number )
            
            # 输入密码
            app.logger.info( "正在输入密码 ..." )
            qq.QQ.Pane16.child_window(title="密码", control_type="Pane").click_input()
            qq.QQ.Pane16.child_window(title="密码", control_type="Pane").type_keys( qq_password )
             
            # 点击登录按钮
            app.logger.info( "正在登录 ..." )
            qq.QQ.child_window(title="登   录", control_type="Button").click_input()

            # 获取QQ群列表窗体对象
            qq = None
            qq = Application( backend='uia' ).connect( path=self.qq_path )
            # 点击第三个tab选项卡，即群聊
            qq.QQ.TabControl.TabItem3.click_input()
            # 单击"我的QQ群"
            qq.QQ.child_window(title="我的QQ群", control_type="ListItem").click_input()

            # TODO: 根据qq群名称自动获取QQ群号码
            group_name = "2014经济学1班（通告）"
            qq.QQ.child_window(title=group_name, control_type="ListItem").click_input()

            # 关闭QQ
            qq.QQ.click_input()
            pyautogui.keyDown( 'altleft' )
            pyautogui.keyDown( 'f4' )
            pyautogui.keyUp( 'altleft' )
            pyautogui.keyUp( 'f4' )     

        app.logger.info( "finished %s" % ( __name__ ) )    

