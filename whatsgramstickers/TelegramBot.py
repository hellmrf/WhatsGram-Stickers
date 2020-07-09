from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os
import re
from Constants import STAGES
from BotMessages import TELEGRAM_MESSAGES

from User import User

with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "credentials", "TelegramApiKey.txt"), 'r') as fl:
    API_KEY = fl.readline()


class TelegramBot:
    def __init__(self):
        self.main()

    def start(self, update: Update, context: CallbackContext) -> None:
        """Send a message when the command /start is issued."""
        update.message.reply_text(TELEGRAM_MESSAGES['start'], parse_mode="HTML")

    def help_command(self, update: Update, context: CallbackContext) -> None:
        """Send a message when the command /help is issued."""
        update.message.reply_text(TELEGRAM_MESSAGES['help'], parse_mode="HTML")

    def receive_code(self, update: Update, context: CallbackContext) -> None:
        """Receive the code, check if is it valid and start StickerSet creation"""
        if re.match(r'^\d+@c\.us$', update.message.text):
            wa_chat_id = update.message.text
            tg_chat_id = update.message.chat_id
            user = User(wa_chat_id)
            user.set_telegram_id(tg_chat_id)
            if user.get_stage(wa_chat_id) == STAGES['WAITING_FOR_TELEGRAM']:
                user.set_stage(STAGES['GENERATE_STICKERS'])
            update.message.reply_text(TELEGRAM_MESSAGES['creating'], parse_mode="HTML")
        else:
            self.start(update, context)

    def main(self) -> None:
        """Start the bot."""
        updater = Updater(API_KEY, use_context=True)

        # Get the dispatcher to register handlers
        dp = updater.dispatcher

        # Register handlers
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(CommandHandler("help", self.help_command))
        dp.add_handler(MessageHandler(Filters.text, self.receive_code))

        updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        # updater.idle()

    @staticmethod
    def get_bot_username() -> str:
        """Return the bot username without '@'."""
        return "WhatsGramStickersBot"
        # TODO: how to make this faster and dynamic?
        # return Bot(API_KEY).name[1:]
