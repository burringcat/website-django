import sys
from .core import *
from .common import RunableBot
class ShellBot(RunableBot):
    bot_type = 'shell'
    def run(self):
        prompt = ">>> "
        print(message_on_start)
        while True:
            cmd = input(prompt).split(' ')[0]
            text = get_message[cmd]
            if callable(text):
                text = text()
            print(text)


