from django.urls import path
from .views import *
urlpatterns = [
    path('bg/', random_background_image, name='random-bg'),
    path('conf/', site_config, name='conf'),
    path('admin-i2b/', image_to_blob, name='admin-i2b'),
    path('ping/', ping, name='ping'),
    # path('test_is_up/<str:url>/', test_is_up, name='test-is-up'),
    path('', utils, name='utils'),
]
