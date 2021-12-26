import contextlib
import io
import json
import random
import sys
import time
from time import sleep
from typing import List, Dict

from neo4j import GraphDatabase


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

    @staticmethod
    def dict_to_neo(_dict: dict):
        s = ''
        for k, v in _dict.items():
            if v is not None:
                s += f'{k}:{json.dumps(v, ensure_ascii=False)},'
        return s.strip(',')

    ## % AREA
    def get_area_list(self, offset=0, limit=100) -> List[Dict]:
        q = f'match (n:Area) return n SKIP {offset} LIMIT {limit}'
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

    def create_vacancy_all(self, vacancy_all: Dict):
        vac_all = vacancy_all
        key_skills: List[str] = vac_all["key_skills"]
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

        res = self.exec(query=q)
        return res

    def filter(self, search_arg: str, areas: List[int] = None, currency: str = None, employer=None,
               schedule=None):
        q = f'CALL db.index.fulltext.queryNodes("descriptions", "{search_arg}~") YIELD node as v, score as s'
        if areas:
            q += f'match (v)--(a:Area) ' \
                 f'where a.id in {json.dump(areas)} '
        # TODO

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
            v.pop("Key_skill")
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

    def count_ks_weight(self):  # TODO если склеить в один запрос будет быстрее?
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

    def get_similar_vacs_by_ks_all(self, id: int):
        q = f'match (a:Vacancy)--(k:Key_skill)--(b:Vacancy) where a.id = {id} and b.id<>a.id return b.id'
        res = self.exec(q)
        ids = [i[0] for i in res]
        ret = []
        for id1 in ids:
            ks = self.get_vacs_common_ks(id, id1)
            ret.append({"vacancy_id": id1, "common_key_skills": ks, "cnt": len(ks)})
        return ret

    def get_most_req_ks(self):  # TODO
        pass

    def get_top_need(self, offset: int = 0, limit: int = 10):
        q = f'MATCH (n:Vacancy) ' \
            f'WITH n order by n.m desc ' \
            f'return n ' \
            f'SKIP {offset} ' \
            f'LIMIT {limit} '
        res = self.exec(q)
        vacs = [dict(i[0]) for i in res]
        fro = random.randint(5, 10) * 10000
        fto = random.randint(11, 20) * 10000
        ret = {"items": vacs, "from": fro, "to": fto}
        return ret

    def exec(self, query: str):
        transaction = lambda tx: tx.run(query).values()

        with self.driver.session() as session:
            return session.write_transaction(transaction)

    def __del__(self):
        self.driver.close()
