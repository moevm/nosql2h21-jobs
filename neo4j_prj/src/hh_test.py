import json

import app
import pathlib
from hh_api import hh_api

api = hh_api.Hh_api()

#res = api.test(49186602)

# res = api.get_vacancy_by_id_raw(49186602)
res = api.get_vacancy_by_name("Аналитик")
print(json.dumps(res, indent = 1, ensure_ascii=False))

#print(res)
if __name__ == "__main__":
    pass
#%%