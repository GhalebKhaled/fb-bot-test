import django.conf

from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView
import rest_framework.response
import rest_framework.status


class VerifyTokenView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        if request.GET.get('hub.verify_token') == django.conf.settings.FB_BOT_VERIFY_TOKEN:
            return rest_framework.response.Response(status=rest_framework.status.HTTP_200_OK,
                                                    data=int(request.GET.get('hub.challenge')),)
        return rest_framework.response.Response(status=rest_framework.status.HTTP_400_BAD_REQUEST,
                                                data="wrong validation token")
