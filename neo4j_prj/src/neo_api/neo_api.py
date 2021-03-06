import base64
import contextlib
import datetime
import io
import json
import random
import sys
import time
from time import sleep
from typing import List, Dict

from flask import request
from neo4j import GraphDatabase

from hh_api import preprocess as hh_prep


@contextlib.contextmanager
def nostdout():
    save_stdout = sys.stdout
    sys.stdout = io.BytesIO()
    yield
    sys.stdout = save_stdout


class Neo_api(object):
    def __init__(self, host: str = "localhost", port: int = 7687, user: str = "neo4j", pwd: str = "admin",
                 timeout_sec: float = 7):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.uri = f"bolt://{self.host}:{self.port}"
        self.driver = None
        t = time.time()
        while not self.driver and time.time() - t <= timeout_sec:
            try:
                with nostdout():
                    self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.pwd))
            except:
                sleep(1)
        if not self.driver:
            raise Exception(f"Neo4j connection timed out after {timeout_sec} sec")

    def do_nothing(self):
        pass

    @staticmethod
    def dict_to_neo(_dict: dict):
        s = ''
        for k, v in _dict.items():
            if v is not None:
                s += f'{k}:{json.dumps(v, ensure_ascii=False)},'
        return s.strip(',')

    ## % AREA
    def get_area_list(self, offset=0, limit=100) -> List[Dict]:
        q = f'match (n:Area) with n order by n.id return n SKIP {offset} LIMIT {limit}'
        res = self.exec(q)
        res = [dict(i[0]) for i in res]
        return res

    def get_area_count(self) -> int:
        q = f'match (n:Area) return COUNT(n)'
        res = self.exec(q)
        return res[0][0]

    def create_area(self, name: str):
        new_id = max(self.get_max_area(), 10000) + 1

        q = "CREATE (a:Area) " \
            f"SET a.id = {new_id} " \
            f"SET a.name = '{name}' " \
            "RETURN a"

        res = self.exec(q)
        return dict(res)

    def get_area(self, id: int):
        q = f'match (n:Area{{id:{id}}}) return n'
        res = self.exec(q)
        return [dict(i[0]) for i in res]

    def get_max_area(self):
        q = 'match (n:Area) return max(n.id)'
        res = self.exec(q)
        return res[0][0]

    def get_currencies(self):
        q = 'match (n:Currency) return n'
        res = self.exec(q)
        return [dict(i[0]) for i in res]

    ## % Currency

    def create_currency(self, name: str):
        if name:
            q = f"merge (n:Currency{{name:'{name}'}}) return n"
            res = self.exec(q)
            return [dict(i[0]) for i in res]
        return None

    def get_max_employer(self):
        q = 'match (n:Employer) return max(n.id)'
        res = self.exec(q)
        return res[0][0]

    ## % Employer

    def get_employer(self, id):
        q = f'match (n:Employer{{id:{id}}}) return n'
        res = self.exec(q)
        return [dict(i[0]) for i in res]

    def get_employer_list(self, offset=0, limit=100):
        q = f'match (n:Employer) return n SKIP {offset} LIMIT {limit}'
        res = self.exec(q)
        return [dict(i[0]) for i in res]

    def get_employer_count(self) -> int:
        q = f'match (n:Employer) return COUNT(n)'
        res = self.exec(q)
        return res[0][0]

    def create_employer(self, name: str):
        new_id = self.get_max_employer() + 1

        q = "CREATE (a:Employer) " \
            f"SET a.id = '{new_id}' " \
            f"SET a.name = '{name}' " \
            "RETURN a"

        res = self.exec(q)
        return res

    def get_schedule(self):
        q = 'match (n:Schedule) return n'
        res = self.exec(q)
        return [dict(i[0]) for i in res]

    ## % Schedule
    def get_vacancy_type(self):
        q = 'match (n:Vacancy_type) return n'
        res = self.exec(q)
        return [dict(i[0]) for i in res]

    def create_vacancy(self, name: str, area_id: int, schedule: str = "fullDay",
                       requirement: str = "", responsibility: str = "", salary_from: int = 0,
                       salary_to: int = 500000, currency: str = 'RUR', employer: str = "None"):

        vid = random.randint(10, 100000)
        while (self.get_vacancy_by_ids([vid])):
            vid = random.randint(10, 100000)

        vacancy = {"created_at": str(datetime.datetime.now().isoformat()),
                   "published_at": str(datetime.datetime.now().isoformat()),
                   "name": name,
                   "requirement": requirement,
                   "responsibility": responsibility,
                   "salary_from": salary_from,
                   "salary_to": salary_to,
                   "id": vid
                   }
        area = self.get_area(area_id)
        if area:
            area = area[0]
        else:
            area = {"id": 0, "name": "None"}
        area = self.get_area(area_id)[0]
        currency = {"name": currency}
        schedule = {"id": schedule}
        type = {"id": "open"}
        employer = {"id": self.get_max_employer() + 1, "name": employer}
        self.create_vacancy_all({"vacancy": vacancy, "area": area, "currency": currency, "employer": employer,
                                 "schedule": schedule, "type": type})
        return vid

    def create_vacancy_all(self, vacancy_all: Dict):
        vac_all = vacancy_all
        key_skills: List[str] = vac_all.get("key_skills") or []
        q = f'MERGE (v:Vacancy{{{self.dict_to_neo(vac_all["vacancy"])}}}) ' \
            f'MERGE (a:Area{{{self.dict_to_neo(vac_all["area"])}}}) ' \
            f'MERGE (c:Currency{{{self.dict_to_neo(vac_all["currency"])}}}) ' \
            f'MERGE (e:Employer{{{self.dict_to_neo(vac_all["employer"])}}}) ' \
            f'MERGE (s:Schedule{{{self.dict_to_neo(vac_all["schedule"])}}}) ' \
            f'MERGE (t:Vacancy_type{{{self.dict_to_neo(vac_all["type"])}}}) ' \
            f'MERGE (v)-[:LOCATED_IN]->(a) ' \
            f'MERGE (v)-[:SALARY_IN]->(c) ' \
            f'MERGE (v)-[:HAS_EMPLOYER]->(e) ' \
            f'MERGE (v)-[:HAS_SCHEDULE]->(s) ' \
            f'MERGE (v)-[:HAS_TYPE]->(t) '  # \
        # f'RETURN v,a,c,e,s,t '
        # res = self.exec(query=q)

        # q1=f'MERGE (v:Vacancy{{{self.dict_to_neo(vac_all["vacancy"])}}})
        for i, ks in enumerate(key_skills):
            q += f'MERGE (k{i}:Key_skill{{name:"{ks.get("name")}"}}) '
            q += f'MERGE (v)-[:HAS_KS]->(k{i}) '

        q += 'RETURN v,a,c,e,s,t '
        try:
            res = self.exec(query=q)
        except:
            res = None
        return res

    def filter(self, search_arg: str, areas: List[int] = None, currency: str = None, employer: int = None,
               sf: int = 0, st: int = 500000,
               schedule: str = None, offset: int = 0, limit: int = 100):
        q = f'CALL db.index.fulltext.queryNodes("descriptions", "{search_arg}~") YIELD node as v, score as s '
        v = 'v'  # v,s,c,a,k,sh,e,t
        vv = 'v.id'
        if areas:
            q += f'match (v)--(a:Area) ' \
                 f'where a.id in {json.dumps(areas)} '
            v += ',a'
        if currency:
            q += f'match (v)--(c:Currency{{name:"{currency}"}}) '
            v += ',c'
        if schedule:
            q += f'MATCH (sh:Schedule{{id: "{schedule}"}})'
            v += ',sh'
        q += f'return {vv} ' \
             f'SKIP {offset} ' \
             f'LIMIT {limit} '
        res = self.exec(q)
        ids = [i[0] for i in res]
        vacs = self.get_vacancy_by_ids(ids)
        return vacs

        # return [dict(i[0]) for i in res]

        # TODO

    def populate(self, qu: str = "????????????????", page: int = 0, per_page: int = 100):
        # hh = hh_api.Hh_api()
        from app import hh_api as hh
        vacs = hh.get_vacancy_by_name(name="????????????????", num_of_pages=1)

        for vac in vacs:
            vac_all = hh_prep.preproc_vacancy(vac)
            try:
                self.create_vacancy_all(vac_all)
            except:
                pass

    def get_vacancy_list(self, offset=0, limit=100) -> List[Dict]:
        q_id = f"MATCH (n:Vacancy) return n.id SKIP {offset} LIMIT {limit}"
        res: List = self.exec(q_id)
        ids = [i[0] for i in res]

        q_vacs = f"MATCH (n:Vacancy) -[l]->(d) WHERE (n.id in {json.dumps(ids)}) return n,l,d"
        res = self.exec(q_vacs)
        vacs = {res[i][0] for i in range(len(res))}
        vacs = {i.get("id"): dict(i) for i in vacs}  # {id:Vac}
        for triplet in res:
            vac = triplet[0]
            rel = triplet[1]
            opt = triplet[2]
            vacs[triplet[0].get("id")][list(opt.labels)[0]] = dict(opt)  # [{id:Vac{...,label:Obj}}]

        return list(vacs.values())

    def get_vacancy_ids_list(self, offset=0, limit=100) -> List[int]:
        q_id = f"MATCH (n:Vacancy) return n.id SKIP {offset} LIMIT {limit}"
        res: List = self.exec(q_id)
        ids = [i[0] for i in res]
        return ids

    def get_vacancy_by_ids(self, ids: List[int]) -> List[Dict]:
        q_vacs = f"MATCH (n:Vacancy) -[l]->(d) WHERE (n.id in {json.dumps(ids)}) return n,l,d"
        res = self.exec(q_vacs)
        vacs = {res[i][0] for i in range(len(res))}
        vacs = {i.get("id"): dict(i) for i in vacs}
        for triplet in res:
            vac = triplet[0]
            rel = triplet[1]
            opt = triplet[2]
            vacs[triplet[0].get("id")][list(opt.labels)[0]] = dict(opt)
        for k, v in vacs.items():
            k: int
            v: Dict
            v["key_skills"] = self.get_kss_for_vac(k)
            try:
                v.pop("Key_skill")
            except:
                pass
        return list(vacs.values())

    def get_kss_for_vac(self, id: int) -> List[str]:
        q = f'match (v:Vacancy{{id:{id}}})--(k:Key_skill) return k.name'
        res = self.exec(q)
        names = [i[0] for i in res]
        return names

    def get_vacancy_pure(self, offset=0, limit=100):
        # q = f'MATCH (n:Vacancy{{id:"{id}"}}) RETURN n SKIP 0 LIMIT 10'
        q = f'MATCH (n:Vacancy) RETURN n SKIP {offset} LIMIT {limit}'
        res = self.exec(q)
        return [dict(i[0]) for i in res]

    def count_ks_weight(self):  # TODO ???????? ?????????????? ?? ???????? ???????????? ?????????? ???????????????
        q = 'match (n:Key_skill) return n.name'
        res = self.exec(q)
        names = [i[0] for i in res]
        ret = []
        for name in names:
            q = f'''
                call{{
                match (n:Key_skill)
                where n.name="{name}"
                match (n)--(v:Vacancy)
                return count(v) as cnt
                }}
                match (m:Key_skill)
                where m.name="{name}"
                set m.w=cnt
                return m
            '''
            res = self.exec(q)
            ret.append(res[0][0])
        return ret

    def count_vac_weight(self):
        q = 'match (n:Vacancy) return n.id'
        res = self.exec(q)
        ids = [i[0] for i in res]
        ret = []
        for id in ids:
            q1 = f'''
                call{{
                match (n:Vacancy)
                where n.id={id}
                match (n)--(v:Key_skill)
                return sum(v.w) as cnt
                }}
                match (m:Vacancy)
                where m.id={id}
                set m.w=cnt
                return m
            '''
            q2 = f'''
                call{{
                match (n:Vacancy)
                where n.id={id}
                match (n)--(v:Key_skill)
                return avg(v.w) as mn
                }}
                match (m:Vacancy)
                where m.id={id}
                set m.m=mn
                return m
            '''
            res = self.exec(q1)
            ret.append(res[0][0])
            res = self.exec(q2)
            ret.append(res[0][0])
        return ret

    def get_vacs_common_ks(self, id1: int, id2: int) -> List[Dict]:
        q = f'match (a:Vacancy)--(k:Key_skill)--(b:Vacancy) where a.id = {id1} and b.id={id2} return k'
        res = self.exec(q)
        kss = [dict(i[0]) for i in res]
        return kss

    def get_area_name(self, id):
        vacs = self.get_area(id)
        if vacs:
            vac = vacs[0]
        else:
            return "None"
        return vac["name"]

    def get_vac_name(self, id):
        vacs = self.get_vacancy_by_ids([id])
        if vacs:
            vac = vacs[0]
        else:
            return "None"
        return vac["name"]

    def get_similar_vacs_by_ks_all(self, id: int, limit: int = 10):
        q = f'match (a:Vacancy)--(k:Key_skill)--(b:Vacancy) where a.id = {id} and b.id<>a.id return b.id'
        res = self.exec(q)
        ids = [i[0] for i in res]
        vacs = []
        ret = {}
        x0 = 100
        x1 = 700
        w = x1 - x0
        y0 = 150
        y1 = 200
        h = y1 - y0
        # a0=.1
        # a1=.9
        b1 = .3
        b2 = .7
        l = len(ids)
        for i, id1 in enumerate(ids):
            # x = x0+ w/l*i
            # y = y1
            ks = self.get_vacs_common_ks(id, id1)
            vacs.append({"vacancy_id": id1, "common_key_skills": ks, "cnt": len(ks),
                         "name": self.get_vac_name(id1)})

        vacs.sort(key=lambda v: v["cnt"])
        vacs = vacs[:min(limit, len(vacs))]
        l = len(vacs)

        for i, vac in enumerate(vacs):
            x = x0 + w / l * i
            y = y1
            vac["cx"] = x
            vac["cy"] = y

        ret["items"] = vacs
        ret["cx"] = x0 + w / 2
        ret["cy"] = y0
        ret["len"] = len(vacs)
        ret["name"] = self.get_vac_name(id)
        # ret["vacancy_id"] = id

        return ret

    def del_vac(self, id):
        q = f'match (v:Vacancy{{id:{id}}}) optional match (v)-[l]-() delete v,l'
        res = self.exec(q)
        print(res)
        return True

    def get_top_need(self, offset: int = 0, limit: int = 10):
        q = f'MATCH (n:Vacancy) ' \
            f'WITH n order by n.m desc ' \
            f'return n.id ' \
            f'SKIP {offset} ' \
            f'LIMIT {limit} '
        res = self.exec(q)
        ids = [i[0] for i in res]
        vacs = self.get_vacancy_by_ids(ids)
        # vacs = [dict(i[0]) for i in res]
        fro = random.randint(5, 10) * 10000
        fto = random.randint(11, 20) * 10000
        ret = {"items": vacs, "from": fro, "to": fto}
        return ret

    def get_top_paid(self, offset: int = 0, limit: int = 10):
        q = f'MATCH (n:Vacancy) ' \
            f'WITH n order by n.m desc ' \
            f'return n.id ' \
            f'SKIP {offset} ' \
            f'LIMIT {limit} '
        res = self.exec(q)
        ids = [i[0] for i in res]
        vacs = self.get_vacancy_by_ids(ids)
        # vacs = [dict(i[0]) for i in res]
        fro = random.randint(5, 10) * 10000
        fto = random.randint(11, 20) * 10000
        ret = {"items": vacs, "from": fro, "to": fto}
        return ret

    def get_top_new(self, offset: int = 0, limit: int = 10):
        q = f'MATCH (n:Vacancy) ' \
            f'WITH n order by n.published_at desc ' \
            f'return n.id ' \
            f'SKIP {offset} ' \
            f'LIMIT {limit} '
        res = self.exec(q)
        ids = [i[0] for i in res]
        vacs = self.get_vacancy_by_ids(ids)
        # vacs = [dict(i[0]) for i in res]
        fro = random.randint(5, 10) * 10000
        fto = random.randint(11, 20) * 10000
        ret = {"items": vacs, "from": fro, "to": fto}
        return ret

    def get_in_area_cnt(self, id: int):
        q = f'MATCH (n:Area{{id:{id}}})-[l]-(a:Vacancy) RETURN count(n)'
        res = self.exec(q)
        return res[0][0]

    def get_cnt_by_area(self, limit: int = 10):
        areas = self.get_area_list(0, limit)
        ids = [area.get("id") or 0 for area in areas]
        data = {self.get_area_name(id): self.get_in_area_cnt(id) for id in ids}
        return data

    def export(self) -> str:
        q = 'MATCH (n:Vacancy) RETURN n.id'
        res = self.exec(q)
        ids = [i[0] for i in res]
        dd = json.dumps(ids)
        b = base64.b64encode(dd.encode()).decode()

        return b

    def iimport(self, bdata: str = ""):
        print(request.data)
        try:
            data = json.loads(base64.b64decode(bdata).decode())
            q = f'MATCH (n:Vacancy) where n in {json.dumps(data)} RETURN n.id'
            res = self.exec(q)
        except:
            res = False
        return res

    def get_total_count(self):
        q = 'match(n) return count(n)'
        res = self.exec(q)
        return res[0][0]

    def create_search_index_if_not_exest(self):
        exists = str(self.exec("CALL db.indexes")).find("FULLTEXT") != -1
        res = None
        if not exists:
            q = "CALL db.index.fulltext.createNodeIndex('descriptions', ['Vacancy'], ['name','responsibility', 'requirement'], {analyzer: 'russian'})"
            q1 = 'CREATE CONSTRAINT ON (n:Vacancy) ASSERT n.id IS UNIQUE'
            try:
                res = self.exec(q)
            except:
                pass
            try:
                res = self.exec(q1)
            except:
                pass

        return exists

    def exec(self, query: str):
        transaction = lambda tx: tx.run(query).values()

        with self.driver.session() as session:
            return session.write_transaction(transaction)

    def __del__(self):
        self.driver.close()

    def autopopulate(self):
        self.populate("????????????????")
        self.populate("??????????????????????")
        self.populate("??????????????????")
