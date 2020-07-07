from telegram import Update, Message
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os
import re

from whatsgramstickers.User import User

with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "credentials", "TelegramApiKey.txt"), 'r') as fl:
    API_KEY = fl.readline()


class TelegramBot:
    def __init__(self):
        self.main()

    def start(self, update: Update, context: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        text = "Hi! To migrate your Whatsapp Stickers to Telegram, you'll need first message me in Whatsapp. Please, " \
               "send me a message to https://wa.me/5531971352054.\n\nIf you already have your code, please send-me."
        update.message.reply_text(text)

    def help_command(self, update: Update, context: CallbackContext) -> None:
        """Send a message when the command /help is issued."""
        text = "Hi! To migrate your Whatsapp Stickers to Telegram, you'll need first message me in Whatsapp. Please, " \
               "send me a message to https://wa.me/5531971352054 so I can guide you through next steps. At the end, " \
               "I'll send you (until via Whatsapp) a code that you will send me here.\n\nIf you already have your " \
               "code, please send-me.\n\nIf you have other questions, contact my human father at @helitonmrf."
        update.message.reply_text(text)

    def receive_code(self, update: Update, context: CallbackContext) -> None:
        """Receive the code, check if is it valid and start StickerSet creation"""
        if re.search(r'^\d+@c\.us$', update.message.text):
            wa_chat_id = update.message.text
            tg_chat_id = update.message.chat_id
            user = User(wa_chat_id)
            user.set_telegram_id(tg_chat_id)
            if user.get_stage(wa_chat_id) == 5:
                user.set_stage(6)
            update.message.reply_text("Great! Wait a little more, please. I'm creating your fancy sticker set!")
        else:
            self.start(update, context)

    def main(self) -> None:
        """Start the bot."""
        # Create the Updater and pass it your bot's token.
        # Make sure to set use_context=True to use the new context based callbacks
        # Post version 12 this will no longer be necessary
        updater = Updater(API_KEY, use_context=True)

        # Get the dispatcher to register handlers
        dp = updater.dispatcher

        # on different commands - answer in Telegram
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(CommandHandler("help", self.help_command))

        # on noncommand i.e message - echo the message on Telegram
        dp.add_handler(MessageHandler(Filters.text, self.receive_code))

        # Start the Bot
        updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        # updater.idle()
