#!/usr/bin/python3

"""
@file: Helper.py
@brief: 公共辅助函数
@author: feihu1996.cn
@date: 18-09-19
@version: 1.0
"""

import base64
import datetime
import hashlib
import re
import pyperclip


def md5_hash( string ):
    """
    获取给定字符串的指纹
    """
    m = hashlib.md5()
    string = base64.encodebytes( string.encode("utf-8") )
    m.update(string)
    return m.hexdigest()  

def get_dict( string ):
    """
    由字符串(如a=1&b=2)得到字典
    """
    new_dict = dict()
    for item in re.split( "&", string ):
        k, v = re.split( "=", item )
        new_dict[k] = v
    return new_dict

def clean_string( string ):
    """
    取出string中的多余字符，如空格等
    """
    return re.sub( r"\s|\n|★|√|×", "", string.strip() )
    
def get_simulator_window_size( driver ):
    """
    Appium获取模拟器屏幕尺寸
    """
    width = driver.get_window_size()['width']
    height = driver.get_window_size()['height']
    return width, height

def driver_swipe_up( current_simulator_window_size,driver ):
    """
    Appium控制模拟器屏幕向上滑动
    """
    l = current_simulator_window_size
    x1 = int( l[0] * 0.5 )
    y1 = int( l[1] * 0.95 )
    y2 = int( l[1] * 0.35 )
    driver.swipe( x1, y1, x1, y2, 1000 )    

def driver_swipe_right( current_simulator_window_size,driver ):
    """
    Appium控制模拟器屏幕向右滑动
    """
    l = current_simulator_window_size
    y1 = int( l[1] * 0.5 )
    x1 = int( l[0] * 0.25 )
    x2 = int( l[0] * 0.95 )
    driver.swipe( x1, y1, x2, y1, 1000 )  

def driver_swipe_down( current_simulator_window_size,driver, start_y=0.35, end_y=0.65 ):
    """
    Appium控制模拟器屏幕向下滑动
    """
    l = current_simulator_window_size
    x1 = int( l[0] * 0.5 )
    y1 = int( l[1] * start_y )
    y2 = int( l[1] * end_y )
    driver.swipe( x1, y1, x1, y2, 1000 )   

def driver_swipe_left( current_simulator_window_size,driver ):
    """
    Appium控制模拟器屏幕向左滑动
    """
    l = current_simulator_window_size
    x1 = int( l[0]*0.9 )
    y1 = int( l[1]*0.5 )
    x2 = int( l[0]*0.1 )
    driver.swipe( x1, y1, x2, y1, 1000 )

def get_current_date( format="%Y-%m-%d %H:%M:%S" ):
    """
    获取当前时间
    """
    return datetime.datetime.now().strftime( format )

def get_clipboard_text():
    """
    获取剪贴板内容
    """
    return pyperclip.paste()

def set_clipboard_text( aString ):
    """
    设置剪贴板内容
    """
    pyperclip.copy( aString )
