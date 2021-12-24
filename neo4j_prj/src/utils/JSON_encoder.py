import datetime
from uuid import UUID

import dataclasses
import neo4j
from dataclasses import is_dataclass
import datetime
from uuid import UUID

import dataclasses
import neo4j
from dataclasses import is_dataclass


# dataclasses.is_dataclass(something)

def json_encoder(obj):
    """
    Usage: json.dumps(obj, default = json_encoder)
    :param obj:
    :return:
    """
    if is_dataclass(obj) and not isinstance(obj, type):
        return dataclasses.asdict(obj)
    if isinstance(obj, UUID):
        return str(obj)
    if isinstance(obj, datetime.date) or isinstance(obj, datetime.datetime):
        return obj.isoformat()
    if isinstance(obj, neo4j.graph.Node):
        return dict(obj)
