from flask import jsonify

from . import neo_api


def get():
    res = neo_api.get_currencies()
    if res:
        return jsonify(res), 200
    else:
        return jsonify(res), 204


def post(name: str):
    res = neo_api.create_currency(name)
    if res:
        return jsonify(res), 201
    else:
        return jsonify(res), 208
