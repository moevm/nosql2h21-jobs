from flask import jsonify

from . import neo_api


def get(id: int):
    employer = neo_api.get_employer(id)
    if employer:
        return jsonify(employer), 200
    else:
        return jsonify(employer), 204


def post(name: str):
    res = neo_api.create_employer(name)
    return jsonify(res), 201


def get_count():
    return neo_api.get_employer_count(), 200


def get_list(offset=0, limit=10):
    res = neo_api.get_employer_list(offset, limit)
    if res:
        return res, 200
    else:
        return res, 204
