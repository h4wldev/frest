# # -*- coding: utf-8 -*-
from flask import request
from flask_api import status
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from app import db, token_auth
from app.config import DEFAULT_URL
from app.models.user_model import UserModel
from app.modules import frest
from app.modules.frest.validate import users
from app.modules.frest.serialize import serialize_user
from app.modules.token import token_is_auth

_URL = '/users'


class Users(Resource):
    @frest.API
    @token_auth.login_required
    def get(self):
        page = request.args.get('page', 0, type=int)
        limit = request.args.get('limit', 10, type=int)
        order = request.args.get('order', 'desc')

        if token_is_auth(request.headers['Authorization']):
            _return = {
                'paging': {
                    'previous': '%s%s?page=%d&limit=%d&order=%s' % (
                        DEFAULT_URL, request.path, page if page < 1 else page - 1, limit, order
                    ),
                    'next': '%s%s?page=%d&limit=%d&order=%s' % (
                        DEFAULT_URL, request.path, page + 1, limit, order
                    )
                },
                'data': []
            }

            users_query = UserModel.query \
                .order_by(UserModel.id.asc() if order == 'asc' else UserModel.id.desc()) \
                .limit(limit) \
                .offset(page * limit)

            for user in users_query:
                _return['data'].append(serialize_user(user))

            return _return, status.HTTP_200_OK

        return "You don't have permission.", status.HTTP_401_UNAUTHORIZED

    @frest.API
    def post(self):
        email = request.form.get('email', None)
        username = request.form.get('username', None)
        password = request.form.get('password', None)

        form = users.RegistrationForm(request.form)

        if form.validate():
            exist_email = UserModel.query \
                .filter(UserModel.email == email) \
                .count()

            exist_username = UserModel.query \
                .filter(UserModel.username == username) \
                .count()

            if not exist_email:
                if not exist_username:
                    try:
                        user = UserModel(
                            username=username,
                            password=generate_password_hash(password),
                            email=email
                        )
                        db.session.add(user)
                        db.session.commit()
                    except IntegrityError as e:
                        error = str(e).splitlines()[1].replace('DETAIL:  ', '')

                        return error, status.HTTP_400_BAD_REQUEST

                    return None, status.HTTP_201_CREATED
                else:
                    return "Username already exists.", status.HTTP_400_BAD_REQUEST
            else:
                return "Email already exists.", status.HTTP_400_BAD_REQUEST

        for field, errors in form.errors.items():
            for error in errors:
                _return = {
                    'message': error,
                    'field': getattr(form, field).label.text
                }

                return _return, status.HTTP_400_BAD_REQUEST
