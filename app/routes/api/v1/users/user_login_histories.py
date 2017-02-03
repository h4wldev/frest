# # -*- coding: utf-8 -*-
import datetime

from flask import request
from flask_api import status
from flask_restful import Resource

from app import token_auth
from app.config import DEFAULT_URL
from app.models.user_login_history_model import get_login_histories
from app.models.user_token_model import token_is_auth, token_load_with_auth
from app.modules import frest
from app.modules.frest.serialize.user import serialize_login_history

_URL = '/users/<prefix>/login_histories'


class UserLoginHistories(Resource):
    @frest.API
    @token_auth.login_required
    def get(self, prefix):
        page = request.args.get('page', 0, type=int)
        limit = request.args.get('limit', 10, type=int)
        order = request.args.get('order', 'desc')

        try:
            if prefix == 'me':
                user_id = token_load_with_auth(request.headers['Authorization'])['user_id']
            else:
                user_id = int(prefix)

            if token_is_auth(request.headers['Authorization'], user_id):
                _return = {
                    'paging': {
                        'previous': '%s%s?page=%d&limit=%d&order=%s' % (
                            DEFAULT_URL, request.path, page if page < 1 else page - 1, limit, order
                        ),
                        'next': '%s%s?page=%d&limit=%d&order=%s' % (
                            DEFAULT_URL, request.path, page + 1, limit, order
                        )
                    },
                    'data': []
                }

                histories = get_login_histories(user_id, order, page, limit)

                for history in histories:
                    _return['data'].append(serialize_login_history(history))

                return _return, status.HTTP_200_OK
            else:
                return "You don't have permission.", status.HTTP_401_UNAUTHORIZED
        except ValueError:
            return "Prefix can only be me or a number.", status.HTTP_400_BAD_REQUEST
