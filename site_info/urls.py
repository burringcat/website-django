from django.urls import path
from .views import *
urlpatterns = [
    # path('newsletters/', newsletters, name='newsletters'),
    path('stats/', stats, name='stats'),
]