from flask import jsonify

from . import neo_api


def get():
    res = neo_api.get_schedule()
    if res:
        return jsonify(res), 200
    else:
        return jsonify(res), 204
