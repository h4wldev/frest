# -*- coding: utf-8 -*-
import datetime
from flask import jsonify, session

from app import token_auth
from app.models.user_token_model import UserTokenModel


@token_auth.verify_token
def verify_token(token):
    token = UserTokenModel.query\
        .filter(UserTokenModel.token == token)

    if token.count():
        token = token.first()

        if token.expired_at > datetime.datetime.now():
            session['token'] = token.token
            return True

    return False


@token_auth.error_handler
def error_handler():
    return jsonify({'status': 'fail', 'message': '존재하지 않거나 만료된 토큰입니다.'})
