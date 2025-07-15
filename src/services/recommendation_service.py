from neo4j import GraphDatabase
from src.config import NEO4J_CONFIG

class RecommendationService:
    def __init__(self):
        self.driver = GraphDatabase.driver(
    NEO4J_CONFIG["uri"], 
    auth=(NEO4J_CONFIG["user"], NEO4J_CONFIG["password"]))


    def close(self):
        self.driver.close()

    def also_bought(self, product_id: str, limit: int = 5):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (p:Product {id: $product_id})<-[:PURCHASED]-(u:User)-[:PURCHASED]->(other:Product)
                WHERE other.id <> $product_id
                RETURN other.id AS id, COUNT(*) AS score
                ORDER BY score DESC
                LIMIT $limit;
            """, product_id=product_id, limit=limit)
            return [record["id"] for record in result]

    def personalized(self, user_id: str, limit: int = 5):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (u:User {id: $user_id})-[:PURCHASED]->(:Product)<-[:PURCHASED]-(other:User),
                      (other)-[:PURCHASED]->(rec:Product)
                WHERE NOT (u)-[:PURCHASED]->(rec)
                RETURN rec.id AS id, COUNT(*) AS score
                ORDER BY score DESC
                LIMIT $limit;
            """, user_id=user_id, limit=limit)
            return [record["id"] for record in result]

# Demo test
if __name__ == "__main__":
    rec = RecommendationService()
    print("Also bought:", rec.also_bought("P001"))
    print("Personalized:", rec.personalized("U001"))
    rec.close()
