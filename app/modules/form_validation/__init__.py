# -*- coding: utf-8 -*-
"""
    form validation
    ~~~~~~~~~~~~~~~

    This module checks variables, and you can easily add rules.

    :copyright: (C) 2017 h4wldev@gmail.com
    :license: MIT, see LICENSE for more details.
"""
import re


class Validation:
    def __init__(self):
        self.parameters = {}
        self.error = '알 수 없는 오류입니다.'
        self.rules = {
            'min_length': self.min_length,
            'max_length': self.max_length,
            'between_length': self.between_length,
            'min': self.min,
            'max': self.max,
            'between': self.between,
            'required': self.required,
            'is_email': self.is_email,
            'is_digit': self.is_digit,
            're': self.re,
            'matches': self.matches
        }

    def add_rule(self, key, value, rules):
        self.parameters[key] = {
            'value': value,
            'rules': rules.split('|')
        }

    def check(self):
        for key, value in self.parameters.items():
            for rule in value['rules']:
                try:
                    (name, rule) = rule.split('=')
                    result = self.rules[name](key, value['value'], rule)
                except ValueError:
                    result = self.rules[rule](key, value['value'])

                if not result:
                    return False

        return True

    def error(self):
        return self.error

    def min_length(self, key, value, rule):
        if len(value) < int(rule):
            self.error = '\'' + key + '\'(은)는 ' + rule + '자 이상이여야 합니다.'
            return False

        return True

    def max_length(self, key, value, rule):
        if len(value) > int(rule):
            self.error = '\'' + key + '\'(은)는 ' + rule + '자 이하여야 합니다.'
            return False

        return True

    def between_length(self, key, value, rule):
        (min, max) = rule.split(',')

        if len(value) < int(min) or len(value) > int(max):
            self.error = '\'' + key + '\'(은)는 ' + min + '자 이상, ' + max + '자 이하여야 합니다.'
            return False

        return True

    def min(self, key, value, rule):
        if int(value) < int(rule):
            self.error = '\'' + key + '\'(은)는 ' + rule + ' 이상이여야 합니다.'
            return False

        return True

    def max(self, key, value, rule):
        if int(value) > int(rule):
            self.error = '\'' + key + '\'(은)는 ' + rule + ' 이하여야 합니다.'
            return False

        return True

    def max(self, key, value, rule):
        if int(value) > int(rule):
            self.error = '\'' + key + '\'(은)는 ' + rule + ' 이하여야 합니다.'
            return False

        return True

    def between(self, key, value, rule):
        (min, max) = rule.split(',')

        if int(value) < int(min) or int(value) > int(max):
            self.error = '\'' + key + '\'(은)는 ' + min + ' 이상, ' + max + ' 이하여야 합니다.'
            return False

        return True

    def required(self, key, value):
        if value is None:
            self.error = '\'' + key + '\'(은)는 필수로 입력되어야 합니다.'
            return False

        return True

    def is_email(self, key, value):
        if not re.match(r'[^@]+@[^@]+\.[^@]+', value):
            self.error = '\'' + key + '\'(은)는 이메일 형식이여야 합니다.'
            return False

        return True

    def is_digit(self, key, value):
        try:
            int(value)
            return True
        except ValueError:
            self.error = '\'' + key + '\'(은)는 숫자여야 합니다.'
            return False

    def re(self, key, value, rule):
        if not re.match(rule, value):
            self.error = '\'' + key + '\'가 형식에 맞지 않습니다.'
            return False

        return True

    def matches(self, key, value, rule):
        if not self.parameters[rule]['value'] == value:
            self.error = '\'' + key + '\'(와)과 \'' + rule + '\'이 같지 않습니다.'
            return False

        return True
