import FBBot


fb_client = FBBot.FBBotClient()


class WebhookView(FBBot.FBBotWebhookView):
    def handle_message(self, message, sender_id):
        if message == "logo":
            fb_client.send_image(sender_id, "https://d2for33x7as0fp.cloudfront.net/static/images/53-logo.71a393299d20.png")
        else:
            fb_client.send_message(sender_id, "I can only repeat right now:{}".format(message))
