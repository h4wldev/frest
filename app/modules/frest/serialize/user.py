# -*- coding: utf-8 -*-
import datetime


def serialize_user(user):
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'permission': user.permission,
        'updated_at': None if user.updated_at is None else user.updated_at.isoformat(),
        'created_at': user.created_at.isoformat()
    }