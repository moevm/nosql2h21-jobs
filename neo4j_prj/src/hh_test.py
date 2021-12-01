import json

import app
import pathlib
from hh_api import hh_api

api = hh_api.Hh_api()

#res = api.test(49186602)

res = api.test_valuta()
print(json.dumps(res, indent = 1, ensure_ascii=False))
#print("AAAAAAaaa")
#print(res)
if __name__ == "__main__":
    pass
#%%