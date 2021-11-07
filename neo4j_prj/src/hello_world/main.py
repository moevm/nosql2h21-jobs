import contextlib
import io
import json
import sys

from neo4j import GraphDatabase


@contextlib.contextmanager
def nostdout():
    save_stdout = sys.stdout
    sys.stdout = io.BytesIO()
    yield
    sys.stdout = save_stdout


if __name__ == "__main__":
    with open("./settings.conf") as fs:
        cfg = json.load(fs)

    user, password = cfg["user"], cfg["pwd"]
    uri = f"bolt://{cfg['host']}:{cfg['port']}"
    message = cfg["hello_message"]
    driver = None
    print("waiting for neo4j connection...")
    while not driver:
        try:
            with nostdout():
                driver = GraphDatabase.driver(uri, auth=(user, password))
        except:
            pass

    transaction = lambda tx: tx.run("CREATE (a:Greeting) "
                                    f"SET a.message = '{message}' "
                                    "RETURN a.message + ', from node ' + id(a)").values()
    print("neo4j connection established")

    with driver.session() as session:
        print(session.write_transaction(transaction)[0])
        # result = session.run("CREATE (a:Greeting) "
        #                      f"SET a.message = '{message}' "
        #                      "RETURN a.message + ', from node ' + id(a)")
        # print(result.single()[0])
    driver.close()
