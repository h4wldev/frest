# -*- coding: utf-8 -*-
import re

from app.config import DATABASE


def get_exists_error(e):
    field, value = '', ''

    if DATABASE['engine'] == 'postgres':
        error = str(e).splitlines()[1].replace('DETAIL:  ', '')
        field, value = map(lambda x: x[1:-1], re.findall(r'\([^)]+\)', error))
    elif DATABASE['engine'] == 'mysql':
        error = [f[1:-1] for f in re.findall(r'\'[^\']+\'', str(e))]
        value, field = error[0], error[1]

    return field, value
