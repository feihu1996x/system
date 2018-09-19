# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, String
from sqlalchemy.schema import FetchedValue

from application import db


class SecondFilterGroupnumber(db.Model):
    __tablename__ = 'second_filter_groupnumber'

    id = db.Column(db.BigInteger, primary_key=True)
    group_number = db.Column(db.String(100), nullable=False, unique=True, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
