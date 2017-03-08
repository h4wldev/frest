# -*- coding: utf-8 -*-
import datetime
from flask import jsonify, request

from app import token_auth
from app.models.user_token_model import UserTokenModel


@token_auth.verify_token
def verify_token(hashed):
    token = UserTokenModel.query\
        .filter(UserTokenModel.hashed == hashed, UserTokenModel.ip_address == request.remote_addr)

    if token.count():
        token = token.first()

        if token.expired_at > datetime.datetime.now():
            return True

    return False


@token_auth.error_handler
def error_handler():
    return jsonify({'code': 401, 'status': 'fail', 'message': 'Token that does not exist or has expired.'})
