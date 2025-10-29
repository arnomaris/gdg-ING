import duckdb
from sentence_transformers import SentenceTransformer

from chatbot.classes import Customer, Product, Transaction

db_path = "banking_data.duckdb"

model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')

conn = duckdb.connect(db_path)
conn.execute("LOAD vss;")
conn.execute("SET GLOBAL hnsw_enable_experimental_persistence = true;")

def get_customer(customer_id: str):
    sql = "SELECT * FROM customers WHERE customer_id = $customer_id"
    result = conn.execute(sql, {"customer_id": customer_id}).fetchall()

    if len(result) == 0:
        return None

    data = result[0]

    customer = Customer()
    customer.customer_id = data[0]
    customer.name = data[1]
    customer.birth_date = data[2]
    customer.email = data[3]
    customer.phone = data[4]
    customer.address = data[5]
    customer.segment_code = data[6]

    return customer

def get_customer_products(customer_id: str):
    sql = "SELECT * FROM products WHERE customer_id = $customer_id"
    result = conn.execute(sql, {"customer_id": customer_id}).fetchall()

    if len(result) == 0:
        return None

    products = []
    for row in result:
        product = Product()
        product.product_id = row[0]
        product.name = row[2]
        product.product_type = row[3]
        product.opened_date = row[4]
        product.status = row[5]
        products.append(product)

    return products

def get_customer_transactions(customer_id: str):
    sql = "SELECT transactions.transaction_id, transactions.product_id, date, amount, amount, currency, description, transaction_type FROM products JOIN transactions ON transactions.product_id = products.product_id WHERE customer_id = $customer_id"
    result = conn.execute(sql, {"customer_id": customer_id}).fetchall()

    transactions = []
    for row in result:
        transaction = Transaction()
        transaction.transaction_id = row[0]
        transaction.product_id = row[1]
        transaction.date = row[2]
        transaction.amount = row[3]
        transaction.currency = row[4]
        transaction.description = row[5]
        transaction.transaction_type = row[6]
        transactions.append(transaction)

    return transactions

def get_customer_data(customer_id: str):
    customer = get_customer(customer_id)
    if customer:
        products = get_customer_products(customer_id)
        transactions = get_customer_transactions(customer_id)

        return customer, products, transactions
    return None

def retrieve_relevant_info(query: str, language: str = 'nl', top_k: int = 1):
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
                           """, [query_embedding.tolist(), language, query_embedding.tolist(), top_k]).fetchall()

    return [r[1] for r in results]