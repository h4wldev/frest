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


def get_login_histories(user_id=0, order='desc', page=0, limit=10):
    histories = []

    histories_query = UserLoginHistoryModel.query \
        .filter(UserLoginHistoryModel.user_id == user_id) \
        .order_by(UserLoginHistoryModel.id.asc() if order == 'asc' else UserLoginHistoryModel.id.desc()) \
        .limit(limit) \
        .offset(page * limit)

    for history in histories_query:
        histories.append(history)

    return histories
