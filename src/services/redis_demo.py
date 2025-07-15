from src.db.redis_client import redis_client

def demo_cart():
    print("--- Cart Demo ---")
    redis_client.add_to_cart("U001", "P001", 2)
    redis_client.add_to_cart("U001", "P002", 1)
    cart = redis_client.get_cart("U001")
    print("Cart contents:", {k: int(v) for k, v in cart.items()})

def demo_hot_products():
    print("--- Hot Products Demo ---")
    redis_client.add_hot_product("P001", 1.0)
    redis_client.add_hot_product("P002", 2.0)
    redis_client.add_hot_product("P001", 1.0)
    hot = redis_client.get_hot_products()
    print("Hot products:", [(k, s) for k, s in hot])

if __name__ == "__main__":
    print("Redis connected:", redis_client.ping())
    print("Keys in Redis:", redis_client.client.keys("*"))

    demo_cart()
    demo_hot_products()
