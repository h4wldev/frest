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


def get_user(user_id=0):
    user_query = UserModel.query \
        .filter(UserModel.id == user_id).first()

    return user_query


def get_users(order='desc', page=0, limit=10):
    users = []

    users_query = UserModel.query \
        .order_by(UserModel.id.asc() if order == 'asc' else UserModel.id.desc()) \
        .limit(limit) \
        .offset(page * limit)

    for user in users_query:
        users.append(user)

    return users
