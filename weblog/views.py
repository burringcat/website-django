from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.core.paginator import Paginator
from .models import Blog, BlogPost, Topic, Comment
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

@login_required
def add_comment(request, post_slug):
    post = BlogPost.objects.filter(is_published=True, slug=post_slug).first()
    if not post:
        return HttpResponseNotFound('404 post not found')
    redirect_resp = redirect(reverse('post', kwargs={'post_slug': post.slug}))
    content = request.POST.get('content', '').strip()
    if not content:
        return redirect_resp
    parent_comment_id = request.POST.get('parent_comment_id')
    if parent_comment_id is None:
        parent_comment = None
    else:
        try:
            parent_comment_id = int(parent_comment_id)
        except:
            return HttpResponseBadRequest('400 bad parent comment id')
        parent_comment = Comment.objects.filter(pk=parent_comment_id).first()
        if parent_comment is None:
            return HttpResponseNotFound('404 parent comment not found')
    Comment.objects.create(content=content, posted_by=request.user, blog_post=post, parent_comment=parent_comment)
    return redirect_resp

@login_required
def reply_page(request, post_slug, parent_comment_id):
    comment = Comment.objects.filter(pk=parent_comment_id).first()
    post = BlogPost.objects.filter(slug=post_slug).first()
    if comment is None or post is None:
        return redirect(reverse('post', kwargs={'post_slug': post.slug}))
    return render(request, 'weblog/reply.html', {'post': post, 'comment': comment})

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
