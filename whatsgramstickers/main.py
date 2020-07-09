from telegram.utils import request
from TelegramBot import TelegramBot
from WhatsappBot import WhatsappBot

request.CON_POOL_SIZE = 10


class WhatsGramSticker:

    def __init__(self, run_telegram=True, run_whatsapp=True):
        if run_telegram:
            self._telegram = TelegramBot()
        if run_whatsapp:
            self._whatsapp = WhatsappBot(headless=False)
            self._whatsapp.keep_running()


if __name__ == '__main__':
    WGS = WhatsGramSticker()
