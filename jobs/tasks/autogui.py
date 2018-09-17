#!/usr/bin/python3

"""
@file: autogui.py
@brief: 自动化GUI获取QQ群消息记录
@author: feihu1996.cn
@date: 18-09-17
@version: 1.0
"""

# TODO:读取配置文件，依次使用不同的账号打开QQ、登录、打开消息管理器、导出QQ群消息记录到指定目录下（先清空该目录）

# TODO:遍历该目录，读取所有消息记录文件，将数据结构化处理后插入到名为original_messages的hive数据表或者mysql数据表或者Redis键中(会实现增量插入)，hive有点吃内存（但可用于分布式计算），同时将数据增量插入到messages数据表中
