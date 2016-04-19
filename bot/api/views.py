import requests_futures.sessions

import django.conf

from rest_framework.generics import GenericAPIView
import rest_framework.response
import rest_framework.status


# TODO : we might need to increase number of workers - I think default is 2
session = requests_futures.sessions.FuturesSession()
fb_token = django.conf.settings.FB_BOT_ACCESS_TOKEN


def send_message_callback(sess, resp):
    pass


def send(to, message_data):
     session.post('https://graph.facebook.com/v2.6/me/messages?access_token={}'.format(fb_token), json={
        'recipient': {'id': to},
        'message': message_data,
    }, background_callback=send_message_callback)


def send_image(to, img_url):
    send(to, {
        "attachment": {
            "type": "image",
            "payload": {
                "url": img_url,
            }
        }
    })

    
def send_message(sender, text):
    send(sender, {
        'text': text
    })



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
                for msg in entry['messaging']:
                    if 'message' in msg:
                        message = msg['message']['text']
                        sender_id = msg['sender']['id']
                        if message == "logo":
                            send_image(sender_id, "https://d2for33x7as0fp.cloudfront.net/static/images/53-logo.71a393299d20.png")
                        else:
                            send_message(sender_id, "I can only repeat right now:{}".format(message))
                    # Else: seems like facebook send ack, just skep them for now

        return rest_framework.response.Response(status=rest_framework.status.HTTP_200_OK)
