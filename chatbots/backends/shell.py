import sys
from .core import *
from .common import RunableBot
class ShellBot(RunableBot):
    bot_type = 'shell'
    def run(self):
        prompt = ">>> "
        print(message_on_start)
        while True:
            user_input = input(prompt).split()
            cmd = user_input[0]
            if cmd in enabled_plugins.keys():
                plugin = enabled_plugins[cmd]
                if len(user_input[1:]) < plugin.args:
                    print("insufficient arguments")
                    continue
                text = plugin.get_message(*user_input[1:])
            else:
                text = get_message[cmd]
                if callable(text):
                    text = text()
            print(text)


