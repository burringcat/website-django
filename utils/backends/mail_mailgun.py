from django.core.mail.backends.base import BaseEmailBackend
class MailgunMailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        raise NotImplemented