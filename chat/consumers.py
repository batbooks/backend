from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from .models import Message, UserChannel, GroupMessage, Group
from django.contrib.auth import get_user_model
import json
from django.contrib.auth.models import AnonymousUser
from asgiref.sync import async_to_sync, sync_to_async


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        if isinstance(self.scope['user'], AnonymousUser):
            self.close()
            return

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
            user_channel = UserChannel.objects.filter(user=to_user).first()
            if user_channel:
                async_to_sync(self.channel_layer.send)(user_channel.channel, data)
        elif load_data['type'] == 'message_seen':
            user_channel = UserChannel.objects.filter(user=from_user).first()

            data = {
                'type': 'receiver_function',
                'type_of_data': 'message_seen',
            }

            message = Message.objects.filter(from_user=to_user, to_user=from_user)
            message.update(has_been_seen=True)
            if user_channel:
                async_to_sync(self.channel_layer.send)(user_channel.channel, data)

    def receiver_function(self, data):
        load_data = json.dumps(data)
        self.send(load_data)


class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.group_name = f"group_{self.group_id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
        if isinstance(self.scope['user'], AnonymousUser):
            await self.close()
            return

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        user = self.scope['user']
        message_text = data['message']

        group = await sync_to_async(Group.objects.get)(id=self.group_id)
        await sync_to_async(GroupMessage.objects.create)(
            group=group, sender=user, message=message_text
        )

        user_info = await sync_to_async(lambda: user.user_info)()
        await  self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'group_message',
                'message': message_text,
                'sender': user.name,
                'image': user_info.image.url if user_info.image else None,
                'user_id': user.id,
            }
        )

    async def group_message(self, event):
        load_data = json.dumps(event)
        await self.send(load_data)
