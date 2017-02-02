# -*- coding: utf-8 -*-
from functools import wraps, partial

from flask import request
from flask_api import status
from flask.wrappers import Response

from app.config import API_ACCEPT_HEADER, API_VERSION


def API(method=None):
    if method is None:
        return partial(API)

    @wraps(method)
    def decorated(*args, **kwargs):
        _return = method(*args, **kwargs)

        if isinstance(_return, Response):
            return _return

        if request.url.find('v' + str(API_VERSION)) > 0:
            try:
                if request.headers['Accept'] == API_ACCEPT_HEADER:
                    ret, code = _return
                else:
                    raise KeyError
            except KeyError:
                ret, code = ("Please check request accept again.", status.HTTP_406_NOT_ACCEPTABLE)
        else:
            ret, code = ("API has been updated. The latest version is v" + str(API_VERSION), status.HTTP_301_MOVED_PERMANENTLY)

        return serialize(ret, code)

    def serialize(ret, code):
        _return = {'code': code}

        if not status.is_success(code):
            _return['status'] = 'fail'

            if ret is not None:
                if isinstance(ret, dict):
                    _return.update(ret)
                else:
                    _return['message'] = ret
        else:
            _return['status'] = 'success'

            if ret is not None:
                if isinstance(ret, dict):
                    _return.update(ret)
                else:
                    _return['data'] = ret

        return _return, code

    return decorated
