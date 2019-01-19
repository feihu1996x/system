#!/usr/bin/python3

"""
@file: OriginalMessage.py
@brief: 原始消息蓝图控制器
@author: feihu1996.cn
@date: 18-10-08
@version: 1.0
"""

import json
import traceback

from flask import Blueprint, make_response, request

from application import app, db
from common.models.messages.OriginalMessages import OriginalMessage

route_original_message = Blueprint( "original_message", __name__ )

@route_original_message.route( "/", methods=[ "POST" ] )
def post_original_message():
    """
    post /original_message/
        批量新增原始消息
    """
    req_dict = request.get_json()  # 获取所有请求参数

    # 封装响应
    resp_data = {
        "code": 0,
        "count": 0,
        "msg": "操作成功~",
        "data": []
    }   
    response = make_response( json.dumps( resp_data ), 200 )
    response.headers["Content-Type"] = "application/json;charset=utf-8"    

    original_message_list = req_dict["original_message_list"] if req_dict else None  # 批量推送的原始消息记录

    if not isinstance( original_message_list, list ):
        resp_data["msg"] = "参数错误"       
        resp_data["code"] = -1
        response = make_response( json.dumps( resp_data ), 400 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response

    app.logger.info( "批量推送的原始消息记录数量为%d" % ( len( original_message_list ) ) )

    for original_message in original_message_list:
        group_id = original_message["group_id"] if "group_id" in original_message else None  # QQ/微信群id
        sender_name = original_message["sender_name"] if "sender_name" in original_message else None  # 用户昵称
        qq_number = original_message["qq_number"] if "qq_number" in original_message else None  # QQ/微信号
        content = original_message["content"] if "content" in original_message else None  # 消息内容
        send_time = original_message["send_time"] if "send_time" in original_message else None  # 消息发布时间
        fingerprint = original_message["fingerprint"] if "fingerprint" in original_message else None  # 每条消息的fingerprint

        original_message_model = OriginalMessage.query.filter_by( fingerprint=fingerprint ).first()
        if not original_message_model:
            app.logger.info( '消息正在入库...' )
            original_message_model = OriginalMessage()
            original_message_model.group_id = group_id
            original_message_model.sender_name = sender_name
            original_message_model.qq_number = qq_number
            original_message_model.content = content
            original_message_model.send_time = str( send_time )
            original_message_model.fingerprint = fingerprint

            try:
                db.session.add( original_message_model )
                db.session.commit()           
                resp_data["data"].append({  # 将写入成功的消息记录的指纹添加到返回数据中
                    "fingerprint": original_message_model.fingerprint
                })
                resp_data["count"] += 1                
            except:
                db.session.rollback()
                app.logger.info( traceback.format_exc() )                    
    
    return response           
