import duckdb
from sentence_transformers import SentenceTransformer

db_path = "../banking_data.duckdb"

model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')

conn = duckdb.connect(db_path)
conn.execute("INSTALL vss;")
conn.execute("LOAD vss;")
conn.execute("SET GLOBAL hnsw_enable_experimental_persistence = true;")

def get_customer(customer_id: int):
    sql = "SELECT * FROM customers WHERE user_id =:user_id"
    result = conn.execute(sql, {"user_id": customer_id})

    for row in result.fetchall():
        return row

    return None

def get_customer_products(customer_id: int):
    sql = "SELECT * FROM products WHERE customer_id =:customer_id"
    result = conn.execute(sql, {"customer_id": customer_id})

    for row in result.fetchall():
        return row

def retrieve_relevant_info(query: str, language: str = 'nl', top_k: int = 3):
    """Retrieve relevant banking information using HNSW index"""

    # Generate query embedding
    query_embedding = model.encode(query)

    # This will automatically use the HNSW index if it exists
    results = conn.execute("""
                           SELECT id,
                                  text, language, array_cosine_distance(embedding::DOUBLE[768], ?::DOUBLE[768]) as distance
                           FROM website_embeddings
                           WHERE language = ?
                           ORDER BY array_cosine_distance(embedding::DOUBLE[768], ?::DOUBLE[768]) ASC
                               LIMIT ?
                           """, [query_embedding.tolist(), language, query_embedding.tolist(), top_k]).fetchdf()

    return results


print(retrieve_relevant_info("How do I setup faceid", language='en').)