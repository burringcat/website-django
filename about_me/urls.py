from django.urls import path, include
from .views import *
urlpatterns = [
    path('cv/', cv, name='cv'),
    path('cv-pdf/', cv_pdf, name='cv-pdf'),
    path('me/', about_me, name='about-me'),
    path('portfolio/', portfolio, name='portfolio'),
]
