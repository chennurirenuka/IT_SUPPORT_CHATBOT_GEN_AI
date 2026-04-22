from typing import List, Tuple

def build_prompt(user_query: str, predicted_intent: str, confidence: float, retrieved_docs: List[dict], history: List[Tuple[str, str]]) -> str:
    history_text = "\n".join([f"{role}: {message}" for role, message in history])

    docs_text = "\n\n".join([
        f"Title: {doc['title']}\nCategory: {doc['category']}\nContent: {doc['content']}"
        for doc in retrieved_docs
    ])

    prompt = f"""
You are an enterprise IT support assistant.

Instructions:
- give step-by-step troubleshooting
- use retrieved knowledge first
- use history to avoid repeating already suggested steps
- if confidence is low, mention that clarification may help
- if issue is unresolved, suggest escalation

Predicted intent: {predicted_intent}
Intent confidence: {confidence:.2f}

Conversation history:
{history_text}

Retrieved knowledge:
{docs_text}

User query:
{user_query}

Generate a professional support answer.
"""
    return prompt.strip()
