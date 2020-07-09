import logging
from webwhatsapi import WhatsAPIDriver
from db import DB
from User import User
from StickerSet import StickerSet
from BotMessages import WHATSAPP_MESSAGES
from Constants import STAGES


class BotActions:

    def __init__(self, driver: WhatsAPIDriver):
        self.BOT_MESSAGES = WHATSAPP_MESSAGES
        self._driver = driver
        self._db = DB()

    def answer(self, chat_id: str, message: str) -> bool:
        message_lower = message.lower()
        user = User(chat_id)
        stage = User.get_stage(chat_id)
        if '/start' in message_lower:
            self.start(chat_id)
            user.set_stage(STAGES['WAITING_PACKAGE_TITLE'])
            return True
        elif '/cancel' in message_lower or '/quit' in message_lower:
            self.cancel(chat_id)
            return True
        elif '/done' in message_lower and stage == STAGES['WAITING_STICKERS']:
            user.set_stage(STAGES['WAITING_FOR_TELEGRAM'])
            return self.ask_for_telegram(chat_id)
        elif stage == STAGES['WAITING_PACKAGE_TITLE']:
            return self.read_package_title(chat_id, message)
        elif stage == STAGES['REMOVED_WAITING_PACKAGE_NAME']:
            user.set_stage(STAGES['WAITING_STICKERS'])
            return True
            # return self.read_package_name(chat_id, message)
        else:
            return self.welcome(chat_id)

    def read_package_title(self, chat_id: str, message: str) -> bool:
        # TODO read package title
        title = message.strip()
        if not StickerSet.validate_set_title(title):
            logging.warning(f"BotActions.read_package_title(): {title} rejected.")
            self._send_message(chat_id, self.BOT_MESSAGES['invalid_package_title'])
            return False
        user = User(chat_id)
        user.set_stage(STAGES['WAITING_STICKERS'])
        user.set_package_title(title)
        self._send_message(chat_id, self.BOT_MESSAGES['send_me_stickers'])
        return True

    def ask_for_telegram(self, chat_id: str) -> bool:
        text = self.BOT_MESSAGES['whats_your_telegram']
        self._send_message(chat_id, text)
        self._send_message(chat_id, str(chat_id))
        return True

    def welcome(self, chat_id: str) -> bool:
        text = self.BOT_MESSAGES['welcome']
        self._send_message(chat_id, text)
        return True

    def start(self, chat_id: str) -> bool:
        self._clean_user(chat_id)
        text = self.BOT_MESSAGES['start']
        self._send_message(chat_id, text)
        return True

    def cancel(self, chat_id: str) -> bool:
        return self._clean_user(chat_id)

    def confirmation(self, chat_id: str, package_name: str) -> None:
        text = self.BOT_MESSAGES['done'].format(package_name)
        self._clean_user(chat_id)
        self._send_message(chat_id, text)

    def _clean_user(self, chat_id: str) -> bool:
        self._driver.delete_chat(chat_id)
        User.clean_user(chat_id)
        return True

    def _send_message(self, chat_id: str, text: str) -> None:
        self._driver.send_message_to_id(chat_id, text)
