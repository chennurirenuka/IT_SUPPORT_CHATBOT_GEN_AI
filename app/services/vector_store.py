import faiss
import joblib
from config.settings import settings
from app.services.embeddings import EmbeddingService

class VectorStore:
    def __init__(self):
        self.index = faiss.read_index(settings.FAISS_INDEX_PATH)
        self.metadata = joblib.load(settings.KNOWLEDGE_META_PATH)
        self.embedding_service = EmbeddingService()

    def search(self, query: str, top_k: int = None):
        if top_k is None:
            top_k = settings.TOP_K

        query_vector = self.embedding_service.encode([query])
        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for idx in indices[0]:
            if idx != -1:
                results.append(self.metadata[idx])
        return results
