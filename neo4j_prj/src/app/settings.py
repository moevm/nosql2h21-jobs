import json
from typing import NamedTuple, Dict
from collections import namedtuple


def read(path: str) -> NamedTuple:
    with open(path,'r') as fp:
        data:Dict = json.load(fp)
    Config_type = namedtuple("config",list(data.keys()))
    config = Config_type(**data)
    return config