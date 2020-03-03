from django.contrib import admin
from utils.widgets import TextareaWithBlobImage
from .models import *
admin.site.register(Blog)
class BlogPostAdmin(admin.ModelAdmin):
    formfield_overrides = {
        BlogPostField: {'widget': TextareaWithBlobImage }
    }
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(BlogPostTranslation)
admin.site.register(Topic)

# Register your models here.
