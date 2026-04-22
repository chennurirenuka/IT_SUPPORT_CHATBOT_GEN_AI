from sentence_transformers import SentenceTransformer
from config.settings import settings

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)

    def encode(self, texts):
        return self.model.encode(texts, convert_to_numpy=True)
