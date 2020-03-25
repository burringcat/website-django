from django.urls import path
from .views import post, enter_password, add_comment, reply_page

urlpatterns = [
    path('<slug:post_slug>/', post, name='post'),
    path('<slug:post_slug>/enter_password/', enter_password, name='enter-password'),
    path('<slug:post_slug>/add_comment/', add_comment, name='add-comment'),
    path('<slug:post_slug>/reply/<int:parent_comment_id>/', reply_page, name='add-comment-reply-page')
]
