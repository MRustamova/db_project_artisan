"""Redis connection and utilities."""

import redis
import json
from typing import Optional, Any
from src.config import REDIS_CONFIG, CACHE_TTL


class RedisClient:
    def __init__(self):
        self.client = redis.Redis(**REDIS_CONFIG)

    def get_json(self, key: str) -> Optional[Any]:
        """Get JSON data from Redis."""
        data = self.client.get(key)
        return json.loads(data) if data else None

    def set_json(self, key: str, value: Any, ttl: int = CACHE_TTL) -> bool:
        """Set JSON data in Redis with TTL."""
        return self.client.setex(key, ttl, json.dumps(value))

    def add_to_cart(self, user_id: str, product_id: str, quantity: int):
        """Add item to user's cart."""
        cart_key = f"cart:{user_id}"
        self.client.hincrby(cart_key, product_id, quantity)
        self.client.expire(cart_key, CACHE_TTL)
        # TODO: Implement cart logic
    def get_cart(self, user_id: str) -> dict:
        cart_key = f"cart:{user_id}"
        return {k: int(v) for k, v in self.client.hgetall(cart_key).items()}

    def remove_from_cart(self, user_id: str, product_id: str):
        cart_key = f"cart:{user_id}"
        self.client.hdel(cart_key, product_id)

    def clear_cart(self, user_id: str):
        cart_key = f"cart:{user_id}"
        self.client.delete(cart_key)

    def rate_limit_check(self, user_id: str, endpoint: str) -> bool:
        """Check if user has exceeded rate limit."""
        # TODO: Implement rate limiting logic
        pass
    def add_hot_product(self, product_id: str, score: float):
        print(f"Adding {product_id} with score {score}")
        self.client.zincrby("hot_products", score, product_id)

    def get_hot_products(self, top_n: int = 10) -> list:
        print("Fetching hot products...")
        return self.client.zrevrange("hot_products", 0, top_n - 1, withscores=True)

    def ping(self):
        return self.client.ping()

    def keys(self, pattern="*"):
        return self.client.keys(pattern)
# Singleton instance
redis_client = RedisClient()

