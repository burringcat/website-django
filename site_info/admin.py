from django.contrib import admin
from .models import SiteInfo, Country, Visitor, Quote
# Register your models here.
admin.site.register(SiteInfo)
admin.site.register(Country)
admin.site.register(Visitor)
admin.site.register(Quote)