# -*- coding: utf-8 -*-
from flask import jsonify, request
from werkzeug.security import check_password_hash

from app import db, basic_auth
from app.models.user_model import UserModel
from app.models.user_login_history_model import UserLoginHistoryModel


@basic_auth.verify_password
def verify_password(email, password):
    user = UserModel.query\
        .filter(UserModel.email == email)

    accepted = False

    if user.count():
        accepted = check_password_hash(user.first().password, password)

    login_history = UserLoginHistoryModel(
        user_id=user.first().id,
        ip_address=request.remote_addr,
        agent=request.headers.get('User-Agent'),
        accepted=accepted
    )
    db.session.add(login_history)
    db.session.commit()

    return accepted


@basic_auth.error_handler
def error_handler():
    return jsonify({'code': 401, 'status': 'fail', 'message': 'User does not exist or the password does not match.'})
