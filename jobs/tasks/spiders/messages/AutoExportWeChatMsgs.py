#!/usr/bin/python3

"""
@file: AutoExportWeChatMsgs.py
@brief: 自动抓取微信群消息
@author: feihu1996.cn
@date: 18-09-29
@version: 1.0
"""

import re
import sys
import time
import traceback

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from application import app, db
from common.libs.Helper import (driver_swipe_down, get_clipboard_text,
                                get_current_date, get_simulator_window_size)
from common.libs.messages.MessagesService import MessagesService


class JobTask():
    """
    python manager.py runjob -m spiders/messages/AutoExportWeChatMsgs
    自动抓取微信群消息
    """
    def __init__(self):  
        app.config.from_pyfile( 'config/auto_export_wechat_msgs_setting.py' )
        self.interval = app.config['INTERVAL']
        self.desired_capability = app.config['DESIREED_CAPABILITY']
        self.appium_server = app.config['APPIUM_SERVER']
        self.timeout = app.config['TIMEOUT']

        self.group_tag_pattern = r"\(\d{1,}\)"  # 判断当前对话框是否是群消息的标识

        # if "Y" != input( "请手动启动安卓模拟器，输入Y继续:" ):
        #     sys.exit( 1 )

        # if "Y" != input( "请手动执行'adb connect 127.0.0.1:62001'，输入Y继续:" ):
        #     sys.exit( 1 )

        # if "Y" != input( "请手动启动Appium Desktop，输入Y继续:" ):
        #     sys.exit( 1 )            

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
        定时任务
        """
        while True:
            time.sleep( self.interval )
            self.task()
            time.sleep( self.interval )

    def task( self ):
        """
        自动抓取微信群消息
        """
        app.logger.info( 'executing %s' % ( __name__ ) )

        try:
            app.logger.info( "正在建立Appium会话..." )
            self.driver = webdriver.Remote( self.appium_server, self.desired_capability )  # Appium会话配置
            self.wait=WebDriverWait(self.driver, self.timeout)        

            app.logger.info( "正在点击微信首页消息列表第一条,进入群消息对话框..." )
            self.wait.until( EC.presence_of_element_located( ( By.ID,'com.tencent.mm:id/as4' ) ) ).click()

            # 获取群聊名称
            group_name = self.wait.until( EC.presence_of_element_located( ( By.ID,'com.tencent.mm:id/hm' ) ) ).get_attribute( 'text' )
            if not group_name or not re.compile( self.group_tag_pattern ).findall( group_name ):
                app.logger.info( "当前会话不是群聊，即将关闭..." )
                return
            group_name = re.sub( self.group_tag_pattern, "", group_name )
            app.logger.info( "当前群聊名称为：" + group_name )

            current_simulator_window_size = get_simulator_window_size( self.driver )
            app.logger.info( "当前屏幕尺寸为:{0}".format( current_simulator_window_size ) )

            time.sleep( 1 )  # 强制等待1秒

            # 消息发布时间
            send_time = get_current_date()
            app.logger.info( '消息发布时间:%s' %( send_time )  )   

            # 不断向下滑屏，获取当前屏消息
            while True:
                self.get_current_page_msgs( group_name=group_name, send_time=send_time )
                try:
                    self.driver.find_element_by_id( 'com.tencent.mm:id/abj' )
                    app.logger.info( "发现新消息提示框,正在继续向下滑屏..." )
                    driver_swipe_down( current_simulator_window_size, self.driver )
                except NoSuchElementException:
                    app.logger.info( "没有找到新消息提示框，只向下滑屏3次..." )
                    for i in range(0, 3):
                        driver_swipe_down( current_simulator_window_size, self.driver )
                        self.get_current_page_msgs( group_name=group_name, send_time=send_time )
                    break

            # 一次过滤，first_filter_keys表， 并保存到数据库（messages表），调用公共方法
            app.logger.info( "正在根据关键词过滤原始消息记录表..." )
            MessagesService.filter_by_keys()

            # 二次过滤，second_filter_qqnumber表、second_filter_groupnumber表， 并保存到数据库（messages表），调用公共方法
            app.logger.info( "根据给定的QQ/微信群号码或者QQ/微信号过滤消息记录表" )
            MessagesService.filter_by_numbers()                    

        except:
            app.logger.info( traceback.format_exc() )
        finally:
            app.logger.info( "正在关闭当前Appium会话..." )  # 关闭当前会话
            self.driver.quit()

        app.logger.info( "finished %s" % ( __name__ ) )

    def get_current_page_msgs( self, group_name=None, group_number=None, send_time=None ):
        """
        提取当前屏/页消息
        """
        app.logger.info( '提取当前屏消息...' )  

        # 当前获取到的消息块列表
        message_list = self.wait.until( EC.presence_of_all_elements_located(
            ( By.ID, 'com.tencent.mm:id/y' )
        ) )
        app.logger.info( '当前页共有%d条消息' %( len( message_list ) ) )

        # 遍历消息块列表，处理每条消息
        app.logger.info( '遍历消息...' )
        for message in message_list:            
            try:  
                # 点击用户头像，进入用户详情页，获取用户信息（如昵称等）
                message.find_element_by_id( 'com.tencent.mm:id/kf' ).click()       
            except NoSuchElementException:
                app.logger.info( '当前消息信息不完全, 跳过当前消息' )
                continue

            # 用户昵称
            sender_name = self.wait.until( EC.presence_of_element_located(
                ( By.ID, 'com.tencent.mm:id/qj' )
            ) ).get_attribute( 'text' )
            app.logger.info( '当前消息用户昵称为:%s' %( sender_name ) )

            app.logger.info( '正在点击返回按钮,返回消息对话框界面...' )
            self.driver.find_element_by_id( 'com.tencent.mm:id/hs' ).click()
            self.wait.until( EC.presence_of_element_located( ( By.ID,'com.tencent.mm:id/hm' ) ) )                   
  
            # 消息内容   
            content = ''
            try:
                content += message.find_element_by_id( 'com.tencent.mm:id/af2' ).get_attribute( 'text' )
                content += message.find_element_by_id( 'com.tencent.mm:id/af5' ).get_attribute( 'text' )
                app.logger.info( '匹配到超链接消息:%s' %( content ) )
            except NoSuchElementException:
                try:
                    content_box = message.find_element_by_id( 'com.tencent.mm:id/kh' )  # 文字消息box                   
                except NoSuchElementException:
                    app.logger.info( '当前消息信息不完全, 跳过当前消息' )
                    continue
                try:
                    app.logger.info( '长按"消息正文"2秒钟' )
                    TouchAction( self.driver ).long_press(  # 长按"消息正文"2秒钟
                        x=content_box.location.get('x'), y=content_box.location.get('y'), duration=2000
                    ).wait( 200 ).release().perform()

                    app.logger.info( '复制当前文字消息' )
                    self.driver.find_element_by_android_uiautomator( # 复制当前文字消息
                        'new UiSelector().text("复制")'
                    ).click()    
                    
                    app.logger.info( '获取剪贴板的文字消息' )
                    content = get_clipboard_text()
                    app.logger.info( '匹配到文字消息:%s' %( content ) )                
                except:
                    app.logger.info( traceback.format_exc() )
                    app.logger.info( '当前消息信息不完全, 跳过当前消息' )
                    continue           
                    
            # 对消息记录进行数据格式化，并增量保存到数据库(original_messages表)     
            app.logger.info( "正在将消息写入数据库..." )                    
            MessagesService.save_wechat_group_msg( sender_name=sender_name, content=content, group_name=group_name, group_number=group_number, send_time=send_time )
