from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from src.db.postgres_client import db  # your PostgresConnection singleton


class SearchService:
    def __init__(self):
        # Load the sentence transformer model once
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def semantic_search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search products using semantic similarity."""
        # Generate embedding for search query
        query_embedding = self.model.encode(query)

        with db.get_cursor() as cursor:
            cursor.execute(
                """
                SELECT p.id, p.name, p.description, p.price,
                       1 - (pe.embedding <=> %s::vector) AS similarity
                FROM products p
                JOIN product_embeddings pe ON p.id = pe.product_id
                ORDER BY pe.embedding <=> %s::vector
                LIMIT %s;
                """,
                (query_embedding.tolist(), query_embedding.tolist(), limit),
            )
            results = cursor.fetchall()

        return results


if __name__ == "__main__":
    service = SearchService()
    query_text = "handmade wooden bowl"
    results = service.semantic_search(query_text, limit=5)

    print(f"Semantic search results for: '{query_text}'\n")
    for row in results:
        print(f"ID: {row['id']}, Name: {row['name']}, Similarity: {row['similarity']:.4f}")
