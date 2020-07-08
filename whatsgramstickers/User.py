from whatsgramstickers.db import DB
"""
CREATE TABLE users
(
    id serial,
    chat_id character varying(32),
    package_name character varying(64),
    stage smallint,
    package_title character varying(64),
    telegram_id integer,
    PRIMARY KEY (id),
    UNIQUE (chat_id)
);
"""


class User:
    def __init__(self, chat_id: str):
        self.chat_id = chat_id

    def set_stage(self, new_stage: int) -> bool:
        if self._is_user_registered():
            return self._update_field('stage', new_stage)
        else:
            with DB() as db:
                db.cursor.execute("INSERT INTO users (chat_id, stage) VALUES (%s, %s)", (self.chat_id, new_stage, ))
                return db.cursor.rowcount > 0

    def set_package_title(self, new_package_title: str) -> bool:
        return self._update_field('package_title', new_package_title)

    def set_telegram_id(self, telegram_id: int) -> bool:
        return self._update_field('telegram_id', telegram_id)

    def _update_field(self, field: str, new_value) -> bool:
        if field not in ['stage', 'package_title', 'telegram_id']:
            # Just for integrity
            return False
        with DB() as db:
            if self._is_user_registered():
                db.cursor.execute("UPDATE users SET "+field+" = %s WHERE chat_id = %s", (new_value, self.chat_id, ))
                return db.cursor.rowcount > 0
            else:
                return False

    @staticmethod
    def get_stage(chat_id: str) -> int:
        with DB() as db:
            db.cursor.execute("SELECT stage FROM users WHERE chat_id = %s", (chat_id, ))
            response = db.cursor.fetchone()
            if response is None:
                return 0
            else:
                return response[0]

    def user_has_telegram_id(self) -> bool:
        """Check if user already have a telegram id registered"""
        with DB() as db:
            db.cursor.execute("SELECT telegram_id FROM users WHERE chat_id = %s", (self.chat_id, ))
            response = db.cursor.fetchone()
            if response is None:
                return False
            else:
                return bool(response[0])

    @staticmethod
    def is_telegram_id_registered(tg_chat_id: int) -> bool:
        """Check if this Telegram ID is registered"""
        with DB() as db:
            db.cursor.execute("SELECT * FROM users WHERE telegram_id = %s", (tg_chat_id, ))
            response = db.cursor.fetchone()
            if response is None:
                return False
            else:
                return bool(response[0])

    def _is_user_registered(self) -> bool:
        with DB() as db:
            db.cursor.execute("SELECT stage FROM users WHERE chat_id = %s", (self.chat_id,))
            return db.cursor.fetchone() is not None

    @staticmethod
    def find_users_in_last_stage() -> list:
        with DB() as db:
            db.cursor.execute("SELECT chat_id, package_title, telegram_id FROM users "
                              "WHERE stage = 6 "
                              "AND package_title != '' "
                              "AND telegram_id != 0")
            return list(db.cursor.fetchall())

    @staticmethod
    def clean_user(chat_id: str) -> bool:
        with DB() as db:
            db.cursor.execute("UPDATE users SET stage = 0, package_name = NULL, package_title = NULL WHERE chat_id = "
                              "%s", (chat_id,))
            return db.cursor.rowcount > 0
