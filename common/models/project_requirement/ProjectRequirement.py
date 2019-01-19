# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue

from application import db


class ProjectRequirement(db.Model):
    __tablename__ = 'project_requirement'

    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(300), nullable=False, server_default=db.FetchedValue(), doc="项目标题")
    url = db.Column(db.String(300), nullable=False, server_default=db.FetchedValue(), doc="项目链接")
    category = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue(), doc="项目类别")
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), doc="最后一次更新时间")
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), doc="插入时间")
