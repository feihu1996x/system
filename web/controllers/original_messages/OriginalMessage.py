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
from common.libs.messages.MessagesService import MessagesService
from common.models.messages.OriginalMessages import OriginalMessage

route_original_message = Blueprint( "original_message", __name__ )

@route_original_message.route( "/", methods=[ "POST" ] )
def post_original_message():
    """
    post /original_message
        新增原始消息
    """
    req_dict = request.values  # 获取所有请求参数

    # 封装响应
    resp_data = {
        "code": 0,
        "count": 0,
        "msg": "操作成功~",
        "data": []
    }        

    group_id = req_dict["group_id"] if "group_id" in req_dict else None  # QQ/微信群id
    sender_name = req_dict["sender_name"] if "sender_name" in req_dict else None  # 用户昵称
    qq_number = req_dict["qq_number"] if "qq_number" in req_dict else None  # QQ/微信号
    content = req_dict["content"] if "content" in req_dict else None  # 消息内容
    send_time = req_dict["send_time"] if "send_time" in req_dict else None  # 消息发布时间
    fingerprint = req_dict["fingerprint"] if "fingerprint" in req_dict else None  # 每条消息的fingerprint

    try:
        group_id = int( group_id )
    except:
        resp_data["msg"] = "参数错误"
        resp_data["code"] = -1
        response = make_response( json.dumps( resp_data ), 400 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response      

    if not sender_name or not qq_number or not content or not send_time or not fingerprint:
        resp_data["msg"] = "参数错误"
        resp_data["code"] = -1
        response = make_response( json.dumps( resp_data ), 400 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response  

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
        except:
            db.session.rollback()
            app.logger.info( traceback.format_exc() )
            resp_data["msg"] = "数据保存失败"
            resp_data["code"] = -1
            response = make_response( json.dumps( resp_data ), 500 )
            response.headers["Content-Type"] = "application/json;charset=utf-8"
            return response

        resp_data["data"].append({
            "group_id": original_message_model.group_id,
            "sender_name": original_message_model.sender_name,
            "qq_number": original_message_model.qq_number,
            "content": original_message_model.content,
            "send_time": str( original_message_model.send_time ),
            "fingerprint": original_message_model.fingerprint
        })
        resp_data["count"] = 1  
        response = make_response( json.dumps( resp_data ), 200 )
        response.headers["Content-Type"] = "application/json;charset=utf-8" 
        return response                        
    else:
        response = make_response( json.dumps( resp_data ), 200 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response          
