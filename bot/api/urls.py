import django.conf
import django.conf.urls

import bot.api.views

urlpatterns = [
            django.conf.urls.url(r'webhook/$', bot.api.views.VerifyTokenView.as_view()),
        ]
