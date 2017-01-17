# -*- coding: utf-8 -*-
from flask import jsonify
from werkzeug.security import check_password_hash

from app import basic_auth
from app.models.user_model import UserModel


@basic_auth.verify_password
def verify_password(email, password):
    user = UserModel.query\
        .filter(UserModel.email == email)

    if user.count():
        return check_password_hash(user.first().password, password)

    return False


@basic_auth.error_handler
def error_handler():
    return jsonify({'code': 401, 'status': 'fail', 'message': '존재하지 않는 유저이거나 패스워드가 맞지 않습니다.'})