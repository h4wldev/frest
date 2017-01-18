# -*- coding: utf-8 -*-
from flask import request
from flask_api import status
from flask_restful import Resource

from app import token_auth
from app.modules import frest
from app.modules.token import token_load


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
            'data': token_load(request.headers['Authorization'])
        }

        return _return, status.HTTP_200_OK
