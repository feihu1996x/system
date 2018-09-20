#!/usr/bin/python3

"""
@file: Message.py
@brief: 消息蓝图控制器
@author: feihu1996.cn
@date: 18-09-17
@version: 1.0
"""

import json

from flask import Blueprint, make_response, request

from application import app, db
from common.libs.messages.MessagesService import MessagesService
from common.models.messages.FirstFilterKeys import FirstFilterKey
from common.models.messages.SecondFilterGroupnumber import \
    SecondFilterGroupnumber
from common.models.messages.SecondFilterQqnumber import SecondFilterQqnumber

route_message = Blueprint( "message", __name__ )

@route_message.route( "/filter/keys", methods=[ "GET", "POST" ] )
def get_post_keys():
    """
    get /message/filter/keys
        获取过滤关键词列表
    post /message/filter/keys
        新增一个关键词       
    """

    # 获取所有请求参数
    req_dict = request.values    

    # 封装响应字段
    resp_data = {
        "msg": "操作成功~",
        "data": {}
    }

    if "GET" == request.method:
        # TODO: 实现分页加载
        key_model_list = FirstFilterKey.query.order_by( FirstFilterKey.id.desc() ).all()

        key_data_list = []

        if key_model_list:
            for model in key_model_list:
                key_data_list.append({
                    "id": model.id,
                    "key_name": model.key_name
                })
        
        resp_data["data"]["key_list"] = key_data_list

        response = make_response( json.dumps( resp_data ), 200 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response

    if "POST" == request.method:
        key_name = req_dict.get( "key_name", None )
        if not key_name:
            resp_data["msg"] = "参数错误"
            response = make_response( json.dumps( resp_data ), 404 )
            response.headers["Content-Type"] = "application/json;charset=utf-8"
            return response     
        key_model = FirstFilterKey.query.filter_by( key_name=key_name ).first()
        if key_model:
            resp_data["msg"] = "关键字已经存在" 
            response = make_response( json.dumps( resp_data ), 406 )
            response.headers["Content-Type"] = "application/json;charset=utf-8"   
            return response
        else:
            key_model = FirstFilterKey()
            key_model.key_name = key_name
            db.session.add( key_model )
            db.session.commit()
            resp_data["data"]["id"] = key_model.id
            resp_data["data"]["key_name"] = key_model.key_name
            response = make_response( json.dumps( resp_data ), 200 )
            response.headers["Content-Type"] = "application/json;charset=utf-8"            

            # 更新消息记录表
            MessagesService.update_messages()

            return response

@route_message.route( "/filter/keys/<key_id>", methods=[ "PUT", "DELETE" ] )
def put_delete_keys( key_id ):
    """
    put /message/filter/keys/key_id
        更新一个关键词
    delete /message/filter/keys/key_id
        删除一个关键词         
    """
    # 获取所有请求参数
    req_dict = request.values   

    # 封装响应字段
    resp_data = {
        "msg": "操作成功~",
        "data": {}
    }

    if not key_id:
        resp_data["msg"] = "缺少参数"
        response = make_response( json.dumps( resp_data ), 404 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response

    try:
        key_id = int( key_id )
    except:
        resp_data["msg"] = "参数错误"
        response = make_response( json.dumps( resp_data ), 406 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response     

    key_model = FirstFilterKey.query.filter_by( id=key_id ).first()
    if not key_model:
        resp_data["msg"] = "资源不存在" 
        response = make_response( json.dumps( resp_data ), 404 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response           

    if "PUT" == request.method:
        key_name = req_dict.get( "key_name", None )   
        if not key_name:
            resp_data["msg"] = "缺少参数"
            response = make_response( json.dumps( resp_data ), 404 )
            response.headers["Content-Type"] = "application/json;charset=utf-8"
            return response              

        key_model.key_name= key_name
        db.session.add( key_model )            
        db.session.commit()
        resp_data["data"]["id"] = key_model.id
        resp_data["data"]["key_name"] = key_model.key_name        
        response = make_response( json.dumps( resp_data ), 200 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"

        # 更新消息记录表
        MessagesService.update_messages()        

        return response           

    if "DELETE" == request.method:
        db.session.delete( key_model )
        db.session.commit()   
        response = make_response( json.dumps( resp_data ), 200 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"

        # 更新消息记录表
        MessagesService.update_messages()

        return response           

@route_message.route( "/filter/group_numbers", methods=[ "GET", "POST" ] )
def get_post_group_numbers():
    """
    get /message/filter/group_numbers
        获取过滤QQ群号码列表
    post /message/filter/group_numbers
        新增一个QQ群号码       
    """
    # 获取所有请求参数
    req_dict = request.values    

    # 封装响应字段
    resp_data = {
        "msg": "操作成功~",
        "data": {}
    }

    if "GET" == request.method:
        # TODO: 实现分页加载
        number_model_list = SecondFilterGroupnumber.query.order_by( SecondFilterGroupnumber.id.desc() ).all()

        number_data_list = []

        if number_model_list:
            for model in number_model_list:
                number_data_list.append({
                    "id": model.id,
                    "group_number": model.group_number
                })
        
        resp_data["data"]["number_list"] = number_data_list

        response = make_response( json.dumps( resp_data ), 200 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response    

    if "POST" == request.method:
        group_number = req_dict.get( "group_number", None )
        if not group_number:
            resp_data["msg"] = "参数错误"
            response = make_response( json.dumps( resp_data ), 404 )
            response.headers["Content-Type"] = "application/json;charset=utf-8"
            return response     
        number_model = SecondFilterGroupnumber.query.filter_by( group_number=group_number ).first()
        if number_model:
            resp_data["msg"] = "QQ群号码已经存在" 
            response = make_response( json.dumps( resp_data ), 406 )
            response.headers["Content-Type"] = "application/json;charset=utf-8"   
            return response
        else:
            number_model = SecondFilterGroupnumber()
            number_model.group_number = group_number
            db.session.add( number_model )
            db.session.commit()
            resp_data["data"]["id"] = number_model.id
            resp_data["data"]["group_number"] = number_model.group_number
            response = make_response( json.dumps( resp_data ), 200 )
            response.headers["Content-Type"] = "application/json;charset=utf-8"      

            # 更新消息记录表
            MessagesService.update_messages()

            return response        

@route_message.route( "/filter/group_numbers/<number_id>", methods=[ "PUT", "DELETE" ] )
def put_delete_group_numbers( number_id ):
    """
    put /filter/group_numbers/number_id
        更新一个QQ群号码
    delete /filter/group_numbers/number_id
        删除一个QQ群号码       
    """
    # 获取所有请求参数
    req_dict = request.values   

    # 封装响应字段
    resp_data = {
        "msg": "操作成功~",
        "data": {}
    }

    if not number_id:
        resp_data["msg"] = "缺少参数"
        response = make_response( json.dumps( resp_data ), 404 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response

    try:
        number_id = int( number_id )
    except:
        resp_data["msg"] = "参数错误"
        response = make_response( json.dumps( resp_data ), 406 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response     

    number_model = SecondFilterGroupnumber.query.filter_by( id=number_id).first()
    if not number_model:
        resp_data["msg"] = "资源不存在" 
        response = make_response( json.dumps( resp_data ), 404 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response           

    if "PUT" == request.method:
        group_number = req_dict.get( "group_number", None )   
        if not group_number:
            resp_data["msg"] = "缺少参数"
            response = make_response( json.dumps( resp_data ), 404 )
            response.headers["Content-Type"] = "application/json;charset=utf-8"
            return response              

        number_model.group_number= group_number
        db.session.add( number_model )            
        db.session.commit()
        resp_data["data"]["id"] = number_model.id
        resp_data["data"]["group_number"] = number_model.group_number        
        response = make_response( json.dumps( resp_data ), 200 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"

        # 更新消息记录表
        MessagesService.update_messages()

        return response           

    if "DELETE" == request.method:
        db.session.delete( number_model )
        db.session.commit()   
        response = make_response( json.dumps( resp_data ), 200 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"

        # 更新消息记录表
        MessagesService.update_messages()        

        return response  

@route_message.route( "/filter/qq_numbers", methods=[ "GET", "POST" ] )
def get_post_qq_numbers():
    """
    get /message/filter/qq_numbers
        获取过滤QQ号码列表
    post /message/filter/qq_numbers
        新增一个QQ号码       
    """    
    # 获取所有请求参数
    req_dict = request.values    

    # 封装响应字段
    resp_data = {
        "msg": "操作成功~",
        "data": {}
    }

    if "GET" == request.method:
        # TODO: 实现分页加载
        number_model_list = SecondFilterQqnumber.query.order_by( SecondFilterQqnumber.id.desc() ).all()

        number_data_list = []

        if number_model_list:
            for model in number_model_list:
                number_data_list.append({
                    "id": model.id,
                    "qq_number": model.qq_number
                })
        
        resp_data["data"]["number_list"] = number_data_list

        response = make_response( json.dumps( resp_data ), 200 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response      

    if "POST" == request.method:
        qq_number = req_dict.get( "qq_number", None )
        if not qq_number:
            resp_data["msg"] = "参数错误"
            response = make_response( json.dumps( resp_data ), 404 )
            response.headers["Content-Type"] = "application/json;charset=utf-8"
            return response     
        number_model = SecondFilterQqnumber.query.filter_by( qq_number=qq_number ).first()
        if number_model:
            resp_data["msg"] = "QQ号码已经存在" 
            response = make_response( json.dumps( resp_data ), 406 )
            response.headers["Content-Type"] = "application/json;charset=utf-8"   
            return response
        else:
            number_model = SecondFilterQqnumber()
            number_model.qq_number = qq_number
            db.session.add( number_model )
            db.session.commit()
            resp_data["data"]["id"] = number_model.id
            resp_data["data"]["qq_number"] = number_model.qq_number
            response = make_response( json.dumps( resp_data ), 200 )
            response.headers["Content-Type"] = "application/json;charset=utf-8"         

            # 更新消息记录表
            MessagesService.update_messages()            

            return response  

@route_message.route( "/filter/qq_numbers/<number_id>", methods=[ "PUT", "DELETE" ] )
def put_delete_qq_numbers( number_id ):
    """
    put /filter/qq_numbers/number_id
        更新一个QQ号码
    delete /filter/qq_numbers/number_id
        删除一个QQ号码
    """
    # 获取所有请求参数
    req_dict = request.values   

    # 封装响应字段
    resp_data = {
        "msg": "操作成功~",
        "data": {}
    }

    if not number_id:
        resp_data["msg"] = "缺少参数"
        response = make_response( json.dumps( resp_data ), 404 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response

    try:
        number_id = int( number_id )
    except:
        resp_data["msg"] = "参数错误"
        response = make_response( json.dumps( resp_data ), 406 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response     

    number_model = SecondFilterQqnumber.query.filter_by( id=number_id).first()
    if not number_model:
        resp_data["msg"] = "资源不存在" 
        response = make_response( json.dumps( resp_data ), 404 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response           

    if "PUT" == request.method:
        qq_number = req_dict.get( "qq_number", None )   
        if not qq_number:
            resp_data["msg"] = "缺少参数"
            response = make_response( json.dumps( resp_data ), 404 )
            response.headers["Content-Type"] = "application/json;charset=utf-8"
            return response              

        number_model.qq_number= qq_number
        db.session.add( number_model )            
        db.session.commit()
        resp_data["data"]["id"] = number_model.id
        resp_data["data"]["qq_number"] = number_model.qq_number        
        response = make_response( json.dumps( resp_data ), 200 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"

        # 更新消息记录表
        MessagesService.update_messages()

        return response           

    if "DELETE" == request.method:
        db.session.delete( number_model )
        db.session.commit()   
        response = make_response( json.dumps( resp_data ), 200 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"

        # 更新消息记录表
        MessagesService.update_messages()

        return response  
