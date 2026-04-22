import json
import os
import joblib
import faiss
import numpy as np
from app.services.embeddings import EmbeddingService

def ingest_knowledge():
    with open("data/knowledge_base.json", "r", encoding="utf-8") as f:
        docs = json.load(f)

    texts = [doc["content"] for doc in docs]
    embedder = EmbeddingService()
    vectors = embedder.encode(texts)

    dimension = vectors.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(vectors, dtype="float32"))

    os.makedirs("models", exist_ok=True)
    faiss.write_index(index, "models/knowledge.index")
    joblib.dump(docs, "models/knowledge_meta.pkl")

    print("Knowledge ingestion completed successfully.")

if __name__ == "__main__":
    ingest_knowledge()
