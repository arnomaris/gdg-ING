import duckdb

data_path = "../10. Hackathon_Leuven_2025"
synthetic_data = data_path + "/Synthetic data"

# Create DB if it does not exist yet
conn = duckdb.connect("../banking_data.duckdb")

# Load CSV files
conn.execute(f"CREATE OR REPLACE TABLE customers AS SELECT * FROM read_csv('{synthetic_data}/customers.csv')")
conn.execute(f"CREATE OR REPLACE TABLE products AS SELECT * FROM read_csv('{synthetic_data}/products.csv')")
conn.execute(f"CREATE OR REPLACE TABLE transactions AS SELECT * FROM read_csv('{synthetic_data}/transactions.csv')")
# conn.execute(f"ALTER TABLE products ALTER COLUMN product_id SET DATA TYPE VARCHAR;")