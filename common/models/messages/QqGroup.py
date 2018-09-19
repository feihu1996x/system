# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, String
from sqlalchemy.schema import FetchedValue

from application import db


class QqGroup(db.Model):
    __tablename__ = 'qq_group'

    id = db.Column(db.BigInteger, primary_key=True)
    group_name = db.Column(db.String(100), nullable=False, unique=True, server_default=db.FetchedValue())
    group_number = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
