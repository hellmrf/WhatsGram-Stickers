import os
import re
from io import BytesIO
import base64
from PIL import Image
from time import sleep

from whatsgramstickers.webwhatsapi import WhatsAPIDriver
from whatsgramstickers.webwhatsapi.objects.message import Message
from whatsgramstickers.BotActions import BotActions
from whatsgramstickers.User import User


class WhatsappBot:

    def __init__(self, auto_run=False):
        self._chromedriver = os.path.join(os.path.dirname(__file__), "chromedriver")
        self._profile_path = os.path.join(os.path.dirname(__file__), "chromeprofile")
        self._headless = False
        self._driver = WhatsAPIDriver(username="API", client="chrome", profile=self._profile_path,
                                      executable_path=self._chromedriver)
        self._bot_actions = BotActions(self._driver)

        if auto_run:
            self.run()

    def run(self, long_run=False) -> None:
        """
        • Check if there's some user with status == 6 (if yes, generate sticker pack)
        • Listen to new messages
            Here we can either keep listening to new messages (long_run == True) or check just once.
        """

        # Check for users waiting the pack
        if User.find_users_in_last_stage():
            pass

        # Check for new messages
        if long_run:
            self.listen_messages()
        else:
            self.check_for_unread_messages()

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
                self.process_incoming_message(message)

    def process_incoming_message(self, message: Message):
        # Message properties: https://gist.github.com/hellmrf/6e06fc374bb43de0868fbb57c223aecd
        if message.type == 'chat':
            print(f"[{message.timestamp}]: {message.content}")
            treat_msg = self.treat_message(message.chat_id, message.content)
            self._driver.send_message_to_id(message.chat_id, treat_msg)
        elif message.type == 'sticker':
            pass
            # sticker = message.save_media_buffer(True)
            # image_base64 = self.convert_sticker_to_png_base64(sticker)

    def treat_message(self, chat_id: str, message: str) -> str:
        return self._bot_actions.answer(chat_id, message)

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
