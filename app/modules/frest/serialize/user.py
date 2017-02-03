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


def serialize_login_history(history):
    return {
        'id': history.id,
        'ip_address': history.ip_address,
        'agent': history.agent,
        'accepted': history.accepted,
        'created_at': history.created_at.isoformat()
    }