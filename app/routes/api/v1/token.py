# -*- coding: utf-8 -*-
from flask import request
from flask_api import status
from flask_restful import Resource

from app import token_auth
from app.modules import frest
from app.modules.token import token_load


END_POINT = '/token'


class Token(Resource):
    @frest.API
    @token_auth.login_required
    def get(self):
        print token_load(request.headers['Authorization'])
        return None, status.HTTP_200_OK
