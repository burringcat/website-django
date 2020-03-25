"""wvr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from django.conf.urls.static import static


urlpatterns = [
    path(settings.ADMIN_URL + '/', admin.site.urls),
    path('', include('landing_page.urls')),
    path('blog/', include('weblog.urls')),
    path('utils/', include('utils.urls')),
    path('site/', include('site_info.urls')),
    path('about/', include('about_me.urls')),
    path('go/', include('shortener.urls')),
    path('f1l3/', include('f1l3.urls')),
    path('auth/', include('wvr_auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
