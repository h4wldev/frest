# # -*- coding: utf-8 -*-
import datetime

from flask import request
from flask_api import status
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

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
            if prefix == 'me':
                user_id = token_load_with_auth(request.headers['Authorization'])['user_id']
            else:
                user_id = int(prefix)

            user_query = UserModel.query \
                .filter(UserModel.id == user_id)

            if token_is_auth(request.headers['Authorization'], user_id):
                if user_query.count():
                    user = user_query.first()

                    try:
                        for key, value in request.form.items():
                            setattr(user, key, value)

                        user.updated_at = datetime.datetime.now()

                        db.session.commit()
                    except IntegrityError as e:
                        error = str(e).splitlines()[1].replace('DETAIL:  ', '')

                        return error, status.HTTP_400_BAD_REQUEST

                    return None, status.HTTP_200_OK
                else:
                    return "The user does not exist.", status.HTTP_404_NOT_FOUND
            else:
                return "You don't have permission.", status.HTTP_401_UNAUTHORIZED

        except ValueError:
            return "Prefix can only be me or a number.", status.HTTP_400_BAD_REQUEST

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
