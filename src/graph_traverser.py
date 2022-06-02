
from typing import Dict

import requests
from collections import deque
from neo4j import GraphDatabase


class GraphTraverser:

    NEIGHBOR_QUERY = '''
    MATCH (source:Node{entity_id :{}})
    CALL gds.bfs.stream('myGraph', {
    sourceNode: source,
    maxDepth: 1
    })
    YIELD path
    RETURN path
    '''

    def __init__(self):
        self.connector = Neo4jConnection()

    def get_related_entities(self, entity_list, hops):
        results = []
        for entity in entity_list:
            entity_result = {entity: 0}
            k = 0
            queue = deque()
            queue.append(entity)
            while queue and k < hops:
                k += 1
                hop_length = len(queue)

                for _ in range(hop_length):
                    node = queue.popleft()
                    query = self.NEIGHBOR_QUERY.format(node)
                    neighbors = self._get_neighbor_list_from_path(
                        self.connector.query(query))
                    for neighbor in neighbors:
                        if neighbor not in entity:
                            entity_result[neighbor] = k
                            queue.append(neighbor)

            del entity_result[entity]
            results.append(entity_result)
        return results

    def _get_neighbor_list_from_path(self, path):
        return path


class Neo4jConnection:

    URI = 'bolt://localhost:7687'
    USER = ''
    PASS = ''

    def __init__(self,):

        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(
                self.URI, auth=(self.USER, self.PASS))
        except Exception as e:
            print("Failed to create the driver:", e)

    def close(self):
        if self.__driver is not None:
            self.__driver.close()

    def query(self, query, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.__driver.session(
                database=db) if db is not None else self.__driver.session()
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response
