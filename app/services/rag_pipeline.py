from config.settings import settings
from app.services.classifier import IntentClassifier
from app.services.vector_store import VectorStore
from app.services.pinecone_store import PineconeVectorStore
from app.services.memory import SessionMemory
from app.services.redis_memory import RedisSessionMemory
from app.services.prompt_builder import build_prompt
from app.services.llm_service import LLMService
from app.core.logger import get_logger

logger = get_logger(__name__)


class RAGPipeline:
    def __init__(self):
        self.classifier = IntentClassifier(
            model_path="models/intent_model.pkl",
            vectorizer_path="models/tfidf_vectorizer.pkl"
        )
        self.vector_store = PineconeVectorStore() if settings.USE_PINECONE else VectorStore()
        self.memory = RedisSessionMemory() if settings.USE_REDIS else SessionMemory()
        self.llm = LLMService()

    def run(self, session_id: str, user_query: str):
        predicted_intent, confidence = self.classifier.predict_intent(user_query)
        logger.info(f"Predicted intent={predicted_intent}, confidence={confidence:.4f}")

        retrieved_docs = self.vector_store.search(user_query, top_k=settings.TOP_K)
        history = self.memory.get_history(session_id)

        prompt = build_prompt(
            user_query=user_query,
            predicted_intent=predicted_intent,
            confidence=confidence,
            retrieved_docs=retrieved_docs,
            history=history
        )

        if confidence < settings.CONFIDENCE_THRESHOLD:
            answer = (
                f"It looks like a possible '{predicted_intent}' issue, but confidence is low. "
                f"Based on the retrieved knowledge, please try these steps:\n\n"
            )

            if retrieved_docs:
                for i, doc in enumerate(retrieved_docs, start=1):
                    answer += f"{i}. {doc['title']}\n"

                answer += (
                    "\nPlease also share the exact error message, when the issue started, "
                    "and whether this happens only in Teams or in other apps too."
                )
            else:
                answer += (
                    "I could not find enough related knowledge. Please share more details such as "
                    "error message, device type, and when the problem started."
                )
        else:
            answer = self.llm.generate(prompt)

        self.memory.add_message(session_id, "user", user_query)
        self.memory.add_message(session_id, "assistant", answer)

        return {
            "session_id": session_id,
            "predicted_intent": predicted_intent,
            "confidence": round(confidence, 4),
            "retrieved_docs": [doc["title"] for doc in retrieved_docs],
            "answer": answer
        }