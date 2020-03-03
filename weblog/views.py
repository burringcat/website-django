from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseNotFound
from django.core.paginator import Paginator
from .models import Blog, BlogPost, Topic
from utils.utils.passhash_tools import check_password
from utils.utils.misc import gen_page_range
from django.utils.translation import get_language
from django.conf import settings


# Create your views here.
def index(request):
    if settings.WEBLOG_URL:
        return redirect(settings.WEBLOG_URL)
    blogs = Blog.objects.all()
    if len(blogs) == 1:
        return redirect(reverse('blog', kwargs={'blog_slug': blogs[0].slug}))
    context = {'blogs': blogs}
    return render(request, 'weblog/index.html', context=context)


def blog(request, blog_slug):
    page = request.GET.get('page', request.POST.get('page', 1))
    blog = Blog.objects.filter(slug=blog_slug).first()
    posts = blog.get_visible_posts()
    paginator = Paginator(posts, 25)
    posts = paginator.get_page(page)
    if not blog:
        return HttpResponseNotFound()
    page_range = gen_page_range(posts)
    current_page = posts.number
    posts = map(lambda post: post.translated_dict_obj(get_language() or 'en'),
                posts)
    return render(request, 'weblog/blog.html', context={
        'blog': blog,
        'posts': posts,
        'page_range': page_range,
        'current_page': current_page
    })


def post(request, post_slug):
    post = BlogPost.objects.filter(is_published=True, slug=post_slug).first()
    if not post:
        return HttpResponseNotFound()
    if post.passhash is not None:
        password = request.GET.get('password', request.POST.get('password', ''))
        error = True
        if check_password(password, post.passhash) is True:
            error = False
        if error is True:
            return redirect(reverse('enter-password', kwargs={'post_slug': post_slug}))
    return render(request, 'weblog/post.html',
                  context={'post': post.translated_dict_obj(get_language() or 'en')})


def enter_password(request, post_slug):
    return render(request, 'weblog/enter_password.html',
                  context={
                      'post_slug': post_slug,
                  })


def topic(request, topic):
    page = request.GET.get('page', request.POST.get('page', 1))
    topic_obj = Topic.objects.filter(name=topic).first()
    if not topic_obj:
        return HttpResponseNotFound()
    posts = sorted(topic_obj.blog_posts.all(), key=lambda post:post.posted, reverse=True)
    paginator = Paginator(posts, 25)
    posts = paginator.get_page(page)
    page_range = gen_page_range(posts)
    current_page = posts.number
    posts = map(lambda post: post.translated_dict_obj(get_language() or 'en'),
                posts)
    context = {
        'topic': topic_obj,
        'posts': posts,
        'page_range': page_range,
        'current_page': current_page
    }
    return render(request, 'weblog/topic.html', context=context)
