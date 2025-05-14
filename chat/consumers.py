from channels.generic.websocket import WebsocketConsumer
from .models import Message, UserChannel
from django.contrib.auth import get_user_model
import json
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        user_channels = UserChannel.objects.filter(user=self.scope['user'])
        if user_channels.exists():
            user_channel = user_channels.first()
            user_channel.channel = self.channel_name
            user_channel.save()
        else:
            UserChannel.objects.create(user=self.scope['user'], channel=self.channel_name)

        self.to_user_id = self.scope['url_route']['kwargs']['user_id']

    def receive(self, text_data):
        load_data = json.loads(text_data)
        User = get_user_model()
        from_user = self.scope['user']
        to_user = User.objects.get(id=self.to_user_id)
        if load_data['type'] == 'new_message':
            message = Message()
            message.from_user = from_user
            message.to_user = to_user
            message.message = load_data['message']
            message.save()

            data = {
                'type': 'receiver_function',
                'type_of_data': 'new_message',
                'data': load_data.get('message'),
            }
            try:
                user_channel = UserChannel.objects.get(user=to_user)
                async_to_sync(self.channel_layer.send)(user_channel.channel, data)
            except:
                pass
        elif load_data['type'] == 'message_seen':
            user_channel = UserChannel.objects.get(user=from_user)
            data = {
                'type': 'receiver_function',
                'type_of_data': 'message_seen',
            }
            message = Message.objects.filter(from_user=to_user, to_user=from_user)
            message.update(has_been_seen=True)

            async_to_sync(self.channel_layer.send)(user_channel.channel, data)

    def receiver_function(self, data):
        load_data = json.dumps(data)
        self.send(load_data)
