# -*- coding: utf-8 -*-
import logging

from app.config import ENVIRONMENT, LOGGER_FORMAT


if ENVIRONMENT == 'development':
    level = logging.DEBUG
else:
    level = logging.INFO

logging.basicConfig(format=LOGGER_FORMAT, level=level)
