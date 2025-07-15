from src.db.redis_client import redis_client
from datetime import datetime



class HotProductsService:
    def __init__(self):
        pass
    def add_hot_product(self, product_id: str, score: float):
        print(f" Adding {product_id} with score {score}")
        self.client.zincrby("hot_products", score, product_id)
    def _key(self, date: str = None) -> str:
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        return f"hot_products:{date}"

    def increment_view(self, product_id: str, score: int = 1):
        key = self._key()
        redis_client.zincrby(key, score, product_id)

    def get_top_products(self, date: str = None, top_n: int = 10):
        key = self._key(date)
        return redis_client.zrevrange(key, 0, top_n - 1, withscores=True)

    def reset_daily_hotlist(self, date: str = None):
        key = self._key(date)
        redis_client.delete(key)
