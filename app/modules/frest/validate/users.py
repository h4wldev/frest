# -*- coding: utf-8 -*-
from wtforms import Form, StringField, PasswordField, validators


class RegistrationForm(Form):
    username = StringField('User Name', [
        validators.DataRequired(),
        validators.Length(min=2, max=20)
    ])
    email = StringField('Email', [
        validators.DataRequired(),
        validators.Length(min=5),
        validators.Email()
    ])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=5)
    ])
