from django.urls import path
from .views import *
urlpatterns = [
    path('', index, name='f1l3'),
    path('upload/', upload, name='f1l3-upload'),
    path('admin_browse/', admin_browse, name='f1l3-admin-browse'),
    path('admin_browse/<str:path>/', admin_browse),
]