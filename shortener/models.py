from base64 import b16encode
from posix import urandom
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings
from .utils import decimal2encoded, encoded2decimal
# Create your models here.

class URL(models.Model):
    AccessOptions = (
        (0, _("Everyone Can Access")),
        (1, _("Need Login")),
        (2, _("Creator Only")),
        (3, _("Superusers Only")),
    )
    url = models.TextField()
    notes = models.TextField(null=True, blank=True)
    is_public_listed = models.BooleanField(default=False)
    access_option = models.IntegerField(choices=AccessOptions, default=0)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    encrypted_id = models.TextField(null=True, blank=True)

    def encrypt(self):
        b = urandom(384)
        k = b16encode(b)
        self.encrypted_id = str(k, encoding='utf8').lower()
        self.save()

    @property
    def is_encrypted(self):
        return self.encrypted_id and len(self.encrypted_id) > 128

    @property
    def unique_id(self):
        return self.encoded_pk if not self.is_encrypted else \
            settings.SHORTENER_URL_ENCRYPT_PREFIX + self.encrypted_id

    @classmethod
    def get_url_by_unique_id(cls, uid):
        if not uid.startswith(settings.SHORTENER_URL_ENCRYPT_PREFIX):
            url = URL.get_url(uid)
            if url.is_encrypted:
                url = None
        else:
            euid = uid[len(settings.SHORTENER_URL_ENCRYPT_PREFIX):]
            url = URL.get_encrypted(euid)
        return url
    def can_access(self, user):
        if self.access_option == 0:
            return True
        if self.access_option == 1:
            return not user.is_anonymous
        if self.access_option == 2:
            return not user.is_anonymous and user == self.creator
        if self.access_option == 3:
            return user.is_superuser
    @classmethod
    def get_encrypted(cls, euid):
        return cls.objects.filter(encrypted_id=euid).first()
    @classmethod
    def get_url(cls, encoded):
        return cls.objects.filter(pk=encoded2decimal(encoded)).first()
    @property
    def title(self):
        return self.notes or self.url
    @property
    def encoded_pk(self):
        return decimal2encoded(self.pk)

    @classmethod
    def decode_pk(cls, encoded):
        return encoded2decimal(encoded)

    @classmethod
    def get_public(cls):
        return cls.objects.filter(is_public_listed=True).all()