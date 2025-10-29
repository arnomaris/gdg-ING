import duckdb

con = duckdb.connect("../banking_data.duckdb")

con.table("website_embeddings").show()