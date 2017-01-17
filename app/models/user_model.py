# -*- coding: utf-8 -*-
import datetime
from sqlalchemy import Column, Integer, String, DateTime

from app import db


class UserModel(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    permission = Column(String(255), nullable=False, default='USER')
    updated_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.datetime.now)

    def __init__(self, username=None, email=None, password=None, permission=None, updated_at=None):
        self.username = username
        self.email = email
        self.password = password
        self.permission = permission
        self.updated_at = updated_at
