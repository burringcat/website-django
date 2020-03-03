from django.forms.widgets import Textarea
from django.conf import settings
class TextareaWithBlobImage(Textarea):
    template_name = settings.BLOG_POST_EDITOR_WIDGET