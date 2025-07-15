

import json
from pathlib import Path
from src.db.mongodb_client import mongo_client


class DocumentLoader:
    def __init__(self):
        self.db = mongo_client

    def load_reviews(self):
        reviews_path = Path("raw_data/reviews.json")
        with open(reviews_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        collection = self.db.get_collection("reviews")
        collection.insert_many(data)
        print(f"Inserted {len(data)} reviews.")

    def load_product_specs(self):
        specs_path = Path("raw_data/product_specs.json")
        with open(specs_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        collection = self.db.get_collection("product_specs")
        collection.insert_many(data)
        print(f"Inserted {len(data)} product specs.")

    def load_seller_profiles(self):
        sellers_path = Path("raw_data/seller_profiles.json")
        with open(sellers_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        collection = self.db.get_collection("seller_profiles")
        collection.insert_many(data)
        print(f"Inserted {len(data)} seller profiles.")

    def load_user_preferences(self):
        prefs_path = Path("raw_data/user_preferences.json")
        with open(prefs_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        collection = self.db.get_collection("user_preferences")
        collection.insert_many(data)
        print(f"Inserted {len(data)} user preferences.")

    def load_all(self):
        print("Creating indexes...")
        self.db.create_indexes()
        print("Loading reviews...")
        self.load_reviews()
        print("Loading product specs...")
        self.load_product_specs()
        print("Loading seller profiles...")
        self.load_seller_profiles()
        print("Loading user preferences...")
        self.load_user_preferences()
        print("MongoDB data loading complete.")


if __name__ == "__main__":
    loader = DocumentLoader()
    loader.load_all()
