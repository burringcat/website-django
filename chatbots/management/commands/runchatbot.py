from django.core.management.base import BaseCommand

from utils.utils.misc import all_subclasses

from chatbots.backends.common import RunableBot
class Command(BaseCommand):
    help = 'Runs some chatbot or all chatbots'
    def add_arguments(self, parser):
        parser.add_argument('bot_type', type=str)

    def handle(self, *args, **options):
        self.runable_bots = all_subclasses(RunableBot)
        msg = self.style.SUCCESS(f'Successfully started {options["bot_type"]} bot') if self.run_bot(options['bot_type']) else f"Failed to run {options['bot_type']} bot"
        self.stdout.write(msg)
    def run_bot(self, bot_type: str) -> bool:
        """
        Returns True on success and False on faliure
        """
        if not bot_type:
            return False
        for b in self.runable_bots:
            if b.bot_type == bot_type:
                b().run()
                return True
        return False


