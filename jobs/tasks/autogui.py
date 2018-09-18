#!/usr/bin/python3

"""
@file: Autogui.py
@brief: 自动化GUI获取QQ群消息记录
@author: feihu1996.cn
@date: 18-09-17
@version: 1.0
"""

import time

import pyautogui
from pywinauto.application import Application
from application import app, db

# TODO:读取配置文件，依次使用不同的账号打开QQ、登录、打开消息管理器、导出QQ群消息记录到指定目录下（先清空该目录）

# TODO:遍历该目录，读取所有消息记录文件，将数据结构化处理后插入到名为original_messages的hive数据表或者mysql数据表或者Redis键中(会实现增量插入)，hive有点吃内存（但可用于分布式计算），同时将数据增量插入到messages数据表中

# 每次函数调用后暂停一秒
pyautogui.PAUSE = 1

# 启动自动防故障功能，将鼠标移到屏幕的左上角的将导致异常
pyautogui.FAILSAFE = True    


class JobTask():
    """
    python manager.py runjob -m Autogui
    自动化GUI获取QQ群消息记录
    """
    def __init__(self):
        self.msg = "launching Autogui ..."  
        self.screen_width, self.screen_height = pyautogui.size()
        self.qq_account_list = app.config['QQ_ACCOUNT_LIST']
        self.qq_path = app.config['QQ_PATH']
        self.export_x_coor = app.config['EXPORT_X_COOR']
        self.export_y_coor = app.config['EXPORT_Y_COOR']

    def run(self, params):
        app.logger.info( self.msg )
        app.logger.info( "当前屏幕宽为：" + str( self.screen_width ) + "," + "当前屏幕高为：" + str( self.screen_height ) )

        for qq_account in self.qq_account_list:
            qq_number = qq_account["qq_number"]
            qq_password = qq_account["qq_password"]

            # 打开qq
            qq = Application( backend='uia' ).start( self.qq_path )

            # qq.QQ.print_control_identifiers()

            # 输入账号            
            qq.QQ.Pane16.child_window(title="QQ号码", control_type="ComboBox").click_input()
            qq.QQ.Pane16.child_window(title="QQ号码", control_type="ComboBox").type_keys( qq_number )
            
            # 输入密码
            qq.QQ.Pane16.child_window(title="密码", control_type="Pane").click_input()
            qq.QQ.Pane16.child_window(title="密码", control_type="Pane").type_keys( qq_password )
             
            # 点击登录按钮
            qq.QQ.child_window(title="登   录", control_type="Button").click_input()

            # 打开QQ消息管理器
            qq = None
            qq = Application( backend='uia' ).connect( path=self.qq_path )
            # 点击第三个tab选项卡，即群聊
            qq.QQ.TabControl.TabItem3.click_input()
            # 单击"我的QQ群"
            qq.QQ.child_window(title="我的QQ群", control_type="ListItem").click_input()
            # 利用pyautogui获取鼠标当前的坐标，然后在第一个QQ群的位置，点击鼠标右键
            x, y = pyautogui.position()
            app.logger.info( "鼠标当前的坐标 X:" + str( x ).rjust( 4 ) + " Y:" + str( y ).rjust( 4 ) )
            # 将鼠标向下移动35个像素
            y = y + 35
            app.logger.info( "鼠标当前的坐标 X:" + str( x ).rjust( 4 ) + " Y:" + str( y ).rjust( 4 ) )
            pyautogui.moveTo( x, y )
            # 点击鼠标右键
            pyautogui.rightClick()
            # 将鼠标向右移动40个像素,向下移动90个像素    
            x = x + 40
            y = y + 90
            app.logger.info( "鼠标当前的坐标 X:" + str( x ).rjust( 4 ) + " Y:" + str( y ).rjust( 4 ) )
            pyautogui.moveTo( x, y )            
            # 点击“查看消息记录”按钮，打开消息管理器
            pyautogui.click()
            
            # 导出全部消息记录
            x = self.export_x_coor
            y = self.export_y_coor
            app.logger.info( "鼠标当前的坐标 X:" + str( x ).rjust( 4 ) + " Y:" + str( y ).rjust( 4 ) )
            pyautogui.moveTo( x, y ) 
            pyautogui.click(x, y)
            # 点击导出按钮
            x = x + 88
            y = y + 49
            app.logger.info( "鼠标当前的坐标 X:" + str( x ).rjust( 4 ) + " Y:" + str( y ).rjust( 4 ) )
            pyautogui.moveTo( x, y ) 
            pyautogui.click( x, y )            
            # qq.QQ.ScrollBar.print_control_identifiers()

            # 关闭QQ
            qq.QQ.close()
            

