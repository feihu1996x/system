# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, String, Text
from sqlalchemy.schema import FetchedValue

from application import db


class OriginalMessage(db.Model):
    __tablename__ = 'original_messages'

    id = db.Column(db.BigInteger, primary_key=True)
    group_id = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    sender_name = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    qq_number = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    content = db.Column(db.Text, nullable=False)
    send_time = db.Column(db.DateTime, nullable=False)
    fingerprint = db.Column(db.String(32), nullable=False, unique=True, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
