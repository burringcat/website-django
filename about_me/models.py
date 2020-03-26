from urllib.parse import urljoin
from django.conf import settings
from django.db import models

from utils.models import DateTimeMixin
from weblog.models import BlogPostField
# Create your models here.
class PortfolioProject(DateTimeMixin):
    cover_static_url = models.TextField()
    category = models.TextField()
    article = BlogPostField()

    @property
    def cover_url(self):
        return urljoin(settings.STATIC_URL, self.cover_static_url)

