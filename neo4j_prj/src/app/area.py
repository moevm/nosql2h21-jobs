import json

import dataclasses
from flask import jsonify
from hh_api import hh_api
from utils.JSON_encoder import json_encoder
from . import neo_api

def get(id:int,subareas:bool = True):
    api = hh_api.Hh_api()
    area:dataclasses.dataclass = api.get_area(id,subareas)
    retcode = 200
    result = []
    return jsonify(dataclasses.asdict(area)), retcode


