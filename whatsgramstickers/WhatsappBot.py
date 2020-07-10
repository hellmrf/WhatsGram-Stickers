import os
from io import BytesIO
import base64
from PIL import Image
from time import sleep
from typing import List
import logging
from concurrent.futures import ThreadPoolExecutor

from webwhatsapi import WhatsAPIDriver
from webwhatsapi.objects.message import Message
from BotActions import BotActions
from StickerSet import StickerSet
from User import User

logging.basicConfig(level=logging.INFO)


class WhatsappBot:

    def __init__(self, auto_run=False, auto_long_run=False, headless=False):
        self._chromedriver = os.environ.get('CHROMEDRIVE_PATH', os.path.join(os.path.dirname(__file__), "chromedriver"))
        self._profile_path = os.path.join(os.path.dirname(__file__), "chromeprofile")

        self._headless = headless
        self._driver = WhatsAPIDriver(
            username="API",
            client="chrome",
            profile=self._profile_path,
            executable_path=self._chromedriver,
            headless=self._headless,
            chrome_options=[
                "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
            ],
            heroku=True
        )
        self._bot_actions = BotActions(self._driver)

        self._thread_pool = ThreadPoolExecutor(max_workers=2)
        self._threaded_users = []

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
            if user[0] not in self._threaded_users:
                self._thread_pool.submit(self.create_sticker_pack, user)
                self._threaded_users.append(user[0])
                logging.info(f"{user[0]} added to queue.")
            else:
                logging.info(f"{user[0]} already in queue.")

    def keep_running(self) -> None:
        """
        Keeps running with self.run()
        :return:
        """

        while True:
            if not self._driver.is_logged_in():
                self._driver.screenshot('scrsht.png')
                self._driver.wait_for_login()
            try:
                self.run()
                sleep(2)
            except TypeError as err:
                logging.critical(err)
                logging.critical("---RESTARTING---")

    def create_sticker_pack(self, user_info: tuple) -> bool:
        """Create a sticker pack using StickerSet class."""
        wa_chat_id = user_info[0]
        package_title = user_info[1]
        tg_chat_id = user_info[2]

        logging.info(f"Running for {wa_chat_id}")

        # Get stickers messages
        stickers = self.list_user_unread_stickers(wa_chat_id)

        # Create sticker set
        sticker_set = StickerSet(tg_chat_id)
        name = sticker_set.create_new_sticker_set(package_title, stickers[0].save_media_buffer(True))

        if not name:
            logging.error(f"Can't create {wa_chat_id} pack: name = {name}")
            return False

        # Populate sticker set
        for sticker in stickers[1:]:
            stts = sticker_set.add_sticker_to_set(tg_chat_id, name, sticker.save_media_buffer(True))
            logging.info(f"Added a sticker to {name}: {stts}")

        # Send confirmation
        self._bot_actions.confirmation(wa_chat_id, name)

        logging.info(f"Finished {wa_chat_id}")

        # Remove user from threading
        if wa_chat_id in self._threaded_users:
            self._threaded_users.remove(wa_chat_id)

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
            print(f"[{message.chat_id} {message.timestamp}]: {message.content}")
            user_is_threaded = message.chat_id in self._threaded_users
            self.treat_message(message.chat_id, message.content, queued=user_is_threaded)
        elif User.get_stage(message.chat_id) == 0:
            self.treat_message(message.chat_id, "Hello")

    def list_user_unread_stickers(self, chat_id: str) -> List[Message]:
        messages: List[Message] = self._driver.get_all_messages_in_chat(chat_id)
        stickers = [message for message in messages if message.type == 'sticker']
        return stickers

    @staticmethod
    def upload_sticker_from_message(tg_user_id: int, sticker_message: Message) -> str:
        sticker = sticker_message.save_media_buffer(True)
        return StickerSet.upload_sticker(tg_user_id, sticker)

    def treat_message(self, chat_id: str, message: str, queued=False) -> bool:
        return self._bot_actions.answer(chat_id, message, queued=queued)

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
