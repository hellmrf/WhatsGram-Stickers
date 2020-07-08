import os
from io import BytesIO
import base64
from PIL import Image
from time import sleep
from typing import List
import logging

from whatsgramstickers.webwhatsapi import WhatsAPIDriver
from whatsgramstickers.webwhatsapi.objects.message import Message
from whatsgramstickers.BotActions import BotActions
from whatsgramstickers.StickerSet import StickerSet
from whatsgramstickers.User import User


class WhatsappBot:

    def __init__(self, auto_run=False, auto_long_run=False):
        self._chromedriver = os.path.join(os.path.dirname(__file__), "chromedriver")
        self._profile_path = os.path.join(os.path.dirname(__file__), "chromeprofile")
        self._headless = False
        self._driver = WhatsAPIDriver(username="API", client="chrome", profile=self._profile_path,
                                      executable_path=self._chromedriver)
        self._bot_actions = BotActions(self._driver)

        if auto_long_run:
            self.keep_running()
        elif auto_run:
            self.run()

    def run(self) -> None:
        """
        • Check if there's some user with status == 6 (if yes, generate sticker pack)
        • Listen to new messages
            Here we can either keep listening to new messages (long_run == True) or check just once.
        """

        # Check for new messages
        self.check_for_unread_messages()

        # Check for users waiting the pack
        user_in_last_stage = User.find_users_in_last_stage()
        for user in user_in_last_stage:
            self.create_sticker_pack(user)

    def keep_running(self) -> None:
        """
        Keeps running with self.run()
        :return:
        """
        while True:
            try:
                self.run()
                sleep(2)
            except TypeError:
                logging.critical("---ERROR...RESTARTING---")

    def create_sticker_pack(self, user_info: tuple) -> bool:
        """Create a sticker pack using StickerSet class."""
        wa_chat_id = user_info[0]
        package_title = user_info[1]
        tg_chat_id = user_info[2]

        # Get stickers messages
        stickers = self.list_user_unread_stickers(wa_chat_id)

        # Upload stickers
        uploaded_stickers = []
        for sticker in stickers:
            uploaded_stickers.append(self.upload_sticker_from_message(tg_chat_id, sticker))
        if not uploaded_stickers:
            return False

        # Create sticker set
        sticker_set = StickerSet(tg_chat_id)
        name = sticker_set.create_new_sticker_set(package_title, uploaded_stickers[0])

        if not name:
            return False

        # Populate sticker set
        for uploaded_sticker in uploaded_stickers[1:]:
            print(sticker_set.add_sticker_to_set(tg_chat_id, name, uploaded_sticker))

        # Send confirmation
        self._bot_actions.confirmation(wa_chat_id, name)
        return True

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

    def process_incoming_message(self, message: Message) -> None:
        # Message properties: https://gist.github.com/hellmrf/6e06fc374bb43de0868fbb57c223aecd
        if message.type == 'chat':
            print(f"[{message.timestamp}]: {message.content}")
            self.treat_message(message.chat_id, message.content)
        elif User.get_stage(message.chat_id) == 0:
            self.treat_message(message.chat_id, "a")

    def list_user_unread_stickers(self, chat_id: str) -> List[Message]:
        messages: List[Message] = self._driver.get_all_messages_in_chat(chat_id)
        stickers = [message for message in messages if message.type == 'sticker']
        return stickers

    @staticmethod
    def upload_sticker_from_message(tg_user_id: int, sticker_message: Message) -> str:
        sticker = sticker_message.save_media_buffer(True)
        return StickerSet.upload_sticker(tg_user_id, sticker)

    def treat_message(self, chat_id: str, message: str) -> bool:
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
    def temp_save_to_txt(base64_string: str, suffix="") -> None:
        with open(f"/home/helitonmrf/Projects/WhatsGram_Stickers/test/sticker{suffix}.html", 'w') as fl:
            fl.write(f"<img src='{base64_string}' />")
