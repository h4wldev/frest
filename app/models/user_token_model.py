# -*- coding: utf-8 -*-
import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app import db
from app.config import TOKEN_SCHEME, TOKEN_EXPIRE_TIME, APP_SECRET_KEY
from app.models.user_model import UserModel, get_user


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


def token_generate(email=None, expires_in=TOKEN_EXPIRE_TIME):
    user = UserModel.query\
        .filter(UserModel.email == email) \
        .first()

    created_at = datetime.datetime.now()
    expired_at = created_at + datetime.timedelta(seconds=expires_in)

    data = {
        'user_id': user.id,
        'created_at': created_at.isoformat(),
        'expired_at': expired_at.isoformat(),
        'expires_in': expires_in,
        'scheme': TOKEN_SCHEME
    }

    data['token'] = Serializer(APP_SECRET_KEY, expires_in=expires_in).dumps(data)

    user_token = UserTokenModel(
        user_id=user.id,
        token=data['token'],
        expired_at=expired_at
    )

    db.session.add(user_token)
    db.session.commit()

    return data


def token_load(token=''):
    data = Serializer(APP_SECRET_KEY).loads(token)
    data['permission'] = get_user(data['user_id']).permission

    return data


def token_load_with_auth(auth=None):
    return token_load(auth.split()[1])


def token_is_auth(_auth=None, user_id=0):
    if _auth is not None:
        data = token_load_with_auth(_auth)

        if data['permission'] == 'ADMIN' or data['user_id'] == user_id:
            if data['expired_at'] > datetime.datetime.now().isoformat():
                return True

    return False


def token_expire_with_token(token=''):
    user_token = UserTokenModel.query\
        .filter(UserTokenModel.token == token) \
        .first()

    user_token.expired_at = datetime.datetime.now()
    db.session.commit()


def token_expire_all(user_id=0):
    user_tokens = UserTokenModel.query\
        .filter(UserTokenModel.user_id == user_id)

    for user_token in user_tokens:
        if user_token.expired_at > datetime.datetime.now():
            user_token.expired_at = datetime.datetime.now()

    db.session.commit()


def token_delete_all(user_id=0):
    user_tokens = UserTokenModel.query \
        .filter(UserTokenModel.user_id == user_id)

    for user_token in user_tokens:
        db.session.delete(user_token)

    db.session.commit()
