from flask import jsonify

from . import neo_api


# def get(id:int,subareas:bool = True):
#     api = hh_api.Hh_api()
#     area:dataclasses.dataclass = api.get_area(id,subareas)
#     retcode = 200
#     result = []
#     return jsonify(dataclasses.asdict(area)), retcode

def get(id: int):
    area = neo_api.get_area(id)
    if area:
        return jsonify(area), 200
    else:
        return jsonify(area), 204


def post(name: str):
    res = neo_api.create_area(name)
    return jsonify(res), 201


def get_count():
    return neo_api.get_area_count(), 200


def get_list(offset=0, limit=10):
    res = neo_api.get_area_list(offset, limit)
    if res:
        return res, 200
    else:
        return res, 204
