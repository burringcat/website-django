import json
import requests
from django.conf import settings
from utils.utils.misc import gen_random_str
def check_settings():
    return settings.WVR_AUTH_GITHUB_ID and settings.WVR_AUTH_GITHUB_SECRET
def oauth_url():
    if not check_settings():
        return None
    base_url = 'https://github.com/login/oauth/authorize'
    client_id = settings.WVR_AUTH_GITHUB_ID
    client_secret = settings.WVR_AUTH_GITHUB_SECRET
    state = gen_random_str(84)
    return f'{base_url}?client_id={client_id}&state={state}', state
def access_token(code, state=None):
    if not check_settings():
        return None
    post_url = 'https://github.com/login/oauth/access_token'
    client_id = settings.WVR_AUTH_GITHUB_ID
    client_secret = settings.WVR_AUTH_GITHUB_SECRET
    post_data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
    }
    if state is not None:
        post_data['state'] = state
    http_headers = {
        'Accept': 'application/json'
    }
    resp = requests.post(post_url, data=post_data, headers=http_headers)
    access_token = json.loads(resp.text).get('access_token')
    return access_token
def user_info(token):
    auth_header = {
        'Authorization': f'token {token}'
    }
    resp = requests.get('https://api.github.com/user', headers=auth_header)
    return resp.text

