#!/usr/bin/python3

"""
@file: AutoExportGroupMsgs.py
@brief: 自动导出QQ群消息记录
@author: feihu1996.cn
@date: 18-09-17
@version: 1.0
"""

import time

import pyautogui
from pywinauto.application import Application

from application import app, db
from common.libs.messages.MessagesService import MessagesService

# 每次函数调用后暂停1秒
pyautogui.PAUSE = 1

# 启动自动防故障功能，将鼠标移到屏幕的左上角的将导致异常
pyautogui.FAILSAFE = True    


class JobTask():
    """
    python manager.py runjob -m spiders/messages/AutoExportGroupMsgs
    自动导出QQ群消息记录
    """
    def __init__(self):  
        self.screen_width, self.screen_height = pyautogui.size()
        self.qq_account_list = app.config['QQ_ACCOUNT_LIST']
        self.qq_path = app.config['QQ_PATH']
        self.msg_path = app.config['MSG_PATH']
        self.export_x_coor = app.config['EXPORT_X_COOR']
        self.export_y_coor = app.config['EXPORT_Y_COOR']
        self.msg_file_x_coor = app.config['MSG_FILE_X_COOR']
        self.msg_file_y_coor = app.config['MSG_FILE_Y_COOR']

    def run(self, params):
        app.logger.info( "launching %s ..." % ( __name__ ) )
        app.logger.info( "当前屏幕宽为：" + str( self.screen_width ) + "," + "当前屏幕高为：" + str( self.screen_height ) )

        for qq_account in self.qq_account_list:  # 依次使用不同的账号登录QQ，导出QQ群消息记录
            qq_number = qq_account["qq_number"]
            qq_password = qq_account["qq_password"]

            # 打开qq
            app.logger.info( "正在打开QQ..." )
            qq = Application( backend='uia' ).start( self.qq_path )

            # qq.QQ.print_control_identifiers()

            # 输入账号            
            app.logger.info( "正在输入账号..." )
            qq.QQ.Pane16.child_window(title="QQ号码", control_type="ComboBox").click_input()
            qq.QQ.Pane16.child_window(title="QQ号码", control_type="ComboBox").type_keys( qq_number )
            
            # 输入密码
            app.logger.info( "正在输入密码..." )
            qq.QQ.Pane16.child_window(title="密码", control_type="Pane").click_input()
            qq.QQ.Pane16.child_window(title="密码", control_type="Pane").type_keys( qq_password )
             
            # 点击登录按钮
            app.logger.info( "正在登录..." )
            qq.QQ.child_window(title="登   录", control_type="Button").click_input()

            # 打开QQ消息管理器
            app.logger.info( "正在连接新的QQ进程..." )
            qq = None
            qq = Application( backend='uia' ).connect( path=self.qq_path )

            # 点击第三个tab选项卡，即群聊
            app.logger.info( "正在打开群聊选项卡..." )
            qq.QQ.TabControl.TabItem3.click_input()

            # 单击"我的QQ群"
            app.logger.info( "正在打开我的QQ群..." )
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
            app.logger.info( "正在打开消息管理器..." )
            pyautogui.click()
            
            # 导出全部消息记录
            app.logger.info( "正在导出消息记录..." )
            x = self.export_x_coor
            y = self.export_y_coor
            app.logger.info( "鼠标当前的坐标 X:" + str( x ).rjust( 4 ) + " Y:" + str( y ).rjust( 4 ) )
            pyautogui.moveTo( x, y ) 
            pyautogui.click(x, y)
            
            # 点击导出按钮
            app.logger.info( "正在点击导出按钮..." )
            x = x + 88
            y = y + 49
            app.logger.info( "鼠标当前的坐标 X:" + str( x ).rjust( 4 ) + " Y:" + str( y ).rjust( 4 ) )
            pyautogui.moveTo( x, y ) 
            pyautogui.click( x, y )

            # 选择消息文件保存类型
            app.logger.info( "正在选择文件保存类型..." )
            x = self.msg_file_x_coor
            y = self.msg_file_y_coor
            app.logger.info( "鼠标当前的坐标 X:" + str( x ).rjust( 4 ) + " Y:" + str( y ).rjust( 4 ) )     
            pyautogui.moveTo( x, y )
            pyautogui.click( x, y )
            y = y + 39
            app.logger.info( "鼠标当前的坐标 X:" + str( x ).rjust( 4 ) + " Y:" + str( y ).rjust( 4 ) )  
            pyautogui.moveTo( x, y )
            pyautogui.click( x, y )

            # 发送快捷键"Alt+S",保存消息记录文件
            app.logger.info( "正在保存..." )
            pyautogui.keyDown('altleft')
            pyautogui.keyDown('s')
            pyautogui.keyUp('altleft')
            pyautogui.keyUp('s')
            # 如果文件已经存在，则覆盖掉
            pyautogui.keyDown('altleft')
            pyautogui.keyDown('y')
            pyautogui.keyUp('altleft')
            pyautogui.keyUp('y') 

            # 关闭消息管理器
            app.logger.info( "正在关闭消息管理器..." )
            pyautogui.keyDown( 'altleft' )
            pyautogui.keyDown( 'f4' )
            pyautogui.keyUp( 'altleft' )
            pyautogui.keyUp( 'f4' )
            # qq.QQ.ScrollBar.print_control_identifiers()

            # 关闭QQ
            app.logger.info( "正在关闭QQ..." )
            qq.QQ.click_input()
            pyautogui.keyDown( 'altleft' )
            pyautogui.keyDown( 'f4' )
            pyautogui.keyUp( 'altleft' )
            pyautogui.keyUp( 'f4' ) 

            msgs = open( self.msg_path + r"\全部消息记录.txt","rb" ).read().decode("utf8")

            # 对消息记录进行数据格式化，并增量保存到数据库(original_messages表)   
            app.logger.info( "正在将消息写入数据库..." )
            MessagesService.save_export_group_msgs( msgs=msgs )               
            
            # 一次过滤，first_filter_keys表， 并保存到数据库（messages表），调用公共方法
            app.logger.info( "正在根据关键词过滤原始消息记录表..." )
            MessagesService.filter_by_keys()

            # 二次过滤，second_filter_qqnumber表、second_filter_groupnumber表， 并保存到数据库（messages表），调用公共方法
            app.logger.info( "根据给定的QQ群号码或者QQ号过滤消息记录表" )
            MessagesService.filter_by_numbers()

        app.logger.info( "finished %s" % ( __name__ ) )
