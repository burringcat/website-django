from django.urls import path, include
from wvr_auth.views import *
github = [
    path('login/', github_auth, name='auth-github'),
    path('callback/', github_callback),
]

urlpatterns = [
    path('login/', login_page, name='auth-login'),
    path('logout/', logout, name='auth-logout'),
    path('github/', include(github)),
]

