import datetime
import time
import random

from django.utils import timezone
from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class SiteInfo(models.Model):
    name = models.TextField(null=False, default='unnamed', unique=True)
    value = models.TextField(null=True)
    def __str__(self):
        return self.name + '=' + str(self.value)
    @classmethod
    def get(cls, name: str):
        return cls.objects.get_or_create(name=name)[0]

    @classmethod
    def should_clear_old_visitor_data(cls) -> bool:
        if settings.SITE_INFO_CLEAR_OLD_VISITOR_DATA is False:
            return False
        last_cleared = cls.get('old_visitor_data_cleared').value
        if last_cleared is None or time.time() - float(last_cleared) >= 24 * 60 * 60:
            return True
        else:
            return False


    @classmethod
    def newsletter_issue_number(cls, inc=True):
        num, is_created = cls.objects.get_or_create(
            name='newsletter_issue_number'
        )
        if is_created:
            num.value = 1 if not inc else 2
            num.save()
            return 1
        else:
            issue_num = int(num.value)
            if inc:
                num.value = issue_num + 1
                num.save()
            return issue_num
class Country(models.Model):
    name = models.CharField(max_length=100, null=True)
    code = models.CharField(max_length=20, null=True)
    def __str__(self):
        return str(self.name)
    @property
    def visitors_today_count(self):
        return self.visitor_set.filter(visit_date=timezone.now()).count()
    @property
    def real_visitors_today_count(self):
        return self.visitor_set.filter(visit_date=timezone.now(), is_bot=False).count()


class Visitor(models.Model):
    country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)
    visit_date = models.DateField(default=timezone.now)
    ip = models.TextField(null=True, unique_for_date='visit_date')
    is_bot = models.BooleanField(default=False)
    def __str__(self):
        return str(self.visit_date) + ' ' + str(self.ip) + ' ' + str(self.country.name)
    @classmethod
    def create(cls, country_code, ip, country_name=None, is_bot=False):
        obj = cls.objects.create(ip=ip, is_bot=is_bot)
        country, is_created = Country.objects.get_or_create(code=country_code)
        if is_created:
            if country_name is None:
                raise ValueError('need country name')
            country.name = country_name
            country.save()
        obj.country = country
        obj.save()
    @classmethod
    def today_total(cls):
        return cls.objects.filter(visit_date=timezone.now()).count()


@receiver(post_save, sender=Visitor)
def clear_old_visitors(sender, instance, **kwargs):
    if SiteInfo.should_clear_old_visitor_data():
        d = timezone.now().date()
        dt_now = datetime.datetime(d.year, d.month, d.day)
        old_visitors = Visitor.objects.filter(visit_date__lt=dt_now)
        if old_visitors.exists():
            old_visitors._raw_delete(old_visitors.db)
        cleared = SiteInfo.get('old_visitor_data_cleared')
        cleared.value = time.time()
        cleared.save()


class Quote(models.Model):
    content = models.TextField()
    by = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.content) + ' - ' + str(self.by)

    @classmethod
    def random_quote(cls):
        quotes_count = cls.objects.count()
        if quotes_count == 0:
            return None
        pk = random.choice(range(quotes_count)) + 1
        return cls.objects.get(pk=pk)