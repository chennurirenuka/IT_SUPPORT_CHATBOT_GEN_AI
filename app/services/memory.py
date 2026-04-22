import sqlite3
from config.settings import settings

class SessionMemory:
    def __init__(self):
        self.conn = sqlite3.connect(settings.MEMORY_DB, check_same_thread=False)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            message TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_message(self, session_id: str, role: str, message: str):
        query = "INSERT INTO conversations (session_id, role, message) VALUES (?, ?, ?)"
        self.conn.execute(query, (session_id, role, message))
        self.conn.commit()

    def get_history(self, session_id: str, limit: int = 6):
        query = """
        SELECT role, message FROM conversations
        WHERE session_id = ?
        ORDER BY id DESC
        LIMIT ?
        """
        rows = self.conn.execute(query, (session_id, limit)).fetchall()
        rows.reverse()
        return rows
