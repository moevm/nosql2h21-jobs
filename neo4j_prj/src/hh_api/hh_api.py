import json
from typing import Optional, List

import requests
from dataclasses import dataclass


# from attr import dataclass
@dataclass
class Area(object):
    id: int
    parent_id: Optional[int]
    name: str
    areas: List[int]



class Hh_api(object):
    def __init__(self, api_domain: str = "api.hh.ru"):
        self.api = api_domain

    def get_area(self, id: int, subareas: bool = False, max_depth: int = -1) -> Area:
        """
        https://github.com/hhru/api/blob/master/docs/areas.md
        :return:
        """
        req = requests.get(f'https://{self.api}/areas/{id}')
        data = json.loads(req.content.decode())
        req.close()
        area = Area(id=int(data["id"]),
                    parent_id=int(data["parent_id"]) if data["parent_id"] is not None else None,
                    name=data["name"],
                    areas=[])
        area.areas.extend(map(lambda x: int(x["id"]), data["areas"]))
        return area


    def get_currencies(self):
        address = f"https://api.hh.ru/dictionaries"
        data = json.loads(requests.get(address).content.decode())
        data = data["currency"]
        res = []
        for val in data:
            res.append({"name": val["code"]})
        return res

    def get_employer(self):
        address = f"https://api.hh.ru/vacancies"
        data = json.loads(requests.get(address).content.decode())
        data = data["items"]
        res = []
        for val in data:
            res.append({"id": int(val["employer"]["id"]), "name": val["employer"]["name"]})
        return res

    def get_schedule(self):
        address = f"https://api.hh.ru/vacancies"
        data = json.loads(requests.get(address).content.decode())
        data = data["items"]
        res = []
        for val in data:
            if ({"id": val["schedule"]["id"], "name": val["schedule"]["name"]}) not in res:
                res.append({"id": val["schedule"]["id"], "name": val["schedule"]["name"]})
        return res

    '''def get_vacancy_type(self):
        address = f"https://api.hh.ru/vacancies"
        data = json.loads(requests.get(address).content.decode())
        data = data["items"]
        res = []
'''

