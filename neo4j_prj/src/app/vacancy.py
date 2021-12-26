from flask import jsonify

from . import neo_api


# def get_list(offset:int = 0,limit:int = 100):
#     # api = hh_api.Hh_api()
#     vacancy:dict = neo_api.get_vacancy_list(offset,limit)
#     resp:List[neo4j.graph.Node] = [i[0]._properties for i in vacancy]
#     # nn[0]._properties
#     # dict(nn[0].items())
#     retcode = 200
#     result = []
#     return jsonify(resp), retcode

def get(id: int):
    pass


def get_list(offset: int = 0, limit: int = 100):
    pass


def get_stuff():
    pass


def get(offset: int = 0, limit: int = 100):
    ret_code = 200
    vacancies = neo_api.get_vacancy_list(offset, limit)
    if len(vacancies) == 0: ret_code = 204
    return jsonify(vacancies), ret_code
