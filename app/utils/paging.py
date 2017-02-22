# -*- coding: utf-8 -*-
import urllib

from flask import request


def get_url(page=0):
    values = request.args.to_dict()
    values.update({'page': page})

    return request.base_url + '?' + urllib.urlencode(values)


def get_urls():
    page = request.args.get('page', 0, type=int)

    return {
        'previous': get_url(0 if page < 1 else page - 1),
        'next': get_url(page + 1)
    }
