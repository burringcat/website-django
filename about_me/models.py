from urllib.parse import urljoin
import markdown

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from utils.models import DateTimeMixin
from weblog.models import BlogPost

# Create your models here.
class PortfolioProject(DateTimeMixin):
    title = models.TextField(null=True, blank=True)
    cover_static_url = models.TextField(default='images/portfolio_default_cover.jpg', blank=True)
    category = models.TextField(blank=True, null=True)
    description_markdown = models.TextField(blank=True, null=True)
    description_rendered = models.TextField(editable=False, blank=True, null=True)
    article = models.ForeignKey(BlogPost, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def cover_url(self):
        return urljoin(settings.STATIC_URL, self.cover_static_url)

@receiver(pre_save, sender=PortfolioProject)
def portfolio_project_pre_save(sender, instance, **kwargs):
    description_rendered = markdown.markdown(instance.description_markdown, output_format='html5', extensions=['fenced_code'])
    instance.description_rendered = description_rendered

