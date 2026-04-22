from config.settings import settings

class PineconeVectorStore:
    def __init__(self):
        self.api_key = settings.PINECONE_API_KEY
        self.index_name = settings.PINECONE_INDEX_NAME

    def search(self, query: str, top_k: int = 3):
        # Placeholder for Pinecone implementation
        # Add real Pinecone code when you connect production vector DB
        return []
