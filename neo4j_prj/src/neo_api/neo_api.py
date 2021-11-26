import contextlib
import io
import sys
import time
from time import sleep
import dataclasses
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

    def create_area(self, area:Area):
        transaction = lambda tx: tx.run("CREATE (a:Area) "
                                        f"SET a.id = '{area.id}' "
                                        f"SET a.name = '{area.name}' "
                                        "RETURN a.message + ', from node ' + id(a)").values()
        # area.
        with self.driver.session() as session:
            print(session.write_transaction(transaction)[0])

    def get_vacancy(self,offset = 0, limit = 100):
        # q = f'MATCH (n:Vacancy{{id:"{id}"}}) RETURN n SKIP 0 LIMIT 10'
        q = f'MATCH (n:Vacancy) RETURN n SKIP {offset} LIMIT {limit}'
        transaction = lambda tx: tx.run(q).values()
        with self.driver.session() as session:
            return(session.write_transaction(transaction))

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
    def exec(self,query:str):
        transaction = lambda tx: tx.run(query).values()

        with self.driver.session() as session:
            return session.write_transaction(transaction)


    def __del__(self):
        self.driver.close()
