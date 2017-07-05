#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import re
from bottle import Bottle, run, get, request, HTTPResponse, install
from needle_seed import search
import id_seed

from bottlelog import LoggingPlugin
from logging.handlers import TimedRotatingFileHandler
from rngapi_logging import log_to_logger


install(log_to_logger)


def create_header():
    return {'X-RNGAPI-Media-Type': 'RNGAPI.v0'}


def create_response(status, header, body):
    res = HTTPResponse(status=status)
    res.body = body
    for k, v in header.items():
        res.set_header(k, v)

    return res


def error(value, resource, code):
    body = {}
    body['message'] = 'Validation Failed'
    body['errors'] = {
        'value': value,
        'resource': resource,
        'code': code
    }
    header = create_header()
    return create_response(422, header, body)


@get('/gen7/sfmt/seed/id')
def seed_id():
    resource = '/gen7/sfmt/seed/id'
    header = create_header()
    body = {}
    needle = request.query.get('needle')

    if needle is None:
        return error(needle, resource, 'invalid')
    if not len(needle.split(',')) in range(8, 21):
        return error(needle, resource, 'the number of needle should be between 8 and 20')
    if not set(needle).issubset(set("0123456789,")):
        return error(needle, resource, 'needle should be only number')
    if not all([int(x) in range(0, 17) for x in re.findall(r"\d+", needle)]):
        return error(needle, resource, 'needle should be between 0 and 16')


    results = id_seed.search(needle)
    body['results'] = results

    return create_response(200, header, body)


@get('/gen7/sfmt/seed')
def seed():
    resource = '/gen7/sfmt/seed'

    needle = request.query.get('needle')
    if needle is None:
        return error(needle, resource, 'invalid')
    if not len(needle.split(',')) in range(8, 16):
        return error(needle, resource, 'the number of needle should be between 8 and 15')
    if not all([x in map(str, range(0, 17)) for x in needle.split(',')]):
        return error(needle, resource, 'needle should be between 0 and 16')

    body = {}

    results = search('{} {}'.format(
        len(needle.split(',')), needle.replace(',', ' ')))
    body['results'] = [
        {'seed': x[0], 'encoded_needle': x[1], 'step': 417} for x in results]

    header = create_header()
    return create_response(200, header, body)

if __name__ == '__main__':
    run(host='0.0.0.0', server='paste',
        port=19937, debug=True, reloader=False)
