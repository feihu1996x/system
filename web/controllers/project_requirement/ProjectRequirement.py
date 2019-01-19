#!/usr/bin/python3

"""
@file: ProjectRequirement.py
@brief: 项目需求蓝图控制器
@author: feihu1996.cn
@date: 18-10-10
@version: 1.0
"""

import json

from flask import Blueprint, make_response, request

from application import app, db
from common.models.project_requirement.ProjectRequirement import \
    ProjectRequirement

route_project_requirement = Blueprint( "project_requirement", __name__ )

@route_project_requirement.route( "/",  methods=[ "POST","GET" ] )
def get_post_project_requirement():
    """
    post /project_requirement/
        新增项目需求
    get /project_requirement/
        获取所有项目需求
    """
    req_dict = request.get_json()  # 获取所有请求参数

    # 封装响应
    resp_data = {
        "code": 0,
        "count": 0,
        "msg": "操作成功~",
        "data": []
    }  

    if "POST" == request.method:  
        """
        新增项目需求
        """
        title = req_dict.get( 'title', None )  # 项目标题        
        url = req_dict.get( 'url', None )  # 项目链接
        category = req_dict.get( 'category', None )  # 项目类别

        if not title or not url or not category:
            resp_data["msg"] = "参数错误"       
            resp_data["code"] = -1
            response = make_response( json.dumps( resp_data ), 400 )
            response.headers["Content-Type"] = "application/json;charset=utf-8"
            return response    

        project_requirement_model = ProjectRequirement()
        project_requirement_model.title = title
        project_requirement_model.url = url
        project_requirement_model.category = category
        db.session.add( project_requirement_model )
        db.session.commit()

        resp_data["data"].append({
            "id": project_requirement_model.id,
            "title": project_requirement_model.title,
            "url": project_requirement_model.url,
            "category": project_requirement_model.category
        })
        resp_data["count"] = 1
        response = make_response( json.dumps( resp_data ), 200 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response      

    if "GET" == request.method:
        """
        获取所有项目需求
        """
        app.logger.info( "get all project" )
        project_requirement_model_list = ProjectRequirement.query.order_by( "-updated_time" ).all()
        app.logger.info( "项目需求列表的长度为：%d" %( len( project_requirement_model_list ) ) )
        project_requirement_data_list = list()
        for project_requirement_model in project_requirement_model_list:
            project_requirement_data_list.append({
                "title": project_requirement_model.title,
                "url": project_requirement_model.url,
                "category": project_requirement_model.category
            })
        resp_data["count"] = len( project_requirement_data_list )
        resp_data["data"] = project_requirement_data_list
        response = make_response( json.dumps( resp_data ), 200 )
        response.headers["Content-Type"] = "application/json;charset=utf-8"
        return response            
