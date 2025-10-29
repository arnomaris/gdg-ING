import duckdb
import pandas as pd
from sentence_transformers import SentenceTransformer
import os

# Connect to DuckDB
conn = duckdb.connect("../banking_data.duckdb")

# Install and load VSS extension
conn.execute("INSTALL vss;")
conn.execute("LOAD vss;")
conn.execute("SET GLOBAL hnsw_enable_experimental_persistence = true;")

# Initialize
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')

def create_embeddings():
    # Collect all data first
    all_data = []
    chunk_id = 0

    for lang in ['nl', 'fr', 'en']:
        chunk_dir = f'{'../10. Hackathon_Leuven_2025'}/chunks/500_750_processed_be_{lang}_2025_09_23'

        if os.path.exists(chunk_dir):
            for filename in os.listdir(chunk_dir):
                if not filename.endswith('.txt'):
                    continue
                file_path = os.path.join(chunk_dir, filename)

                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read().strip()

                    if text:
                        embedding = model.encode(text)
                        all_data.append({
                            'id': chunk_id,
                            'language': lang,
                            'text': text,
                            'embedding': embedding.tolist()
                        })
                        chunk_id += 1
    df = pd.DataFrame(all_data)
    conn.execute("CREATE OR REPLACE TABLE website_embeddings AS SELECT * FROM df")

create_embeddings()