# # -*- coding: utf-8 -*-
import re
import datetime

from flask import request
from flask_api import status
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from app import db, token_auth
from app.models.user_model import UserModel, get_user
from app.models.user_token_model import token_is_auth, token_load_with_auth, token_expire_all, token_delete_all
from app.modules import frest
from app.modules.frest.validate import user as userValidate
from app.modules.frest.serialize.user import serialize_user

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

            if token_is_auth(request.headers['Authorization'], user_id):
                user = get_user(user_id)

                return serialize_user(user), status.HTTP_200_OK
            else:
                return "You don't have permission.", status.HTTP_401_UNAUTHORIZED
        except ValueError:
            return "Prefix can only be me or a number.", status.HTTP_400_BAD_REQUEST

    @frest.API
    @token_auth.login_required
    def put(self, prefix):
        try:
            if prefix == 'me':
                user_id = token_load_with_auth(request.headers['Authorization'])['user_id']
            else:
                user_id = int(prefix)

            user_query = UserModel.query \
                .filter(UserModel.id == user_id)

            if token_is_auth(request.headers['Authorization'], user_id):
                user_permission = token_load_with_auth(request.headers['Authorization'])['permission']

                if user_permission != 'ADMIN' and request.form.get('permission') is not None:
                    return "You don't have permission.", status.HTTP_401_UNAUTHORIZED

                form = userValidate.modificationForm(request.form)

                if form.validate():
                    if user_query.count():
                        user = user_query.first()

                        try:
                            for key, value in request.form.items():
                                if value is not None and value != '':
                                    if key == 'password':
                                        value = generate_password_hash(value)
                                        token_expire_all(user.id)

                                    setattr(user, key, value)

                            user.updated_at = datetime.datetime.now()
                            db.session.commit()
                        except IntegrityError as e:
                            error = str(e).splitlines()[1].replace('DETAIL:  ', '')
                            field, value = map(lambda x: x[1:-1], re.findall(r'\([^)]+\)', error))

                            _return = {
                                'message': "'" + value + "' is already exists.",
                                'field': {
                                    'label': getattr(form, field).label.text,
                                    'name': field
                                }
                            }

                            return _return, status.HTTP_400_BAD_REQUEST

                        return None, status.HTTP_200_OK
                    else:
                        return "The user does not exist.", status.HTTP_404_NOT_FOUND

                for field, errors in form.errors.items():
                    for error in errors:
                        _return = {
                            'message': error,
                            'field': getattr(form, field).label.text
                        }

                        return _return, status.HTTP_400_BAD_REQUEST
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
