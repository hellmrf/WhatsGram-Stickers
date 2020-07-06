from whatsgramstickers.webwhatsapi import WhatsAPIDriver
from whatsgramstickers.db import DB


class User:
    def __init__(self, chat_id: str):
        self.chat_id = chat_id

    def set_stage(self, new_stage: int) -> bool:
        with DB() as db:
            db.cursor.execute("UPDATE users SET stage = %s WHERE chat_id = %s", (new_stage, self.chat_id, ))
            return db.cursor.rowcount > 0

    @staticmethod
    def get_stage(chat_id: str) -> int:
        with DB() as db:
            db.cursor.execute("SELECT stage FROM users WHERE chat_id = %s", (chat_id, ))
            response = db.cursor.fetchone()
            if response is None:
                return 0
            else:
                return response[0]
