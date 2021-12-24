import json

from hh_api import hh_api
from neo_api import neo_api
from utils.JSON_encoder import json_encoder

api = hh_api.Hh_api()
napi = neo_api.Neo_api()
# res = api.test(49186602)

# res = api.get_vacancy_by_id_raw(49186602)
# res = api.get_vacancy_by_name("Аналитик")
res = napi.get_employer_list(offset=15, limit=10)
print(json.dumps(res, indent=1, ensure_ascii=False, default=json_encoder))

# print(res)
if __name__ == "__main__":
    pass
# %%
