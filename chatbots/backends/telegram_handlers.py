from telegram.ext import CommandHandler, MessageHandler, Filters
from .core import get_message

def send_message_action(text):
    def func(update, context):
        if callable(text):
            text = text()
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    return func

handlers = []
for cmd, text in get_message.items():
    action = send_message_action(text)
    handlers.append(CommandHandler(cmd, action))

unknown_msg_handler = MessageHandler(Filters.command, send_message_action(get_message['unknown']))
handlers.append(unknown_msg_handler)
