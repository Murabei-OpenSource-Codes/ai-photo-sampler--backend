#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse

from core import settings

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),

    url(r'^admin/pumpwood-auth-app/gui/', admin.site.urls),
    url(r'^health-check/pumpwood-auth-app/',
        lambda r: JsonResponse(True, safe=False)),

    # Registration end-points
    url(r'^rest/', include('pumpwood_django_auth.registration.urls')),
    url(r'^rest/', include('pumpwood_django_auth.system.urls')),

    # Models
    url(r'^rest/', include('photo.urls')),
    url(r'^rest/', include('experiment.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
