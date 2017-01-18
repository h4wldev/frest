# -*- coding: utf-8 -*-
from flask_api import status
from flask_restful import Resource

from app import basic_auth
from app.modules import frest
from app.modules.token import token_generate

_URL = '/auth'


class Auth(Resource):
    @frest.API
    @basic_auth.login_required
    def get(self):
        _return = {
            'data': token_generate(email=basic_auth.username())
        }

        return _return, status.HTTP_201_CREATED
