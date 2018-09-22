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
from sqlalchemy import func, or_

from application import app, db
from common.libs.Helper import get_dict
from common.libs.messages.MessagesService import MessagesService
from common.models.messages.FirstFilterKeys import FirstFilterKey
from common.models.messages.Messages import Message
from common.models.messages.QqGroup import QqGroup
from common.models.messages.SecondFilterGroupnumber import \
    SecondFilterGroupnumber
from common.models.messages.SecondFilterQqnumber import SecondFilterQqnumber

route_message = Blueprint( "message", __name__ )

@route_message.route( "/", methods=[ "GET" ] )
def get_message():
    """
    get /message/
        获取QQ群消息列表
    """
    # 获取所有请求参数列表
    req_dict = request.values

    # 封装响应数据
    resp_data = {
        "code": 0,
        "count": 0,
        "msg": "操作成功~",
        "data": []
    }

    query = Message.query

    # 根据群号码或者群名称过滤消息列表
    group = req_dict.get( "group", None )
    if group:
        query = query.filter( or_(
            Message.group_id == ( QqGroup.query.filter_by( group_name=group ).first().id if QqGroup.query.filter_by( group_name=group ).first() else 0 ),
            Message.group_id == ( QqGroup.query.filter_by( group_number=group ).first().id if QqGroup.query.filter_by( group_number=group ).first() else 0 )
        ) )

    # 根据项目信息过滤消息列表
    content = req_dict.get( "content", None )    
    if content:
        query = query.filter( Message.content.ilike( "%{0}%".format( content ) ) )

    # 根据发布人QQ过滤消息列表
    qq_number = req_dict.get( "qq_number", None )
    if qq_number:
        query = query.filter_by( qq_number=qq_number )

    # 根据状态过滤消息列表
    status = req_dict.get( "status", None )
    if status:
        query = query.filter_by( status=status )

    # 根据操作人过滤消息列表
    operator = req_dict.get( "operator", None )
    if operator:
        query =query.filter_by( operator=operator )

    # 实现分页加载
    page = req_dict.get( "page", 1 )
    try:
        page = int( page )
    except:
        resp_data["msg"] = "参数错误"
        resp_data["code"] = -1
        response = make_response( json.dumps( resp_data ), 406 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response          
    if page < 1:
        page = 1        
    page_size = req_dict.get( "limit", 10 )
    try:
        page_size = int( page_size )
    except:
        resp_data["msg"] = "参数错误"
        resp_data["code"] = -1
        response = make_response( json.dumps( resp_data ), 406 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"        
    offset = ( page - 1 ) * page_size

    message_model_list = query.order_by( "-updated_time" ).offset( offset ).limit( page_size ).all()

    message_data_list = []
    if message_model_list:
        for model in message_model_list:
            message_data_list.append({
                "id": model.id,
                "group_number": QqGroup.query.filter_by( id=model.group_id ).first().group_number if QqGroup.query.filter_by( id=model.group_id ).first() else "暂无",
                "group_name": QqGroup.query.filter_by( id=model.group_id ).first().group_name if QqGroup.query.filter_by( id=model.group_id ).first() else "暂无",
                "content": model.content,
                "qq_number": model.qq_number,
                "send_time": str( model.send_time ),
                "status": app.config["MESSAGE_STATUS_MAPPING"][model.status],
                "operator": model.operator
            })
    
    resp_data[ "data" ] = message_data_list
    resp_data[ "count" ] = db.session.query(func.count( Message.id )).scalar()

    response = make_response( json.dumps( resp_data ), 200 )
    response.headers["Content-Type"] = "application/json;charset=utf-8"
    return response

@route_message.route( "/<message_id>", methods=[ "PATCH" ] )
def patch_message( message_id ):
    """
    patch /message/message_id
        更新一条消息
    """
    # 获取所有请求参数
    req_dict = request.values

    # 封装响应字段
    resp_data = {
        "code": 0,
        "count": 0,
        "msg": "操作成功~",
        "data": []
    }    

    if not message_id:
        resp_data["msg"] = "缺少路由参数"
        resp_data["code"] = -1
        response = make_response( json.dumps( resp_data ), 404 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response

    try:
        message_id = int( message_id )
    except:
        resp_data["msg"] = "参数错误"
        resp_data["code"] = -1
        response = make_response( json.dumps( resp_data ), 406 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response     

    message_model = Message.query.filter_by( id=message_id ).first()
    if not message_model:
        resp_data["msg"] = "资源不存在" 
        resp_data["code"] = -1
        response = make_response( json.dumps( resp_data ), 404 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response           

    status = req_dict.get( "status", None )   
    if not status:
        resp_data["msg"] = "缺少参数"
        resp_data["code"] = -1
        response = make_response( json.dumps( resp_data ), 404 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response              

    message_model.status = status
    
    # TODO:通过请求拦截器获取到当前用户信息
    message_model.operator = request.remote_addr
    
    db.session.add( message_model )            
    db.session.commit()

    resp_data[ "data" ].append({
        "id": message_model.id,
        "group_number": QqGroup.query.filter_by( id=message_model.group_id ).first().group_number if QqGroup.query.filter_by( id=message_model.group_id ).first() else "暂无",
        "content": message_model.content,
        "qq_number": message_model.qq_number,
        "send_time": str( message_model.send_time ),
        "status": app.config["MESSAGE_STATUS_MAPPING"][message_model.status],
        "operator": message_model.operator  
    })      
    resp_data["count"] = 1

    response = make_response( json.dumps( resp_data ), 200 )
    response.headers["Content-Type"] = "application/json;charset=utf-8"     

    return response      

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
        "code": 0,
        "count": 0,
        "msg": "操作成功~",
        "data": []
    }

    if "GET" == request.method:
        # 实现分页加载
        page = req_dict.get( "page", 1 )
        try:
            page = int( page )
        except:
            resp_data["msg"] = "参数错误"
            resp_data["code"] = -1
            response = make_response( json.dumps( resp_data ), 406 )
            response.headers["Content-Type"] = "application/json;charset=utf-8"
            return response          
        if page < 1:
            page = 1        
        page_size = req_dict.get( "limit", 10 )
        try:
            page_size = int( page_size )
        except:
            resp_data["msg"] = "参数错误"
            resp_data["code"] = -1
            response = make_response( json.dumps( resp_data ), 406 )
            response.headers["Content-Type"] = "application/json;charset=utf-8"           
        offset = ( page - 1 ) * page_size

        key_model_list = FirstFilterKey.query.order_by( FirstFilterKey.id.desc() ).offset( offset ).limit( page_size ).all()

        key_data_list = []

        if key_model_list:
            for model in key_model_list:
                key_data_list.append({
                    "id": model.id,
                    "key_name": model.key_name
                })
        
        resp_data["data"] = key_data_list
        resp_data[ "count" ] = db.session.query(func.count( FirstFilterKey.id )).scalar()

        response = make_response( json.dumps( resp_data ), 200 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response

    if "POST" == request.method:
        req_dict = request.get_json()
        key_name = req_dict["key_name"] if "key_name" in req_dict else None
        if not key_name:
            resp_data["msg"] = "参数错误"
            resp_data["code"] = -1
            response = make_response( json.dumps( resp_data ), 404 )
            response.headers["Content-Type"] = "application/json;charset=utf-8"
            return response     
        key_model = FirstFilterKey.query.filter_by( key_name=key_name ).first()
        if key_model:
            resp_data["msg"] = "关键字已经存在" 
            resp_data["code"] = -1
            response = make_response( json.dumps( resp_data ), 406 )
            response.headers["Content-Type"] = "application/json;charset=utf-8"   
            return response
        else:
            key_model = FirstFilterKey()
            key_model.key_name = key_name
            db.session.add( key_model )
            db.session.commit()
            resp_data["data"].append({
                "id": key_model.id,
                "key_name": key_model.key_name
            })
            resp_data["count"] = 1
            response = make_response( json.dumps( resp_data ), 200 )
            response.headers["Content-Type"] = "application/json;charset=utf-8"            

            # 更新消息记录表
            MessagesService.update_messages()

            return response

@route_message.route( "/filter/keys/<key_id>", methods=[ "PATCH", "DELETE" ] )
def patch_delete_keys( key_id ):
    """
    patch /message/filter/keys/key_id
        更新一个关键词
    delete /message/filter/keys/key_id
        删除一个关键词         
    """
    # 获取所有请求参数
    req_dict = request.values   

    # 封装响应字段
    resp_data = {
        "code": 0,
        "count": 0,
        "msg": "操作成功~",
        "data": []
    }

    if not key_id:
        resp_data["msg"] = "缺少参数"
        resp_data["code"] = -1
        response = make_response( json.dumps( resp_data ), 404 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response

    try:
        key_id = int( key_id )
    except:
        resp_data["msg"] = "参数错误"
        resp_data["code"] = -1
        response = make_response( json.dumps( resp_data ), 406 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response     

    key_model = FirstFilterKey.query.filter_by( id=key_id ).first()
    if not key_model:
        resp_data["msg"] = "资源不存在" 
        resp_data["code"] = -1
        response = make_response( json.dumps( resp_data ), 404 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response           

    if "PATCH" == request.method:
        key_name = req_dict.get( "key_name", None )   
        if not key_name:
            req_dict = request.get_json()
            key_name = req_dict.get( "key_name", None )  
        if not key_name:
            resp_data["msg"] = "缺少参数"
            resp_data["code"] = -1
            response = make_response( json.dumps( resp_data ), 404 )
            response.headers["Content-Type"] = "application/json;charset=utf-8"
            return response              

        key_model.key_name= key_name
        db.session.add( key_model )            
        db.session.commit()
        resp_data["data"].append({
            "id": key_model.id,
            "key_name": key_model.key_name
        }) 
        resp_data["count"] = 1     
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
        "code": 0,
        "count": 0,
        "msg": "操作成功~",
        "data": []
    }

    if "GET" == request.method:
        # 实现分页加载
        page = req_dict.get( "page", 1 )
        try:
            page = int( page )
        except:
            resp_data["msg"] = "参数错误"
            resp_data["code"] = -1
            response = make_response( json.dumps( resp_data ), 406 )
            response.headers["Content-Type"] = "application/json;charset=utf-8"
            return response          
        if page < 1:
            page = 1        
        page_size = req_dict.get( "limit", 10 )
        try:
            page_size = int( page_size )
        except:
            resp_data["msg"] = "参数错误"
            resp_data["code"] = -1
            response = make_response( json.dumps( resp_data ), 406 )
            response.headers["Content-Type"] = "application/json;charset=utf-8"           
        offset = ( page - 1 ) * page_size

        number_model_list = SecondFilterGroupnumber.query.order_by( SecondFilterGroupnumber.id.desc() ).offset( offset ).limit( page_size ).all()

        number_data_list = []

        if number_model_list:
            for model in number_model_list:
                number_data_list.append({
                    "id": model.id,
                    "group_number": model.group_number
                })
        
        resp_data["data"] = number_data_list
        resp_data[ "count" ] = db.session.query(func.count( SecondFilterGroupnumber.id )).scalar()

        response = make_response( json.dumps( resp_data ), 200 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response    

    if "POST" == request.method:
        group_number = req_dict.get( "group_number", None )
        if not group_number:
            req_dict = request.get_json()
            group_number = req_dict.get( "group_number", None )
        if not group_number:
            resp_data["msg"] = "参数错误"
            resp_data["code"] = -1
            response = make_response( json.dumps( resp_data ), 404 )
            response.headers["Content-Type"] = "application/json;charset=utf-8"
            return response     
        number_model = SecondFilterGroupnumber.query.filter_by( group_number=group_number ).first()
        if number_model:
            resp_data["msg"] = "QQ群号码已经存在" 
            resp_data["code"] = -1
            response = make_response( json.dumps( resp_data ), 406 )
            response.headers["Content-Type"] = "application/json;charset=utf-8"   
            return response
        else:
            number_model = SecondFilterGroupnumber()
            number_model.group_number = group_number
            db.session.add( number_model )
            db.session.commit()
            resp_data["data"].append({
                "id": number_model.id,
                "group_number": number_model.group_number
            })
            resp_data["count"] = 1
            response = make_response( json.dumps( resp_data ), 200 )
            response.headers["Content-Type"] = "application/json;charset=utf-8"      

            # 更新消息记录表
            MessagesService.update_messages()

            return response        

@route_message.route( "/filter/group_numbers/<number_id>", methods=[ "PATCH", "DELETE" ] )
def patch_delete_group_numbers( number_id ):
    """
    patch /filter/group_numbers/number_id
        更新一个QQ群号码
    delete /filter/group_numbers/number_id
        删除一个QQ群号码       
    """
    # 获取所有请求参数
    req_dict = request.values   

    # 封装响应字段
    resp_data = {
        "code": 0,
        "count": 0,
        "msg": "操作成功~",
        "data": []
    }

    if not number_id:
        resp_data["msg"] = "缺少参数"
        resp_data["code"] = -1
        response = make_response( json.dumps( resp_data ), 404 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response

    try:
        number_id = int( number_id )
    except:
        resp_data["msg"] = "参数错误"
        resp_data["code"] = -1
        response = make_response( json.dumps( resp_data ), 406 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response     

    number_model = SecondFilterGroupnumber.query.filter_by( id=number_id).first()
    if not number_model:
        resp_data["msg"] = "资源不存在" 
        resp_data["code"] = -1
        response = make_response( json.dumps( resp_data ), 404 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response           

    if "PATCH" == request.method:
        group_number = req_dict.get( "group_number", None )   
        if not group_number:
            req_dict = request.get_json()
            group_number = req_dict.get( "group_number", None )   
        if not group_number:
            resp_data["msg"] = "缺少参数"
            resp_data["code"] = -1
            response = make_response( json.dumps( resp_data ), 404 )
            response.headers["Content-Type"] = "application/json;charset=utf-8"
            return response              

        number_model.group_number= group_number
        db.session.add( number_model )            
        db.session.commit()
        resp_data["data"].append({
            "id": number_model.id,
            "group_number": number_model.group_number
        })
        resp_data["count"] = 1     
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
        "code": 0,
        "count": 0,
        "msg": "操作成功~",
        "data": []
    }

    if "GET" == request.method:
        # 实现分页加载
        page = req_dict.get( "page", 1 )
        try:
            page = int( page )
        except:
            resp_data["msg"] = "参数错误"
            resp_data["code"] = -1
            response = make_response( json.dumps( resp_data ), 406 )
            response.headers["Content-Type"] = "application/json;charset=utf-8"
            return response          
        if page < 1:
            page = 1        
        page_size = req_dict.get( "limit", 10 )
        try:
            page_size = int( page_size )
        except:
            resp_data["msg"] = "参数错误"
            resp_data["code"] = -1
            response = make_response( json.dumps( resp_data ), 406 )
            response.headers["Content-Type"] = "application/json;charset=utf-8"           
        offset = ( page - 1 ) * page_size

        number_model_list = SecondFilterQqnumber.query.order_by( SecondFilterQqnumber.id.desc() ).offset( offset ).limit( page_size ).all()

        number_data_list = []

        if number_model_list:
            for model in number_model_list:
                number_data_list.append({
                    "id": model.id,
                    "qq_number": model.qq_number
                })
        
        resp_data["data"] = number_data_list
        resp_data[ "count" ] = db.session.query(func.count( SecondFilterQqnumber.id )).scalar()

        response = make_response( json.dumps( resp_data ), 200 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response      

    if "POST" == request.method:
        qq_number = req_dict.get( "qq_number", None )
        if not qq_number:
            req_dict = request.get_json()
            qq_number = req_dict.get( "qq_number", None )
        if not qq_number:
            resp_data["msg"] = "参数错误"
            resp_data["code"] = -1
            response = make_response( json.dumps( resp_data ), 404 )
            response.headers["Content-Type"] = "application/json;charset=utf-8"
            return response     
        number_model = SecondFilterQqnumber.query.filter_by( qq_number=qq_number ).first()
        if number_model:
            resp_data["msg"] = "QQ号码已经存在" 
            resp_data["code"] = -1
            response = make_response( json.dumps( resp_data ), 406 )
            response.headers["Content-Type"] = "application/json;charset=utf-8"   
            return response
        else:
            number_model = SecondFilterQqnumber()
            number_model.qq_number = qq_number
            db.session.add( number_model )
            db.session.commit()
            resp_data["data"].append({
                "id": number_model.id,
                "qq_number": number_model.qq_number
            })
            resp_data["count"] = 1
            response = make_response( json.dumps( resp_data ), 200 )
            response.headers["Content-Type"] = "application/json;charset=utf-8"         

            # 更新消息记录表
            MessagesService.update_messages()            

            return response  

@route_message.route( "/filter/qq_numbers/<number_id>", methods=[ "PATCH", "DELETE" ] )
def patch_delete_qq_numbers( number_id ):
    """
    patch /filter/qq_numbers/number_id
        更新一个QQ号码
    delete /filter/qq_numbers/number_id
        删除一个QQ号码
    """
    # 获取所有请求参数
    req_dict = request.values   

    # 封装响应字段
    resp_data = {
        "code": 0,
        "count": 0,
        "msg": "操作成功~",
        "data": []
    }

    if not number_id:
        resp_data["msg"] = "缺少参数"
        resp_data["code"] = -1
        response = make_response( json.dumps( resp_data ), 404 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response

    try:
        number_id = int( number_id )
    except:
        resp_data["msg"] = "参数错误"
        resp_data["code"] = -1
        response = make_response( json.dumps( resp_data ), 406 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response     

    number_model = SecondFilterQqnumber.query.filter_by( id=number_id).first()
    if not number_model:
        resp_data["msg"] = "资源不存在" 
        resp_data["code"] = -1
        response = make_response( json.dumps( resp_data ), 404 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response           

    if "PATCH" == request.method:
        qq_number = req_dict.get( "qq_number", None )   
        if not qq_number:
            req_dict = request.get_json()
            qq_number = req_dict.get( "qq_number", None )   
        if not qq_number:
            resp_data["msg"] = "缺少参数"
            resp_data["code"] = -1
            response = make_response( json.dumps( resp_data ), 404 )
            response.headers["Content-Type"] = "application/json;charset=utf-8"
            return response              

        number_model.qq_number= qq_number
        db.session.add( number_model )            
        db.session.commit()
        resp_data["data"].append({
            "id": number_model.id,
            "qq_number": number_model.qq_number
        })
        resp_data["count"] = 1    
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
