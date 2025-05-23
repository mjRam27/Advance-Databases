# utils/db_neo4j.py
from neo4j import GraphDatabase
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Q@vrjud0327"))
def create_route(from_station, to_station, line, delay):
    with driver.session() as session:
        session.run(
            """
            MERGE (a:Station {name: $from})
            MERGE (b:Station {name: $to})
            MERGE (a)-[:ROUTE {line: $line, delay: $delay}]->(b)
            """,
            {
                "from": from_station,
                "to": to_station,
                "line": line,
                "delay": delay
            }
        )
