import os
import markdown
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import models
from django.utils.translation import get_language
from django.utils import translation
from django.conf import settings
from django.template.loader import get_template
from utils.models import Language, DateTimeMixin
from utils.utils.passhash_tools import get_passhash
from utils.utils.misc import slugify, ObjectDict

class Feedable:
    @classmethod
    def gen_html5_feed_today(cls, lang_code: str = 'en'):
        return ''
    @classmethod
    def gen_rss_feed_today(cls, lang_code: str = 'en'):
        return ''


# Create your models here.

class Topic(models.Model, Feedable):
    name = models.TextField(unique=True)


class Blog(models.Model, Feedable):
    slug = models.TextField(null=True, editable=False)
    blog_name = models.TextField()
    custom_header_image_path = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    @classmethod
    def gen_html5_feed_today(cls, lang_code='en'):
        translation.activate(lang_code)
        rendered = ''
        blogs = Blog.objects.all()
        for blog in blogs:
            new_posts = BlogPost.objects.filter(
                is_published=True,
                is_hidden=False,
                passhash=None,
                blog=blog,
                posted__gte=timezone.now().date(),
            ).all()
            new_posts = [post.translated_dict_obj(lang_code) for post in new_posts]
            template = get_template(
                os.path.join(settings.BASE_DIR,
                             'weblog/templates/weblog/blog_updates.html')
            )
            html = template.render(context={
                'new_posts': new_posts,
                'blog': blog,
            })
            rendered += html
        return rendered.strip()

    def get_visible_posts(self, translate=False):
        posts = self.blogpost_set.filter(is_hidden=False).order_by('-posted').all()
        if translate:
            posts = [post.translated_dict_obj(
                get_language() or 'en'
            ) for post in posts]
        return posts

    def __str__(self):
        return str(self.pk) + ' ' + self.blog_name


class BlogPostField(models.TextField):
    pass


class BlogPost(models.Model):
    slug = models.TextField(null=True, editable=False)
    title = models.TextField()
    posted = models.DateTimeField(default=timezone.now, editable=True, null=True)
    is_published = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True, editable=False, null=True)
    is_hidden = models.BooleanField(default=False)
    # Will be password-protected if password is not null
    password = models.TextField(null=True, blank=True)
    passhash = models.TextField(null=True, blank=True, editable=False)
    content_markdown = BlogPostField(default='')
    content_rendered = models.TextField(null=True, editable=False)
    topic = models.ManyToManyField(Topic, blank=True, related_name='blog_posts')
    blog = models.ForeignKey(Blog, on_delete=models.SET_NULL, null=True)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True)
    allow_comments = models.BooleanField(default=True)

    def __str__(self):
        return str(self.blog) + ':' + self.title

    def translated_dict_obj(self, lang_code):
        d = ObjectDict(self.__dict__)
        d['original'] = self
        if self.get_language_code() != lang_code:
            translated = self.get_translation(lang_code)
            if translated:
                d['updated'] = translated.updated
                d['posted'] = translated.posted
                if translated.content_markdown:
                    d['content_markdown'] = translated.content_markdown
                if translated.content_rendered:
                    d['content_rendered'] = translated.content_rendered
                if translated.title:
                    d['title'] = translated.title
        return d

    def get_translation(self, language_code):
        language = Language.objects.filter(language_code=language_code).first()
        return self.blogposttranslation_set.filter(language=language).first()

    def get_language_code(self):
        if self.language is None:
            return 'en'
        else:
            return self.language.language_code

class Comment(DateTimeMixin):
    class Meta:
        ordering = ["-created"]
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies')
    def __str__(self):
        return self.posted_by.username + ' says ' + self.content + ' at ' + str(self.created) + ' on ' + self.blog_post.slug


@receiver(pre_save, sender=BlogPost)
def blog_post_pre_save(sender, instance, **kwargs):
    html = markdown.markdown(instance.content_markdown, output_format='html5', extensions=['fenced_code'])
    if instance.password and instance.password != instance.passhash:
        passhash = get_passhash(instance.password)
        instance.password = passhash
        instance.passhash = passhash
    if not instance.password:
        instance.passhash = None
    instance.content_rendered = html
    if not instance.slug:
        instance.slug = slugify(instance.title)


@receiver(pre_save, sender=Blog)
def blog_pre_save(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.blog_name)


class BlogPostTranslation(models.Model):
    posted = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    title = models.TextField(null=True, blank=True)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    blog_post = models.ForeignKey(BlogPost, on_delete=models.SET_NULL, null=True)
    content_markdown = models.TextField(default='')
    content_rendered = models.TextField(null=True, editable=False)

    def get_language_code(self):
        if self.language is None:
            return 'en'
        else:
            return self.language.language_code


@receiver(pre_save, sender=BlogPostTranslation)
def render_translated(sender, instance, **kwargs):
    html = markdown.markdown(instance.content_markdown, output_format='html5', extensions=['fenced_code'])
    instance.content_rendered = html
