from __future__ import unicode_literals

import django.conf
import django.conf.urls
import django.views.generic
import django.contrib.auth.urls
import django.conf
import django.conf.urls.static
import django.contrib.admin

urlpatterns = [
    django.conf.urls.url(r'^admin/', django.conf.urls.include(django.contrib.admin.site.urls)),
    django.conf.urls.url(r'^bot/', django.conf.urls.include('bot.urls')),
]
