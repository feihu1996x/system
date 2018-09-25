# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Integer, String, Text
from sqlalchemy.schema import FetchedValue

from application import db


class Procurement(db.Model):
    __tablename__ = 'procurement'

    id = db.Column(db.BigInteger, primary_key=True)
    fingerprint = db.Column(db.String(32), nullable=False, unique=True, server_default=db.FetchedValue())
    posted = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    name = db.Column(db.String(1000), nullable=False, server_default=db.FetchedValue())
    field = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    desc = db.Column(db.Text, nullable=False)
    spend = db.Column(db.String(1000), nullable=False, server_default=db.FetchedValue())
    completed_time = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    publish_time = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    delivery_method = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    publisher = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    contact_information = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    source = db.Column(db.String(1000), nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
