from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    language_code = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name or '' + '(' + self.language_code + ')'
    def auto_translate_to(self, to_lang_code, content):
        raise NotImplemented(f'Translate from {self.language_code} to '
                             f'{to_lang_code} is not implemented')
    @classmethod
    def get(cls, language_code='en'):
        if not language_code:
            language_code = 'en'
        return cls.objects.get_or_create(language_code=language_code)[0]
class DateTimeMixin(models.Model):
    class Meta:
        abstract = True
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
