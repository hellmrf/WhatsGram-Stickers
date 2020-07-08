import os
import re
import logging
import requests
from io import BytesIO

with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "credentials", "TelegramApiKey.txt"), 'r') as fl:
    API_KEY = fl.readline()

DEFAULT_EMOJI = u"🗨"


class StickerSet:

    def __init__(self, user_id: int):
        self.user_id = user_id

    def create_new_sticker_set(self, set_name: str, set_title: str, first_sticker: str, emojis: str = DEFAULT_EMOJI) -> bool:
        if not self.validate_set_name(set_name):
            return False
        if not self.validate_set_title(set_title):
            return False

        url = f"https://api.telegram.org/bot{API_KEY}/createNewStickerSet"
        data = {
            'user_id': self.user_id,
            'name': set_name,
            'title': set_title,
            'png_sticker': first_sticker,
            u'emojis': u'😍'
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            return True
        else:
            logging.error("StickerSet.create_new_sticker_set(): error creating the new sticker set")
            logging.error(f"Status: {response.status_code}")
            logging.error(response.json())
            return False

    @staticmethod
    def upload_sticker(user_id: int, sticker: BytesIO) -> str:
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
    def add_sticker_to_set(user_id: int, set_name: str, sticker: str, emojis: str = DEFAULT_EMOJI) -> bool:
        url = f"https://api.telegram.org/bot{API_KEY}/addStickerToSet"
        data = {
            'user_id': user_id,
            'name': set_name,
            'png_sticker': sticker,
            u'emojis': u'😀'
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            return True
        else:
            logging.error("StickerSet.add_sticker_to_set(): error adding sticker")
            logging.error(f"Status: {response.status_code}")
            logging.error(response.json())
            return False

    @staticmethod
    def validate_set_name(name: str) -> bool:
        """
        Can contain only english letters, digits and underscores. Must begin with a letter, can't contain consecutive
        underscores and must end in “_by_<bot username>”. <bot_username> is case insensitive. 1-64 characters.
        """
        if not name.lower().endswith('_by_whatsgramstickersbot'):
            name = name + '_by_WhatsGramStickersBot'

        # Check length (up to 64) considering the  at the end.
        if len(name) not in range(1, 65):
            logging.warning("StickerSet.validate_set_name(): Invalid length.")
            return False

        # Check if contain only english letters, digits and underscore and if begin with a letter.
        elif not re.match(r'^\w[A-Za-z0-9_]+$', name, re.IGNORECASE):
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