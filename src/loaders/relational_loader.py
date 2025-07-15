"""Load data into PostgreSQL database."""

from src.db.postgres_client import db
from src.utils.data_parser import DataParser


class RelationalLoader:
    def __init__(self):
        self.db = db
        self.parser = DataParser()

    def load_categories(self):
        """Load categories into PostgreSQL."""
        categories = self.parser.parse_categories()

        with self.db.get_cursor() as cursor:
            for _, row in categories.iterrows():
                # TODO: Implement INSERT query
                query = """
                        INSERT INTO categories (id, name, description)
                        VALUES (%(id)s, %(name)s, %(description)s) ON CONFLICT (id) DO NOTHING; \
                        """
                cursor.execute(query, row.to_dict())

        print(f"Loaded {len(categories)} categories")

    def load_sellers(self):
        """Load sellers into PostgreSQL."""
        # TODO: Implement seller loading
        sellers = self.parser.parse_sellers()
        with self.db.get_cursor() as cursor:
            for _, row in sellers.iterrows():
                cursor.execute(
                    """
                    INSERT INTO sellers (id, name, specialty, rating, joined)
                    VALUES (%(id)s, %(name)s, %(specialty)s, %(rating)s, %(joined)s)
                    ON CONFLICT (id) DO NOTHING;
                    """,
                    row.to_dict()
                )
        

    def load_users(self):
        users = self.parser.parse_users()
        with self.db.get_cursor() as cursor:
            for _, row in users.iterrows():
                cursor.execute(
                    """
                    INSERT INTO users (id, name, email, join_date, location, interests)
                    VALUES (%(id)s, %(name)s, %(email)s, %(join_date)s, %(location)s, %(interests)s)
                    ON CONFLICT (id) DO NOTHING;
                    """,
                    row.to_dict()
                )

    def load_products(self):
        products = self.parser.parse_products()
        with self.db.get_cursor() as cursor:
            for _, row in products.iterrows():
                cursor.execute(
                    """
                    INSERT INTO products (id, name, category, price, seller_id, description, tags, stock)
                    VALUES (%(id)s, %(name)s, %(category)s, %(price)s, %(seller_id)s, %(description)s, %(tags)s, %(stock)s)
                    ON CONFLICT (id) DO NOTHING;
                    """,
                    row.to_dict()
                )

    def load_all(self):
        print("Creating tables...")
        self.db.create_tables()

        print("Loading categories...")
        self.load_categories()

        print("Loading sellers...")
        self.load_sellers()

        print("Loading users...")
        self.load_users()

        print("Loading products...")
        self.load_products()

        # TODO: Load remaining data
        print("Relational data loading complete!")


if __name__ == "__main__":
    loader = RelationalLoader()
    loader.load_all()
