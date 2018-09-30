#!/usr/bin/python3

"""
@file: AutoExportWeChatMsgs.py
@brief: 自动抓取微信群消息
@author: feihu1996.cn
@date: 18-09-29
@version: 1.0
"""

import re
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
from common.libs.Helper import (driver_swipe_down, get_current_date,
                                get_simulator_window_size)
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

            # TODO:获取群聊名称
            group_name = self.wait.until( EC.presence_of_element_located( ( By.ID,'com.tencent.mm:id/hm' ) ) ).get_attribute( 'text' )
            if not group_name or not re.compile( self.group_tag_pattern ).findall( group_name ):
                app.logger.info( "当前会话不是群聊，即将关闭..." )
                return
            group_name = re.sub( self.group_tag_pattern, "", group_name )
            app.logger.info( "当前群聊名称为：" + group_name )

            current_simulator_window_size = get_simulator_window_size( self.driver )
            app.logger.info( "当前屏幕尺寸为:{0}".format( current_simulator_window_size ) )

            time.sleep( 1 )  # 强制等待1秒

            # TODO:消息发布时间
            send_time = get_current_date()
            app.logger.info( '消息发布时间:%s' %( send_time )  )   

            # 不断向下滑屏，获取当前屏消息
            while True:
                self.get_current_page_msgs()
                try:
                    self.driver.find_element_by_id( 'com.tencent.mm:id/abj' )
                    app.logger.info( "发现新消息提示框,正在继续向下滑屏..." )
                    driver_swipe_down( current_simulator_window_size, self.driver )
                except NoSuchElementException:
                    app.logger.info( "没有找到新消息提示框，只向下滑屏10次..." )
                    for i in range(0, 10):
                        driver_swipe_down( current_simulator_window_size, self.driver )
                        self.get_current_page_msgs()
                    break

        except:
            app.logger.info( traceback.format_exc() )
        finally:
            app.logger.info( "正在关闭当前Appium会话..." )  # 关闭当前会话
            self.driver.quit()

        app.logger.info( "finished %s" % ( __name__ ) )

    def get_current_page_msgs( self ):
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

            # TODO: 用户昵称
            send_name = self.wait.until( EC.presence_of_element_located(
                ( By.ID, 'com.tencent.mm:id/qj' )
            ) ).get_attribute( 'text' )
            app.logger.info( '当前消息用户昵称为:%s' %( send_name ) )

            app.logger.info( '正在点击返回按钮,返回消息对话框界面...' )
            self.driver.find_element_by_id( 'com.tencent.mm:id/hs' ).click()
            self.wait.until( EC.presence_of_element_located( ( By.ID,'com.tencent.mm:id/hm' ) ) )                   
  
            # TODO:消息内容   
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

                    edit_input = self.driver.find_element_by_id( 'com.tencent.mm:id/ac8' )  # 获取输入框元素

                    app.logger.info( '清空输入框' )
                    edit_input.clear()  # 清空输入框      

                    app.logger.info( '长按"输入框"2秒钟' )
                    TouchAction( self.driver ).long_press(  # 长按"输入框"2秒钟
                        edit_input, duration=2000
                    ).wait( 200 ).release().perform()

                    # TODO:安卓系统升级到5.1.1后可以直接获取toast
                    app.logger.info( '点击"粘贴"' )
                    TouchAction( self.driver ).press(  # 点击"粘贴"
                        x=edit_input.location.get('x'), y=edit_input.location.get('y')-20
                    ).release().perform()
                    
                    app.logger.info( '获取输入框的文字' )
                    content = self.wait.until(EC.presence_of_element_located(
                        ( By.ID,'com.tencent.mm:id/ac8' )
                    )).get_attribute( 'text' )
                    app.logger.info( '匹配到文字消息:%s' %( content ) )
                except:
                    app.logger.info( traceback.format_exc() )
                    app.logger.info( '当前消息信息不完全, 跳过当前消息' )
                    continue                                    
