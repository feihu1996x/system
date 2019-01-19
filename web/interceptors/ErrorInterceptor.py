#!/usr/bin/python3

"""
@file: ErrorInterceptor.py
@brief: 统一错误请求拦截器
@author: feihu1996.cn
@date: 18-10-02
@version: 1.0
"""

import json

from flask import make_response

from application import app


@app.errorhandler( 404 )
def error_404( e ):
    resp_data = {
        "code": 0,
        "count": 0,
        "msg": "操作失败~",
        "data": []
    }    

    app.logger.info( str( e ) )

    resp_data['msg'] = str( e )
    resp_data['code'] = -1

    response = make_response( json.dumps( resp_data ), 404 )
    response.headers["Content-Type"] = "application/json;charset=utf-8"
    return response

@app.errorhandler( 405 )
def error_405( e ):
    resp_data = {
        "code": 0,
        "count": 0,
        "msg": "操作失败~",
        "data": []
    }    

    app.logger.info( str( e ) )

    resp_data['msg'] = str( e )
    resp_data['code'] = -1

    response = make_response( json.dumps( resp_data ), 405 )
    response.headers["Content-Type"] = "application/json;charset=utf-8"
    return response    
