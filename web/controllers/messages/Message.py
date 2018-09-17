#!/usr/bin/python3

"""
@file: Message.py
@brief: 消息蓝图控制器
@author: feihu1996.cn
@date: 18-09-17
@version: 1.0
"""

# TODO:定义一个接口，自定义一次过滤项目需求关键词（会有一张first_filter_keys表）和二次过滤项目需求群号码、QQ号（会分别用second_filter_qqnumber表和second_filter_groupnumber表来保存）

# TODO:定义一个接口，根据first_filter_keys表中的关键词，查询original_messages数据表，进行一次过滤，将结果集插入到名为first_filter_messages的hive数据表或者mysql数据表或者Redis键中（会实现增量插入）， 同时将数据增量插入到messages数据表中

# TODO:定义一个接口，根据second_filter_qqnumber表和second_filter_groupnumber表中的群号码、QQ号，查询first_filter_messages数据表，进行二次过滤，将结果集插入到名为second_filter_messages的hive数据表或者mysql数据表或者Redis键中（会实现增量插入），同时将数据增量插入到messages数据表中

# TODO:定义一个接口，用于查询messages数据表

