#!/usr/bin/python3

"""
@file: Helper.py
@brief: 公共辅助函数
@author: feihu1996.cn
@date: 18-09-19
@version: 1.0
"""

import base64
import hashlib
import re


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
    return re.sub( r"\s|\n", "", string.strip() )
    