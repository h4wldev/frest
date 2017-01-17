# -*- coding: utf-8 -*-
"""
    flask restful api frame
    ~~~~~~~~~~~~~~~~~~~~~~~

    This project is the frame of the restful api server created with flask.

    :copyright: (C) 2017 h4wldev@gmail.com
    :license: MIT, see LICENSE for more details.
"""
from flask import Flask
from flask_restful import Api
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask_sqlalchemy import SQLAlchemy

from app.config import DATABASE, TOKEN_SCHEME


# API SERVER APPLICATION
app = Flask(__name__)
api = Api(app)


# DATABASE
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


# BASIC AUTH AUTHENTICATION
basic_auth = HTTPBasicAuth()


# TOKEN AUTH AUTHENTICATION
token_auth = HTTPTokenAuth(scheme=TOKEN_SCHEME)
