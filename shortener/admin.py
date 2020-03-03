from django.contrib import admin
from .models import URL
# Register your models here.
class URLAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'url', 'encoded_pk'
    )
admin.site.register(URL, URLAdmin)
