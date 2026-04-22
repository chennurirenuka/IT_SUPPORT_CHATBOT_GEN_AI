import redis
from config.settings import settings

class RedisSessionMemory:
    def __init__(self):
        self.client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)

    def add_message(self, session_id: str, role: str, message: str):
        key = f"chat:{session_id}"
        self.client.rpush(key, f"{role}:{message}")

    def get_history(self, session_id: str, limit: int = 6):
        key = f"chat:{session_id}"
        messages = self.client.lrange(key, -limit, -1)
        history = []
        for item in messages:
            if ":" in item:
                role, message = item.split(":", 1)
                history.append((role, message))
        return history
