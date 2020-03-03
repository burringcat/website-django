from django.urls import path
from .views import post, enter_password

urlpatterns = [
    path('<slug:post_slug>/', post, name='post'),
    path('<slug:post_slug>/enter_password/', enter_password, name='enter-password'),

]