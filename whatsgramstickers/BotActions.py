from whatsgramstickers.webwhatsapi import WhatsAPIDriver
from whatsgramstickers.db import DB
from whatsgramstickers.User import User


class BotActions:
    BOT_MESSAGES = {
        "welcome": "Olá! Eu sou um robô 🤖 e consigo enviar figurinhas aqui do Whatsapp para o Telegram.\n\nPara "
                   "começar, envie ```/start```",
        "start": "Ótimo, me envie agora o nome do pacote que você deseja criar no Telegram.",
    }

    def __init__(self, driver: WhatsAPIDriver):
        self._driver = driver
        self._db = DB()

    def answer(self, chat_id: str, message: str) -> str:
        message_lower = message.lower()
        if '/start' in message_lower:
            return self.start(chat_id)
        else:
            return self.welcome()

    def welcome(self) -> str:
        return self.BOT_MESSAGES['welcome']

    def start(self, chat_id: str) -> str:
        self._driver.chat_send_seen(chat_id)
        return self.BOT_MESSAGES['start']

    def _clean_user(self, chat_id: str) -> bool:
        pass

