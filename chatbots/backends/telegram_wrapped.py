from telegram.ext import CommandHandler, Updater, MessageHandler, Filters
from django.conf import settings
from .common import RunableBot
from .core import message_on_unknown_command, message_on_start, message_yes_or_no
def on_start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=message_on_start)
on_start_handler = CommandHandler('start', on_start)

def on_unknown_command(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=message_on_unknown_command)
on_unknown_command_handler = MessageHandler(Filters.command, on_unknown_command)

def on_yn(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=message_yes_or_no())
on_yn_handler = CommandHandler('yn', on_yn)
class TelegramBotWrapped(RunableBot):
    bot_type = 'telegram-wrapped'
    def __init__(self):
        self.updater = None

    def setup(self):
        if not self.updater:
            return
        self.updater.dispatcher.add_handler(on_start_handler)
        self.updater.dispatcher.add_handler(on_yn_handler)
        self.updater.dispatcher.add_handler(on_unknown_command_handler)

        self.updater.start_polling()

    def run(self, token=None):
        if token is None:
            token = settings.CHATBOTS_TELEGRAM_TOKEN
        if not token:
            raise ValueError("Malformed telegram bot token(settings.CHATBOTS_TELEGRAM_TOKEN)")
        self.updater = Updater(token=token, use_context=True)
        self.setup()

