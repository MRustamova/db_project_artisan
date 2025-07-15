"""Load purchases into PostgreSQL and Neo4j."""

import pandas as pd
from datetime import datetime

from src.db.postgres_client import db
from src.db.graph_client import graph


class PurchaseLoader:
    def __init__(self, purchase_csv: str = "purchases.csv"):
        self.purchases = pd.read_csv(purchase_csv)
        self.purchases["purchase_date"] = pd.to_datetime(self.purchases["purchase_date"])

    def load_postgres(self):
        """Load purchases into PostgreSQL (orders + order_items)."""
        with db.get_cursor() as cursor:
            for i, row in self.purchases.iterrows():
                order_id = f"ORD{i+1:03d}"
                cursor.execute("""
                    INSERT INTO orders (id, user_id, order_date)
                    VALUES (%s, %s, %s) ON CONFLICT (id) DO NOTHING;
                """, (order_id, row["user_id"], row["purchase_date"]))

                cursor.execute("""
                    INSERT INTO order_items (order_id, product_id, quantity)
                    VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;
                """, (order_id, row["product_id"], row["quantity"]))

        print(f"Loaded {len(self.purchases)} purchases into PostgreSQL")

    def load_neo4j(self):
        """Load purchases into Neo4j."""
        session = graph.session()
        for _, row in self.purchases.iterrows():
            session.run("""
                MERGE (u:User {id: $user_id})
                MERGE (p:Product {id: $product_id})
                MERGE (u)-[r:PURCHASED {date: $date, quantity: $quantity}]->(p)
            """, {
                "user_id": row["user_id"],
                "product_id": row["product_id"],
                "quantity": int(row["quantity"]),
                "date": row["purchase_date"].isoformat()
            })
        print(f"Loaded {len(self.purchases)} purchases into Neo4j")


if __name__ == "__main__":
    loader = PurchaseLoader()
    print("Loading purchases into PostgreSQL...")
    loader.load_postgres()
    print("Loading purchases into Neo4j...")
    loader.load_neo4j()
