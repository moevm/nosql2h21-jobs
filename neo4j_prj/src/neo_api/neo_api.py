import contextlib
import io
import json
import sys
import time
from time import sleep
from typing import List, Dict

from neo4j import GraphDatabase

from hh_api.hh_api import Area


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
            e = Exception
            raise Exception(f"Neo4j connection timed out after {timeout_sec} sec")

    @staticmethod
    def dict_to_neo(_dict: dict):
        s = ''
        for k, v in _dict.items():
            if v is not None:
                s += f'{k}:{json.dumps(v, ensure_ascii=False)},'
        return s.strip(',')

    def get_area_list(self, offset = 0, limit = 100):
        pass

    def create_area(self, area: Area):
        transaction = lambda tx: tx.run("CREATE (a:Area) "
                                        f"SET a.id = '{area.id}' "
                                        f"SET a.name = '{area.name}' "
                                        "RETURN a.message + ', from node ' + id(a)").values()
        # area.
        with self.driver.session() as session:
            print(session.write_transaction(transaction)[0])

    def get_vacancy(self, offset=0, limit=100) -> List[Dict]:
        q_id = f"MATCH (n:Vacancy) return n.id SKIP {offset} LIMIT {limit}"
        res: List = self.exec(q_id)
        ids = [i[0] for i in res]

        q_vacs = f"MATCH (n:Vacancy) -[l]->(d) WHERE (n.id in {json.dumps(ids)}) return n,l,d"
        res = self.exec(q_vacs)
        vacs = {res[i][0] for i in range(len(res))}
        vacs = {i.get("id"): dict(i) for i in vacs}
        for triplet in res:
            vac = triplet[0]
            rel = triplet[1]
            opt = triplet[2]
            vacs[triplet[0].get("id")][list(opt.labels)[0]] = dict(opt)

        return list(vacs.values())

    def create_vacancy_all(self, vacancy_all: Dict):
        vac_all = vacancy_all
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
            f'MERGE (v)-[:HAS_TYPE]->(t) ' \
            f'RETURN v,a,c,e,s,t'
        res = self.exec(query=q)
        return res

    def get_vacancy_pure(self, offset=0, limit=100):
        # q = f'MATCH (n:Vacancy{{id:"{id}"}}) RETURN n SKIP 0 LIMIT 10'
        q = f'MATCH (n:Vacancy) RETURN n SKIP {offset} LIMIT {limit}'
        transaction = lambda tx: tx.run(q).values()
        with self.driver.session() as session:
            return (session.write_transaction(transaction))

    def hello_world(self):
        message = "Hello, World!"

        transaction = lambda tx: tx.run("CREATE (a:Greeting) "
                                        f"SET a.message = '{message}' "
                                        "RETURN a.message + ', from node ' + id(a)").values()

        with self.driver.session() as session:
            print(session.write_transaction(transaction)[0])
            # result = session.run("CREATE (a:Greeting) "
            #                      f"SET a.message = '{message}' "
            #                      "RETURN a.message + ', from node ' + id(a)")
            # print(result.single()[0])

    def exec(self, query: str):
        transaction = lambda tx: tx.run(query).values()

        with self.driver.session() as session:
            return session.write_transaction(transaction)

    def __del__(self):
        self.driver.close()
