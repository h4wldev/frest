# -*- coding: utf-8 -*-
import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey

from app import db
from app.models.user_model import UserModel


class UserLoginHistoryModel(db.Model):
    __tablename__ = 'user_login_histories'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    ip_address = Column(String(20), nullable=False)
    agent = Column(String(200))
    accepted = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.datetime.now)

    def __init__(self, user_id=None, ip_address=None, agent=None, accepted=None):
        self.user_id = user_id
        self.ip_address = ip_address
        self.agent = agent
        self.accepted = accepted
