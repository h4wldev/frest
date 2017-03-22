# -*- coding: utf-8 -*-
import re

from flask import request
from flask_api import status
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from app import db, token_auth
from app.config import DEFAULT_URL
from app.models.user_model import UserModel, get_users
from app.models.user_token_model import token_is_auth
from app.modules import frest
from app.modules.frest.api.error import get_exists_error
from app.modules.frest.validate import users as usersValidate
from app.modules.frest.serialize.user import serialize_user
from app.utils import paging

_URL = '/users'


class Users(Resource):

    """
        @api {get} /users Get users information
        @apiName Users Info
        @apiGroup Users

        @apiHeader {String} Authorization Access token.
        @apiHeaderExample {json} Header-Example:
          {
            "Authorization": "304924"
          }

        @apiParam {int} page Paging number.
        @apiParam {int} limit Result limit.

        @apiSuccess (200) {String} data Users data.
        @apiError (401) UnAuthorized You don't have permission.

        """

    @frest.API
    @token_auth.login_required
    def get(self):
        page = request.args.get('page', 0, type=int)
        limit = request.args.get('limit', 10, type=int)
        order = request.args.get('order', 'desc')

        if token_is_auth(request.headers['Authorization']):
            _return = {
                'paging': paging.get_urls(),
                'data': []
            }

            users = get_users(order, page, limit)

            for user in users:
                _return['data'].append(serialize_user(user))

            return _return, status.HTTP_200_OK

        return "You don't have permission.", status.HTTP_401_UNAUTHORIZED

    """
       @api {post} /users Users SignUp
       @apiName SignUp
       @apiGroup Users

       @apiParam {String} email User's email.
       @apiParam {String} username User's username.
       @apiParam {String} password User's password.

       @apiSuccess (201) {String} data Users data.

       @apiError (400) BadRequests BadRequest with error message
       @apiErrorExample {json} Error-BadRequest-Already exists:
           HTTP /1.1 400 BadRequest
           {
               'message': "'" + value + "' is already exists.",
                   'field': {
                       'label': getattr(form, field).label.text,
                       'name': field
                   }
           }

       @apiErrorExample {json} Error-BadRequest-Invalid data format:
           HTTP /1.1 400 BadRequest
           {
               'message': error,
               'field' : invalid field
           }
       """

    @frest.API
    def post(self):
        email = request.form.get('email', None)
        username = request.form.get('username', None)
        password = request.form.get('password', None)

        form = usersValidate.RegistrationForm(request.form)

        if form.validate():
            try:
                user = UserModel(
                    username=username,
                    password=generate_password_hash(password),
                    email=email
                )
                db.session.add(user)
                db.session.commit()
            except IntegrityError as e:
                field, value = get_exists_error(e)

                _return = {
                    'message': "'" + value + "' is already exists.",
                    'field': {
                        'label': getattr(form, field).label.text,
                        'name': field
                    }
                }

                return _return, status.HTTP_400_BAD_REQUEST

            return None, status.HTTP_201_CREATED

        for field, errors in form.errors.items():
            for error in errors:
                _return = {
                    'message': error,
                    'field': getattr(form, field).label.text
                }

                return _return, status.HTTP_400_BAD_REQUEST
