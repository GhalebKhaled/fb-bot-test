import requests_futures.sessions

import django.conf

from rest_framework.generics import GenericAPIView
import rest_framework.response
import rest_framework.status


# TODO : we might need to increase number of workers - I think default is 2
session = requests_futures.sessions.FuturesSession()


def send_message_callback(sess, resp):
    pass


def send_message(sender, text):
    token = django.conf.settings.FB_BOT_ACCESS_TOKEN
    messageData = {
        'text': text
    }
    session.post('https://graph.facebook.com/v2.6/me/messages?access_token={}'.format(token), json={
        'recipient': {'id': sender},
        'message': messageData,
    }, background_callback=send_message_callback)


class WebhookView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        if request.GET.get('hub.verify_token') == django.conf.settings.FB_BOT_VERIFY_TOKEN:
            return rest_framework.response.Response(status=rest_framework.status.HTTP_200_OK,
                                                    data=int(request.GET.get('hub.challenge')),)
        return rest_framework.response.Response(status=rest_framework.status.HTTP_400_BAD_REQUEST,
                                                data="wrong validation token")

    def post(self, request, *args, **kwargs):
        if request.data and request.data['entry']:
            for entry in request.data['entry']:
                print "_-_-_-_-_"
                print entry
                print type(entry)
                print "_-_-_-_-_"
                for msging in entry['messaging']:
                    print "_-_-_-_-_"
                    print msging
                    print type(msging)
                    print "_-_-_-_-_"
                    for msg in msging:
                        print msg
                        print type(msg)
                        message = msg['message']['text']
                        sender_id = msg['sender']['1249712545046598']
                        send_message(sender_id, "I can only repeat right now:{}".format(message))

        return rest_framework.response.Response(status=rest_framework.status.HTTP_200_OK)
