# -*- coding: utf-8 -*-
from flask import Flask
from flask_cors import CORS, cross_origin
from flask_restful import Api
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask_sqlalchemy import SQLAlchemy

from app.config import DATABASE_URI, TOKEN_SCHEME


# API SERVER APPLICATION
app = Flask(__name__)
CORS(app)
api = Api(app)


# DATABASE
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


# TOKEN AUTH AUTHENTICATION
token_auth = HTTPTokenAuth(scheme=TOKEN_SCHEME)
