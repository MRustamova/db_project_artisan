from src.db.redis_client import redis_client
import json
from datetime import timedelta


class CartService:
    def __init__(self, ttl_seconds: int = 3600):  # Default: 24 hours
        self.ttl = ttl_seconds

    def _key(self, user_id: str) -> str:
        return f"cart:{user_id}"

    def add_item(self, user_id: str, product_id: str, quantity: int):
        key = self._key(user_id)
        redis_client.hset(key, product_id, quantity)
        redis_client.expire(key, self.ttl)

    def remove_item(self, user_id: str, product_id: str):
        key = self._key(user_id)
        redis_client.hdel(key, product_id)

    def get_cart(self, user_id: str) -> dict:
        key = self._key(user_id)
        return {k.decode(): int(v) for k, v in redis_client.hgetall(key).items()}

    def update_item(self, user_id: str, product_id: str, quantity: int):
        self.add_item(user_id, product_id, quantity)

    def clear_cart(self, user_id: str):
        key = self._key(user_id)
        redis_client.delete(key)

    def cart_exists(self, user_id: str) -> bool:
        return redis_client.exists(self._key(user_id)) == 1
