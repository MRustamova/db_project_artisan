"""Neo4j connection and utilities."""

from neo4j import GraphDatabase
from src.config import NEO4J_CONFIG

class GraphClient:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            NEO4J_CONFIG["uri"],
            auth=(NEO4J_CONFIG["user"], NEO4J_CONFIG["password"])
        )

    def session(self):
        return self.driver.session()

# Singleton instance
graph = GraphClient()
