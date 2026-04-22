import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = "IT Support Chatbot"
    APP_VERSION = "2.0.0"
    APP_ENV = os.getenv("APP_ENV", "development")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    TOP_K = int(os.getenv("TOP_K", 3))
    MEMORY_DB = os.getenv("MEMORY_DB", "memory_store.db")
    FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "models/knowledge.index")
    KNOWLEDGE_META_PATH = os.getenv("KNOWLEDGE_META_PATH", "models/knowledge_meta.pkl")
    CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", 0.45))
    USE_REDIS = os.getenv("USE_REDIS", "false").lower() == "true"
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    USE_PINECONE = os.getenv("USE_PINECONE", "false").lower() == "true"
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "it-support-kb")
    MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "mlruns")

settings = Settings()
