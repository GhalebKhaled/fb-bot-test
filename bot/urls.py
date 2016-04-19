import django.conf
import django.conf.urls

urlpatterns = [
            django.conf.urls.url(r'^apiv1/',  django.conf.urls.include('bot.api.urls')),
        ]
