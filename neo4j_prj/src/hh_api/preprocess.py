from typing import Dict


def preproc_vacancy_peel(vacancy: Dict):
    val = vacancy
    snippet = val.get("snippet") or {}
    res = {"id": int(val.get("id")),
           "name": val["name"],
           "has_test": val["has_test"],
           "salary_from": int(val["salary"]["from"]) if val["salary"] and val["salary"][
               "from"] is not None else None,
           "salary_to": int(val["salary"]["to"]) if val["salary"] and val["salary"][
               "to"] is not None else None,
           "published_at": val["published_at"],
           "created_at": val["created_at"],
           "requirement": snippet.get("requirement"),
           "responsibility": snippet.get("responsibility")
           }
    return res


def preproc_vacancy_get_employer(vacancy: Dict):
    val = vacancy
    res = {"id": int(val["employer"]["id"]), "name": val["employer"]["name"]}
    return res


def preproc_vacancy_get_type(vacancy: Dict):
    val = vacancy
    res = {"id": val["type"]["id"], "name": val["type"]["name"]}
    return res


def preproc_vacancy_get_area(vacancy: Dict):
    val = vacancy
    area = val["area"]
    res = {"id": int(area["id"]), "name": area["name"]}
    return res


def preproc_vacancy_get_schedule(vacancy: Dict):
    val = vacancy
    schedule = val["schedule"]
    res = {"id": schedule["id"], "name": schedule["name"]}
    return res


def preproc_vacancy_get_currency(vacancy: Dict):
    val = vacancy
    salary = val["salary"]
    if not salary:
        res = {"name":"NONE"}
    else:
        res = {"name": salary["currency"]}
    return res


def preproc_vacancy(vacancy: Dict):
    res = {"area": preproc_vacancy_get_area(vacancy),
           "currency": preproc_vacancy_get_currency(vacancy),
           "employer": preproc_vacancy_get_employer(vacancy),
           "schedule": preproc_vacancy_get_schedule(vacancy),
           "type": preproc_vacancy_get_type(vacancy),
           "vacancy": preproc_vacancy_peel(vacancy)}
    return res
