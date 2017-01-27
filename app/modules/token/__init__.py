# -*- coding: utf-8 -*-
import datetime

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app import db
from app.config import APP_SECRET_KEY, TOKEN_SCHEME, TOKEN_EXPIRE_TIME
from app.models.user_model import get_user
from app.models.user_token_model import UserModel, UserTokenModel


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


def token_expire_with_id(user_id=0):
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
