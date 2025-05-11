from channels.generic.websocket import WebsocketConsumer
from .models import Message
from django.contrib.auth import get_user_model
import json


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def receive(self, text_data):
        load_data = json.loads(text_data)
        print(load_data)
        User = get_user_model()
        from_user = self.scope['user']
        to_user_id = self.scope['url_route']['kwargs']['user_id']
        to_user = User.objects.get(id=to_user_id)
        message = Message()
        message.from_user = from_user
        message.to_user = to_user
        message.message = load_data['message']
        message.save()
