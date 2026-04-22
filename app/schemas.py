from pydantic import BaseModel
from typing import List

class ChatRequest(BaseModel):
    session_id: str
    user_query: str

class ChatResponse(BaseModel):
    session_id: str
    predicted_intent: str
    confidence: float
    retrieved_docs: List[str]
    answer: str

class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
