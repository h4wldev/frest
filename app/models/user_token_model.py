# -*- coding: utf-8 -*-
import hashlib
import datetime

from flask import request
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app import db
from app.config import TOKEN_SCHEME, TOKEN_EXPIRE_TIME, APP_SECRET_KEY
from app.models.user_model import UserModel, get_user


class UserTokenModel(db.Model):
    __tablename__ = 'user_tokens'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    token = Column(String(500), nullable=False)
    hashed = Column(String(100), unique=True, nullable=False)
    ip_address = Column(String(45))
    created_at = Column(DateTime, default=datetime.datetime.now)
    expired_at = Column(DateTime)

    def __init__(self, user_id=None, token=None, hashed=None, expired_at=None):
        self.user_id = user_id
        self.token = token
        self.hashed = hashed
        self.ip_address = request.remote_addr
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
        'scheme': TOKEN_SCHEME
    }

    token = Serializer(APP_SECRET_KEY, expires_in=expires_in).dumps(data)
    data['token'] = hashlib.sha384(token).hexdigest()

    user_token = UserTokenModel(
        user_id=user.id,
        token=token,
        hashed=data['token'],
        expired_at=expired_at
    )

    db.session.add(user_token)
    db.session.commit()

    return data


def token_load(hashed=''):
    user_token = UserTokenModel.query \
        .filter(UserTokenModel.hashed == hashed)\
        .first()

    data = Serializer(APP_SECRET_KEY).loads(user_token.token)
    data['expired_at'] = user_token.expired_at.isoformat()
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


def token_expire_with_token(hashed=''):
    user_token = UserTokenModel.query\
        .filter(UserTokenModel.hashed == hashed, UserTokenModel.ip_address == request.remote_addr) \
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


def token_expire_extension(hashed=''):
    user_token = UserTokenModel.query\
        .filter(UserTokenModel.hashed == hashed, UserTokenModel.ip_address == request.remote_addr) \
        .first()

    user_token.expired_at = datetime.datetime.now() + datetime.timedelta(seconds=TOKEN_EXPIRE_TIME)
    db.session.commit()


def token_exist(hashed=''):
    user_token = UserTokenModel.query\
        .filter(UserTokenModel.hashed == hashed, UserTokenModel.ip_address == request.remote_addr)

    return user_token.count()
