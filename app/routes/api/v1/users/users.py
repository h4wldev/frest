# # -*- coding: utf-8 -*-
from flask import request
from flask_api import status
from flask_restful import Resource
from werkzeug.security import generate_password_hash

from app import db, token_auth
from app.modules import frest
from app.modules.token import token_is_auth, token_load
from app.modules.form_validation import Validation
from app.modules.frest.serialize import serialize_user
from app.models.user_model import UserModel

END_POINT = '/users'


class Users(Resource):
    @frest.API
    @token_auth.login_required
    def get(self):
        page = request.args.get('page', 0, type=int)
        limit = request.args.get('limit', 10, type=int)

        if token_is_auth(request.headers['Authorization']):
            users = []

            users_query = UserModel.query \
                .order_by(UserModel.id.desc()) \
                .limit(limit) \
                .offset(page * limit)

            for user in users_query:
                users.append(serialize_user(user))

            return users, status.HTTP_200_OK

        return 'UNAUTHORIZED', status.HTTP_401_UNAUTHORIZED

    @frest.API
    def post(self):
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        email = request.form.get('email', None)

        validation = Validation()

        validation.add_rule('이름', username, 'required|min_length=2')
        validation.add_rule('패스워드', password, 'required|min_length=5')
        validation.add_rule('이메일', email, 'required|is_email')

        if validation.check():
            is_email = UserModel.query \
                .filter(UserModel.email == email) \
                .count()

            if not is_email:
                user = UserModel(
                    username=username,
                    password=generate_password_hash(password),
                    email=email
                )
                db.session.add(user)
                db.session.commit()

                return None, status.HTTP_201_CREATED
            else:
                return '이미 존재하는 이메일입니다.', status.HTTP_400_BAD_REQUEST

        return validation.error, status.HTTP_400_BAD_REQUEST
