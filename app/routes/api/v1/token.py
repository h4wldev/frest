# -*- coding: utf-8 -*-
from flask import request
from flask_api import status
from flask_restful import Resource

from app import token_auth
from app.models.user_token_model import token_load_with_auth
from app.modules import frest


_URL = '/token'


class Token(Resource):
    @frest.API
    @token_auth.login_required
    def get(self):
        _return = {
            'header': {
                'scheme': request.headers['Authorization'].split()[0],
                'token': request.headers['Authorization'].split()[1]
            },
            'data': token_load_with_auth(request.headers['Authorization'])
        }

        return _return, status.HTTP_200_OK
