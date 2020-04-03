from collections import defaultdict
import random

from utils.utils.misc import all_subclasses

from .plugins.plugins import ChatBotPlugin

message_on_start = "Nyaaawwn~~ Hello! I'm awake :3"
message_on_unknown_command = "I'm sorry? Uhm, what did you say?"


def message_yes_or_no():
    return random.choice(('Yes.', 'No.'))

get_message = defaultdict(lambda:message_on_unknown_command)
get_message.update({
    "start": message_on_start,
    "yn": message_yes_or_no
})

enabled_plugins = {plugin.cmd: plugin for plugin in all_subclasses(ChatBotPlugin) if plugin.is_enabled and plugin.cmd}
