# -*- coding: utf-8 -*-
import os
import importlib

from app import api as Api
from app.config import API_VERSION
from app.logger import logging


routes = {}


def load_api_module(path):
    for module in os.listdir(path):
        if os.path.isdir(path + '/' + module):
            load_api_module(path + '/' + module)

        if module == '__init__.py' or module[-3:] != '.py':
            continue

        _path = path.replace(os.path.dirname(__file__), '').replace('/', '.')

        module_name = module[:-3]
        module = importlib.import_module('app.routes' + _path + '.' + module[:-3])

        routes[module_name] = {
            'route': '/api/v' + str(API_VERSION) + module._URL,
            'class': getattr(module, module_name.title().replace('_', ''))
        }


load_api_module(os.path.dirname(__file__) + '/api/v' + str(API_VERSION))

for route in routes.values():
    logging.info('Route is loaded at \'%s\' (class : \'%s\')', route['route'], route['class'].__name__)

    Api.add_resource(route['class'], route['route'])
