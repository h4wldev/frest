# -*- coding: utf-8 -*-
from flask_api import status
from flask_restful import Resource

from app import basic_auth
from app.modules import frest
from modules.token import token_generate

END_POINT = '/auth'


class Auth(Resource):
    @frest.API
    @basic_auth.login_required
    def get(self):
        return token_generate(email=basic_auth.username()), status.HTTP_201_CREATED
