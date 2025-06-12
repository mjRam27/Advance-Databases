# services/route_service.py
from utils.db_neo4j import get_neo4j_session

def find_shortest_route(start_station_name: str, end_station_name: str):
    """
    Finds the shortest path between two stations using Neo4j.
    """
    query = """
    MATCH path = shortestPath(
      (start:Station {name: $start_name})-[:CONNECTED*]->(end:Station {name: $end_name})
    )
    UNWIND nodes(path) AS station
    RETURN station.name AS station_name
    """
    
    session = get_neo4j_session()
    try:
        result = session.run(query, start_name=start_station_name, end_name=end_station_name)
        
        # Extract station names from the result records
        path_stations = [record["station_name"] for record in result]
        
        if not path_stations:
            return {"status": "error", "message": "No route found between the specified stations."}
            
        return {"status": "success", "route": path_stations}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}
    finally:
        session.close()
