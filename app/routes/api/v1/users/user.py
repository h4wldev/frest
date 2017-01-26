# # -*- coding: utf-8 -*-
from flask import request
from flask_api import status
from flask_restful import Resource

from app import db, token_auth
from app.modules import frest
from app.modules.token import token_is_auth, token_load_with_auth, token_delete_all
from app.modules.frest.serialize import serialize_user
from app.models.user_model import UserModel

_URL = '/users/<prefix>'


class User(Resource):
    @frest.API
    @token_auth.login_required
    def get(self, prefix):
        try:
            if prefix == 'me':
                user_id = token_load_with_auth(request.headers['Authorization'])['user_id']
            else:
                user_id = int(prefix)

            user_query = UserModel.query\
                .filter(UserModel.id == user_id)

            if token_is_auth(request.headers['Authorization'], user_id):
                if user_query.count():
                    user = user_query.first()

                    return serialize_user(user), status.HTTP_200_OK
                else:
                    return "The user does not exist.", status.HTTP_404_NOT_FOUND
            else:
                return "You don't have permission.", status.HTTP_401_UNAUTHORIZED
        except ValueError:
            return "Prefix can only be me or a number.", status.HTTP_400_BAD_REQUEST

    @frest.API
    @token_auth.login_required
    def post(self, prefix):
        try:
            prefix == 'me' or int(prefix)

            return "", status.HTTP_200_OK
        except ValueError:
            return "", status.HTTP_400_BAD_REQUEST

    @frest.API
    @token_auth.login_required
    def delete(self, prefix):
        try:
            if prefix == 'me':
                user_id = token_load_with_auth(request.headers['Authorization'])['user_id']
            else:
                user_id = int(prefix)

            user_query = UserModel.query \
                .filter(UserModel.id == user_id)

            if token_is_auth(request.headers['Authorization'], user_id):
                if user_query.count():
                    token_delete_all(user_id)

                    user = user_query.first()
                    db.session.delete(user)
                    db.session.commit()

                    return None, status.HTTP_200_OK
                else:
                    return "The user does not exist.", status.HTTP_404_NOT_FOUND
            else:
                return "You don't have permission.", status.HTTP_401_UNAUTHORIZED
        except ValueError:
            return "Prefix can only be me or a number.", status.HTTP_400_BAD_REQUEST
