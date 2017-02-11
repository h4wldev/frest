# -*- coding: utf-8 -*-
from flask import request
from flask_api import status
from flask_restful import Resource

from app import token_auth
from app.models.user_token_model import token_load, token_expire_extension, token_exist
from app.modules import frest


_URL = '/token'


class Token(Resource):
    @frest.API
    def get(self):
        _type = request.args.get('type', None)
        hashed = request.args.get('token', None)

        if _type == 'extension':
            if hashed and token_exist(hashed):
                token_expire_extension(hashed)

                _return = {
                    'data': token_load(hashed)
                }

                return _return, status.HTTP_200_OK
            else:
                _return = {
                    'message': 'The token must be entered as required.'
                }
                return _return, status.HTTP_400_BAD_REQUEST

        return None, status.HTTP_400_BAD_REQUEST
