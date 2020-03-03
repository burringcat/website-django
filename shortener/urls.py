from django.urls import path
from .views import *
urlpatterns = [
    path('shortener/', shortener, name='shortener'),
    path('shortener/<str:action>/', shortener, name='shortener-action'),
    path('links/', links, name='links'),
    path('', to, name='redirect-to'),
]
