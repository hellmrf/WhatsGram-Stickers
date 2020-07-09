import os
import re
import requests
from io import BytesIO
from typing import Union
import logging

from TelegramBot import TelegramBot

with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "credentials", "TelegramApiKey.txt"), 'r') as fl:
    API_KEY = fl.readline()

DEFAULT_EMOJI = u"😍"


class StickerSet:

    def __init__(self, user_id: int):
        self.user_id = user_id

    def create_new_sticker_set(self, set_title: str, first_sticker: Union[str, BytesIO], emojis: str = DEFAULT_EMOJI, set_name: str = None) -> Union[str, bool]:
        """ Create a new sticker set and returns its name or False """
        if not self.validate_set_title(set_title):
            return False

        if not set_name or not self.validate_set_name(set_name):
            set_name = self.generate_package_name_by_title(set_title)

        url = f"https://api.telegram.org/bot{API_KEY}/createNewStickerSet"

        if isinstance(first_sticker, str):
            data = {
                'user_id': self.user_id,
                'name': set_name,
                'title': set_title,
                'png_sticker': first_sticker,
                u'emojis': u'😍'
            }
            response = requests.post(url, data=data)
        else:
            data = {
                'user_id': self.user_id,
                'name': set_name,
                'title': set_title,
                u'emojis': u'😍'
            }
            response = requests.post(url, data=data, files={'png_sticker': first_sticker})
        if response.status_code == 200:
            return set_name
        else:
            logging.error("StickerSet.create_new_sticker_set(): error creating the new sticker set")
            logging.error(f"Status: {response.status_code}")
            logging.error(response.json())
            return False

    @staticmethod
    def upload_sticker(user_id: int, sticker: BytesIO) -> str:
        logging.warning("Uploading sticker before adding to a set is not necessary. Use add_sticker_to_set() directly.")
        url = f"https://api.telegram.org/bot{API_KEY}/uploadStickerFile"
        response = requests.post(url, data={'user_id': user_id}, files={'png_sticker': sticker})
        if response.status_code != 200:
            logging.error("StickerSet.upload_sticker(): Error uploading sticker.")
            logging.error(f"Status: {response.status_code}")
            logging.error(response.json())
            return ""
        data = response.json()
        return data['result']['file_id']

    @staticmethod
    def add_sticker_to_set(user_id: int, set_name: str, sticker: Union[str, BytesIO], emojis: str = DEFAULT_EMOJI) -> bool:
        url = f"https://api.telegram.org/bot{API_KEY}/addStickerToSet"
        if isinstance(sticker, str):
            data = {
                'user_id': user_id,
                'name': set_name,
                'png_sticker': sticker,
                u'emojis': u'😀'
            }
            response = requests.post(url, data=data)
        else:
            data = {
                'user_id': user_id,
                'name': set_name,
                u'emojis': u'😀'
            }
            response = requests.post(url, data=data, files={'png_sticker': sticker})

        if response.status_code == 200:
            return True
        else:
            logging.error("StickerSet.add_sticker_to_set(): error adding sticker")
            logging.error(f"Status: {response.status_code}")
            logging.error(response.json())
            return False

    @staticmethod
    def generate_package_name_by_title(title: str) -> str:
        # Replace spaces with _
        name = title.replace(' ', '_')

        # Remove special characters
        name = re.sub(r'[^A-Z0-9_]*', '', name, flags=re.IGNORECASE)

        # Remove consecutive underscores
        name = re.sub(r'(_+)', '_', name, flags=re.IGNORECASE)

        # Remove underscores at the end
        name = re.sub(r'_+$', '', name, flags=re.IGNORECASE)

        # Remove non letters at beginning
        name = re.sub(r'^[^A-Z]+', '', name, flags=re.IGNORECASE)

        # Get only 40 first characters to sum up to 64 when append bot username
        name = name[:40]

        # Check length
        bot_suffix = '_by_' + TelegramBot.get_bot_username()
        max_length = 64 - len(bot_suffix)
        if len(name) > max_length:
            name = name[:max_length]

        # Check validity. If not valid, enter despair mode and generate random characters.
        if not StickerSet.validate_set_name(name):
            import random
            import string
            letters = string.ascii_letters + '1234567890'
            random_letters = ''.join(random.choice(letters) for i in range(30))
            name = "a"+random_letters  # never begin with non letters.

        # Append bot username
        if not name.lower().endswith(bot_suffix.lower()):
            name = name + bot_suffix

        return name

    @staticmethod
    def validate_set_name(name: str) -> bool:
        """
        Can contain only english letters, digits and underscores. Must begin with a letter, can't contain consecutive
        underscores and must end in “_by_<bot username>”. <bot_username> is case insensitive. 1-64 characters.
        """
        bot_username = TelegramBot.get_bot_username()
        if not name.lower().endswith(bot_username.lower()):
            name = name + '_by_' + bot_username

        # Check length (up to 64) considering the username at the end.
        if len(name) not in range(len(bot_username) + 5, 65):
            logging.warning("StickerSet.validate_set_name(): Invalid length.")
            return False

        # Check if contain only english letters, digits and underscore and if begin with a letter.
        elif not re.match(r'^[A-Z][A-Z0-9_]{1,62}[A-Z0-9]$', name, re.IGNORECASE):
            logging.warning("StickerSet.validate_set_name(): Invalid package name.")
            return False

        # Check if it doesn't contain consecutive underscores.
        elif '__' in name:
            logging.warning("StickerSet.validate_set_name(): Invalid subsequent underscores.")
            return False

        # Alright.
        return True

    @staticmethod
    def validate_set_title(name: str) -> bool:
        """ 1-64 characters. """
        return len(name) in range(1, 65)