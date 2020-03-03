import json
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout as auth_logout
from utils.backends import auth_github
# Create your views here.
def github_auth(request):
    return redirect(auth_github.oauth_url()[0])

def github_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    if not code:
        return redirect('/')
    token = auth_github.access_token(code, state)
    user_info = auth_github.user_info(token)
    user_info = json.loads(user_info)
    email = user_info.get('email', '')
    gh_login = user_info.get('login')
    gh_id = user_info.get('id')
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = User.objects.get_or_create(username=f'github_{gh_login}_{gh_id}', email=email)[0]
        user.set_unusable_password()
        user.save()
    login(request, user)
    return redirect('/')
def logout(request):
    auth_logout(request)
    return redirect('/')
def login_page(request):
    return redirect(reverse('auth-github'))
