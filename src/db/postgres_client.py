"""PostgreSQL connection and utilities."""

from contextlib import contextmanager
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.config import POSTGRES_CONFIG

Base = declarative_base()


class PostgresConnection:
    def __init__(self):
        self.config = POSTGRES_CONFIG
        self._engine = None
        self._session_factory = None

    @property
    def engine(self):
        if not self._engine:
            db_url = (
                f"postgresql://{self.config['user']}:{self.config['password']}@"
                f"{self.config['host']}:{self.config['port']}/{self.config['database']}"
            )
            self._engine = create_engine(db_url)
        return self._engine

    @property
    def session_factory(self):
        if not self._session_factory:
            self._session_factory = sessionmaker(bind=self.engine)
        return self._session_factory

    @contextmanager
    def get_cursor(self):
        """Get a database cursor for raw SQL queries."""
        conn = psycopg2.connect(**self.config)
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                yield cursor
                conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def create_tables(self):
        with self.get_cursor() as cursor:
            cursor.execute("""
                CREATE EXTENSION IF NOT EXISTS vector;

                CREATE TABLE IF NOT EXISTS categories (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE,
                    description TEXT
                );

                CREATE TABLE IF NOT EXISTS sellers (
                    id VARCHAR PRIMARY KEY,
                    name TEXT NOT NULL,
                    specialty TEXT,
                    rating FLOAT,
                    joined DATE
                );

                CREATE TABLE IF NOT EXISTS users (
                    id VARCHAR PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE,
                    join_date DATE,
                    location TEXT,
                    interests TEXT
                );

                CREATE TABLE IF NOT EXISTS products (
                    id VARCHAR PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT REFERENCES categories(name),
                    price FLOAT,
                    seller_id VARCHAR REFERENCES sellers(id),
                    description TEXT,
                    tags TEXT,
                    stock INTEGER
                );

                CREATE TABLE IF NOT EXISTS product_embeddings (
                    product_id VARCHAR PRIMARY KEY REFERENCES products(id),
                    embedding vector(384)
                );

                -- UPDATED PART: orders.id is now TEXT
                CREATE TABLE IF NOT EXISTS orders (
                    id TEXT PRIMARY KEY,
                    user_id VARCHAR REFERENCES users(id),
                    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total_amount FLOAT
                );

                -- UPDATED PART: order_id is now TEXT to match orders.id
                CREATE TABLE IF NOT EXISTS order_items (
                    id SERIAL PRIMARY KEY,
                    order_id TEXT REFERENCES orders(id) ON DELETE CASCADE,
                    product_id VARCHAR REFERENCES products(id),
                    quantity INTEGER,
                    price FLOAT
                );

                CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
                CREATE INDEX IF NOT EXISTS idx_products_seller ON products(seller_id);
                CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);
            """)

# Singleton instance
db = PostgresConnection()
