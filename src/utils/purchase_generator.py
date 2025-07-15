"""Generate random purchase history."""

import random
from datetime import timedelta
import pandas as pd

from src.utils.data_parser import DataParser


class PurchaseGenerator:
    def __init__(self):
        self.parser = DataParser()
        self.users = self.parser.parse_users()
        self.products = self.parser.parse_products()

    def generate_purchases(self, num_purchases: int = 100) -> pd.DataFrame:
        """Generate random purchases based on user interests."""
        purchases = []
        users = self.users.to_dict(orient="records")
        products = self.products.to_dict(orient="records")

        max_attempts = num_purchases * 5
        attempts = 0

        while len(purchases) < num_purchases and attempts < max_attempts:
            attempts += 1
            user = random.choice(users)
            join_date = pd.to_datetime(user["join_date"])

            # Match products by user interests
            matching_products = [
                p for p in products
                if any(tag in user["interests"] for tag in p["tags"])
            ]
            if not matching_products:
                continue

            product = random.choice(matching_products)

            days_since_join = (pd.Timestamp.now() - join_date).days
            if days_since_join <= 0:
                continue

            purchase_date = join_date + timedelta(days=random.randint(0, days_since_join))
            quantity = random.randint(1, 3)

            purchases.append({
                "user_id": user["id"],
                "product_id": product["id"],
                "quantity": quantity,
                "purchase_date": purchase_date.isoformat()
            })

        return pd.DataFrame(purchases)

    def save_purchases(self, purchases: pd.DataFrame, filename: str = "purchases.csv"):
        """Save generated purchases to CSV."""
        purchases.to_csv(filename, index=False)


if __name__ == "__main__":
    generator = PurchaseGenerator()
    purchases = generator.generate_purchases()
    generator.save_purchases(purchases)
    print(f"Generated {len(purchases)} purchases")
