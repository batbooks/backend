from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Message, GroupMessage, Group


class ShowMessageSerializer(serializers.ModelSerializer):
    from_user = serializers.SlugRelatedField(slug_field='name', read_only=True)
    to_user = serializers.SlugRelatedField(slug_field='name', read_only=True)
    to_user_id = serializers.SerializerMethodField()
    from_user_id = serializers.SerializerMethodField()
    is_you = serializers.SerializerMethodField()

    def get_is_you(self, obj):
        req_user = self.context.get('request').user
        return req_user.id == obj.from_user.id

    def get_to_user_id(self, obj):
        return obj.to_user.id

    def get_from_user_id(self, obj):
        return obj.from_user.id

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('id', 'from_user', 'to_user')


class DirectMessageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    image = serializers.CharField(read_only=True)
    last_message = serializers.CharField(read_only=True)
    unread_count = serializers.IntegerField(read_only=True)


User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    is_last_you = serializers.SerializerMethodField()
    member_count = serializers.SerializerMethodField()

    def get_member_count(self, obj):
        return obj.members.count()

    def get_is_last_you(self, obj):
        req_user = self.context.get('request').user
        last_msg = obj.messages.all().order_by('-date').first()
        if not last_msg:
            return True
        msg_user = last_msg.sender
        return req_user == msg_user

    def get_last_message(self, obj):
        last_msg = obj.messages.all().order_by('-date').first()
        return last_msg.message if last_msg else None

    class Meta:
        model = Group
        fields = ['id', 'name', 'members', 'last_message', 'is_last_you', 'image', 'member_count']
        read_only_fields = ('members',)


class GroupMessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()

    class Meta:
        model = GroupMessage
        fields = ['id', 'sender', 'message', 'date']
