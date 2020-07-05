from whatsgramstickers.webwhatsapi import WhatsAPIDriver


class BotActions:
    BOT_MESSAGES = {
        "welcome": "Olá! Eu sou um robô 🤖 e consigo enviar figurinhas aqui do Whatsapp para o Telegram.\n\nPara "
                   "começar, envie ```/start```",
        "start": "Ótimo, me envie agora o nome do pacote que você deseja criar no Telegram.",
    }

    def __init__(self, driver: WhatsAPIDriver):
        self._driver = driver

    def welcome(self) -> str:
        return self.BOT_MESSAGES['welcome']

    def start(self, chat_id: str) -> str:
        self._driver.chat_send_seen(chat_id)
        return self.BOT_MESSAGES['start'] + f"\n\nAgora eu devo salvar seu id <{chat_id}> para mais tarde."
