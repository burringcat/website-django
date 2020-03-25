from django.urls import path, include
from .views import *
urlpatterns = [
    path('', index, name='blog-index'),
    path('<slug:blog_slug>/', blog, name='blog'),
    path('post/', include('weblog.post_urls')),
    path('topic/<slug:topic>/', topic, name='topic'),
]
