# -*- coding: utf-8 -*-
from flask_api import status
from flask_restful import Resource

from app.modules import frest


_URL = '/'


class Index(Resource):
    @frest.API
    def get(self):
        return None, status.HTTP_200_OK
