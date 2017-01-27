# -*- coding: utf-8 -*-
from wtforms import Form, StringField, PasswordField, validators


class modificationForm(Form):
    username = StringField('User Name', [
        validators.Optional(),
        validators.Length(min=2, max=20)
    ])
    email = StringField('Email', [
        validators.Optional(),
        validators.Length(min=5),
        validators.Email()
    ])
    password = PasswordField('Password', [
        validators.Optional(),
        validators.Length(min=5)
    ])
