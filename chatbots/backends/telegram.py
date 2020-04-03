from telegram.ext import CommandHandler, Updater
from django.conf import settings
from .common import RunableBot
from .telegram_handlers import handlers
class TelegramBot(RunableBot):
    bot_type = 'telegram'
    def __init__(self):
        self.updater = None
    def setup(self):
        if not self.updater:
            return
        for h in handlers:
            self.updater.dispatcher.add_handler(h)
        self.updater.start_polling()

    def run(self, token=None):
        if token is None:
            token = settings.CHATBOTS_TELEGRAM_TOKEN
        if not token:
            raise ValueError("Malformed telegram bot token(settings.CHATBOTS_TELEGRAM_TOKEN)")
        self.updater = Updater(token=token, use_context=True)
        self.setup()

