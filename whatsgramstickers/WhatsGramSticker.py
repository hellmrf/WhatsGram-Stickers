from whatsgramstickers.TelegramBot import TelegramBot
from whatsgramstickers.WhatsappBot import WhatsappBot


class WhatsGramSticker:

    def __init__(self, run_telegram=True, run_whatsapp=True):
        if run_telegram:
            self._telegram = TelegramBot()
        if run_whatsapp:
            self._whatsapp = WhatsappBot(auto_run=False, auto_long_run=False)
            self._whatsapp.keep_running()

            """while True:
                try:
                    self._whatsapp.run()
                    sleep(5)
                except TypeError:
                    print("------------------------")
                    print("---ERROR...RESTARTING---")
                    print("------------------------")
            """
