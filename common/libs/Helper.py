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


def md5_hash( string ):
    """
    获取给定字符串的指纹
    """
    m = hashlib.md5()
    string = base64.encodebytes( string.encode("utf-8") )
    m.update(string)
    return m.hexdigest()  
