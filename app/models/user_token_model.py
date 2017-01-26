# -*- coding: utf-8 -*-
import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from app import db
from app.models.user_model import UserModel


class UserTokenModel(db.Model):
    __tablename__ = 'user_tokens'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    token = Column(String(500), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    expired_at = Column(DateTime)

    def __init__(self, user_id=None, token=None, created_at=None, expired_at=None):
        self.user_id = user_id
        self.token = token
        self.created_at = created_at
        self.expired_at = expired_at
