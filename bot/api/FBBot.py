import requests_futures.sessions

import django.conf

from rest_framework.generics import GenericAPIView
import rest_framework.response
import rest_framework.status


# TODO : we might need to increase number of workers - I think default is 2
session = requests_futures.sessions.FuturesSession()


class FBBotClient(object):
    def __init__(self, fb_token=None, request_callback=None):
        self.fb_token = fb_token or django.conf.settings.FB_BOT_ACCESS_TOKEN
        self.request_callback = request_callback

    def send_message_callback(self, sess, resp):
        if self.request_callback:
            self.request_callback(resp)

    def send(self, to, message_data):
         session.post('https://graph.facebook.com/v2.6/me/messages?access_token={}'.format(self.fb_token), json={
            'recipient': {'id': to},
            'message': message_data,
        }, background_callback=self.send_message_callback)

    def send_image(self, to, img_url):
        self.send(to, {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": img_url,
                }
            }
        })

    def send_message(self, sender, text):
        self.send(sender, {
            'text': text
        })


class FBBotWebhookView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        if request.GET.get('hub.verify_token') == django.conf.settings.FB_BOT_VERIFY_TOKEN:
            return rest_framework.response.Response(status=rest_framework.status.HTTP_200_OK,
                                                    data=int(request.GET.get('hub.challenge')),)
        return rest_framework.response.Response(status=rest_framework.status.HTTP_400_BAD_REQUEST,
                                                data="wrong validation token")

    def post(self, request, *args, **kwargs):
        if request.data and request.data['entry']:
            for entry in request.data['entry']:
                for msg in entry['messaging']:
                    if 'message' in msg:
                        message = msg['message']['text']
                        sender_id = msg['sender']['id']
                        self.handle_message(message, sender_id)
                    # Else: seems like facebook send ack, just skep them for now

        return rest_framework.response.Response(status=rest_framework.status.HTTP_200_OK)
