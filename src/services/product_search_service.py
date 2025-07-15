import hashlib
import psycopg2
from typing import List, Dict, Any, Optional

from src.db.postgres_client import db
from src.db.redis_client import redis_client


class ProductSearchService:
    def __init__(self):
        self.conn = psycopg2.connect(**db.config)

    def _make_cache_key(
        self, query: str, category: Optional[str], min_price: float, max_price: float, limit: int
    ) -> str:
        return f"search:{query}:{category or 'any'}:{min_price}:{max_price}:{limit}"

    def search_products(
        self,
        query: str,
        category: Optional[str] = None,
        min_price: float = 0.0,
        max_price: float = float("inf"),
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        cache_key = self._make_cache_key(query, category, min_price, max_price, limit)
        cached_result = redis_client.get_json(cache_key)

        if cached_result:
            print("Cache hit")
            return cached_result

        print("Cache miss")
        with self.conn.cursor() as cursor:
            sql = """
                SELECT id, name, description, price
                FROM products
                WHERE (name ILIKE %s OR description ILIKE %s OR tags ILIKE %s)
                AND price >= %s AND price <= %s
            """
            params = [f"%{query}%"] * 3 + [min_price, max_price]

            if category:
                sql += " AND category = %s"
                params.append(category)

            sql += " ORDER BY price ASC LIMIT %s"
            params.append(limit)

            cursor.execute(sql, params)
            rows = cursor.fetchall()

        result = [
            {"id": row[0], "name": row[1], "description": row[2], "price": float(row[3])}
            for row in rows
        ]
        redis_client.set_json(cache_key, result)
        return result


if __name__ == "__main__":
    service = ProductSearchService()
    results = service.search_products("bowl", category="Home & Kitchen", min_price=10, max_price=100, limit=5)
    for r in results:
        print(r)
