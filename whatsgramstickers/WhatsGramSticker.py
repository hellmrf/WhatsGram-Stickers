import os
import re
from io import BytesIO
import base64
from PIL import Image
from time import sleep

from whatsgramstickers.webwhatsapi import WhatsAPIDriver
from whatsgramstickers.BotActions import BotActions


class WhatsGramSticker:

    def __init__(self, start=True):
        self._chromedriver = os.path.join(os.path.dirname(__file__), "chromedriver")
        self._profile_path = os.path.join(os.path.dirname(__file__), "chromeprofile")
        self._headless = False
        self._driver = WhatsAPIDriver(username="API", client="chrome", profile=self._profile_path,
                                      executable_path=self._chromedriver)
        self._bot_actions = BotActions(self._driver)

        # print(self._driver.get_all_chats())
        if start:
            self.listen_messages()

    def listen_messages(self) -> None:
        """
        Keeps listening for new messages.
        :return:
        """
        while True:
            try:
                self.check_for_unread_messages()
                sleep(5)
            except TypeError:
                print("------------------------")
                print("---ERROR...RESTARTING---")
                print("------------------------")

    def check_for_unread_messages(self) -> None:
        """
        Check for unread messages and call actions
        :return:
        """
        unread = self._driver.get_unread()
        for msg_group in unread:
            print(f'Message from <{msg_group.chat.id}>.')
            for message in msg_group.messages:
                print("--------------------------------------------------------------")
                print(f"{message.type} from {message.sender}.")
                if message.type == 'chat':
                    print(f"[{message.timestamp}]: {message.content}")
                    self._driver.send_message_to_id(message.chat_id,
                                                    self.treat_message(message.chat_id, message.content))
                elif message.type == 'sticker':
                    print(f'[       Size]: {message.size}')
                    print(f'[       MIME]: {message.mime}')
                    print(f'[    Caption]: {message.caption}')
                    print(f'[  Media Key]: {message.media_key}')
                    print(f'[ Client URL]: {message.client_url}')
                    print(f'[   Filename]: {message.filename}')
                    sticker = message.save_media_buffer(True)
                    image_base64 = self.convert_sticker_to_png_base64(sticker)
                    self.temp_save_to_txt(image_base64)
                print(f'Chat id: {message.chat_id}')
                print("--------------------------------------------------------------")

    def treat_message(self, chat_id: str, message: str) -> str:
        message_lower = message.lower()
        if '/start' in message_lower:
            return self._bot_actions.start(chat_id)
        else:
            return self._bot_actions.welcome()

    @staticmethod
    def convert_sticker_to_png_base64(sticker: BytesIO) -> str:
        """
        Converts a sticker file (webp) to base64 string (png)
        :param sticker: the sticker to be converted
        :return: the base64 string
        """
        file = BytesIO()
        img = Image.open(sticker)
        img.save(file, 'png')

        base64_content = base64.b64encode(file.getvalue()).decode()
        base64_string = 'data:image/png;base64,' + base64_content
        return base64_string

    # TODO: remove that
    @staticmethod
    def temp_response(msg: str) -> str:
        if re.search(r'(oi|ola|olá|hi|hello)', msg, re.IGNORECASE):
            return "Olá!! Tudo bem?"
        elif 'te amo' in msg.lower():
            return "Eu também amo você!"
        elif 'fofinho' in msg.lower():
            return "Você também é muito fofx!"
        elif 'tchau' in msg.lower():
            return "Que pena que você já vai :(. Tchauzinho. Bom conversar com você."
        else:
            return "Ehr... Bruh... Pi pi pi... Ainda não aprendi o que você disse..."

    # TODO: remove that
    @staticmethod
    def temp_save_to_txt(base64_string: str) -> None:
        with open("/home/helitonmrf/Projects/WhatsGram_Stickers/test/sticker.html", 'w') as fl:
            fl.write(f"<img src='{base64_string}' />")
