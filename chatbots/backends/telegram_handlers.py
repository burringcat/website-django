from random import choice

from telegram.ext import CommandHandler, MessageHandler, Filters

def on_start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Nyaaawwn~~ Hello! I'm awake :3")
start_handler = CommandHandler('start', on_start)

def yn(update, context):
    yn = choice(("Yes.", "No."))
    context.bot.send_message(chat_id=update.effective_chat.id, text=yn)
yn_handler = CommandHandler('yn', yn)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm sorry? Uhm, what did you say?")
unknown_msg_handler = MessageHandler(Filters.command, unknown)
