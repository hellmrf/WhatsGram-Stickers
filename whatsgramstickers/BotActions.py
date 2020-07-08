import re
import json
from whatsgramstickers.webwhatsapi import WhatsAPIDriver
from whatsgramstickers.db import DB
from whatsgramstickers.User import User
from whatsgramstickers.StickerSet import StickerSet


class BotActions:

    def __init__(self, driver: WhatsAPIDriver):
        with open('BotMessages.json', 'r') as fl:
            self.BOT_MESSAGES = json.load(fl)
        self._driver = driver
        self._db = DB()

    def answer(self, chat_id: str, message: str) -> bool:
        message_lower = message.lower()
        user = User(chat_id)
        stage = User.get_stage(chat_id)
        if '/start' in message_lower:
            self.start(chat_id)
            user.set_stage(1)
            return True
        elif '/cancel' in message_lower or '/quit' in message_lower:
            self.cancel(chat_id)
            return True
        elif '/done' in message_lower and stage == 3:
            user.set_stage(5)
            return self.ask_for_telegram(chat_id)
        elif stage == 1:
            return self.read_package_title(chat_id, message)
        elif stage == 2:
            return self.read_package_name(chat_id, message)
        else:
            return self.welcome(chat_id)

    def read_package_title(self, chat_id: str, message: str) -> bool:
        # TODO read package title
        title = message.strip()
        if not StickerSet.validate_set_title(title):
            return False
        user = User(chat_id)
        user.set_stage(2)
        user.set_package_title(title)
        self._send_message(chat_id, self.BOT_MESSAGES['package_name'])
        return True

    def read_package_name(self, chat_id: str, message: str) -> bool:
        # TODO read package name
        # _by_WhatsGramStickersBot
        name = message.strip()
        if not StickerSet.validate_set_name(name):
            self._send_message(chat_id, self.BOT_MESSAGES['package_name_error'])
            return False
        user = User(chat_id)
        set_name_success = user.set_package_name(name+'_by_WhatsGramStickersBot')
        if not set_name_success:
            return False
        user.set_stage(3)
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
