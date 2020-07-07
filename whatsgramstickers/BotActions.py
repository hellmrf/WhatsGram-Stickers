from whatsgramstickers.webwhatsapi import WhatsAPIDriver
from whatsgramstickers.db import DB
from whatsgramstickers.User import User


class BotActions:
    BOT_MESSAGES = {
        "welcome": "Olá! Eu sou um robô 🤖 e consigo enviar figurinhas aqui do Whatsapp para o Telegram.\n\nPara "
                   "começar, envie ```/start```",
        "start": "Ótimo, me envie agora o nome do pacote que você deseja criar no Telegram.",
        "package_name": "Me envie também um id para seu pacote. Ele pode conter apenas letras (sem acentos), "
                        "\"_\" e números, e precisa começar com uma letra.\n\nSeu pacote de stickers será adicionado "
                        "usando um link como: t.me/addstickers/seu_id_aqui.",
        "send_me_stickers": "Ok. Agora me envie todas as figurinhas (no mínimo 3) que você quer adicionar ao pacote. "
                            "Quando terminar, envie `/done`.",
        "whats_your_telegram": "Estamos quase lá. Pra criar seu pacote, preciso te encontrar no Telegram. Meu nome lá "
                               "é @WhatsGramStickerBot (http://t.me/WhatsGramStickersBot). Por favor, me encontre, "
                               "me inicie e me envie o seguinte código:",
        "done": "Pronto! Seu pacote de figurinhas foi criado. Acesse "
                "http://t.me/addstickers/<id_do_seu_pack>_by_WhatsGramStickerBot para encontrá-lo!",
    }

    def __init__(self, driver: WhatsAPIDriver):
        self._driver = driver
        self._db = DB()

    def answer(self, chat_id: str, message: str) -> str:
        message_lower = message.lower()
        user = User(chat_id)
        stage = User.get_stage(chat_id)
        if '/start' in message_lower:
            text = self.start(chat_id)
            user.set_stage(1)
            return text
        elif '/cancel' in message_lower or '/quit' in message_lower:
            self.start(chat_id)
            return ""
        elif '/done' in message_lower and stage == 3:
            user.set_stage(5)
            return self.ask_for_telegram(chat_id)
        elif stage == 1:
            return self.read_package_title(chat_id, message)
        elif stage == 2:
            return self.read_package_name(chat_id, message)
        else:
            return self.welcome()

    def read_package_title(self, chat_id: str, message: str) -> str:
        # TODO
        User(chat_id).set_stage(2)
        return self.BOT_MESSAGES['package_name']

    def read_package_name(self, chat_id: str, message: str) -> str:
        # TODO
        User(chat_id).set_stage(3)
        return self.BOT_MESSAGES['send_me_stickers']

    def ask_for_telegram(self, chat_id: str) -> str:
        return self.BOT_MESSAGES['whats_your_telegram'] + f"\n\n{chat_id}"

    def welcome(self) -> str:
        return self.BOT_MESSAGES['welcome']

    def start(self, chat_id: str) -> str:
        self._driver.chat_send_seen(chat_id)
        User.clean_user(chat_id)
        return self.BOT_MESSAGES['start']

    def _clean_user(self, chat_id: str) -> bool:
        pass
