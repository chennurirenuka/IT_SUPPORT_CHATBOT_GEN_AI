from fastapi import APIRouter, HTTPException
from app.schemas import ChatRequest, ChatResponse, HealthResponse
from app.services.rag_pipeline import RAGPipeline
from app.core.logger import get_logger
from config.settings import settings

router = APIRouter()
logger = get_logger(__name__)
pipeline = RAGPipeline()

@router.get("/health", response_model=HealthResponse)
def health_check():
    return {
        "status": "ok",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION
    }

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        logger.info(f"Received chat request for session_id={request.session_id}")
        result = pipeline.run(session_id=request.session_id, user_query=request.user_query)
        return result
    except Exception as e:
        logger.exception("Error while processing chat request")
        raise HTTPException(status_code=500, detail=str(e))
