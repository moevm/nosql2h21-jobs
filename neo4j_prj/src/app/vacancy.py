import json
from typing import List

import dataclasses
import neo4j
from flask import jsonify
from hh_api import hh_api
from utils.JSON_encoder import json_encoder
from . import neo_api

def get_list(offset:int = 0,limit:int = 100):
    # api = hh_api.Hh_api()
    vacancy:dict = neo_api.get_vacancy(offset,limit)
    resp:List[neo4j.graph.Node] = [i[0]._properties for i in vacancy]
    # nn[0]._properties
    # dict(nn[0].items())
    retcode = 200
    result = []
    return jsonify(resp), retcode


