from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Message,GroupMessage,Group


class ShowMessageSerializer(serializers.ModelSerializer):
    from_user = serializers.SlugRelatedField(slug_field='name', read_only=True)
    to_user = serializers.SlugRelatedField(slug_field='name', read_only=True)
    to_user_id = serializers.SerializerMethodField()
    from_user_id = serializers.SerializerMethodField()

    def get_to_user_id(self, obj):
        return obj.to_user.id

    def get_from_user_id(self, obj):
        return obj.from_user.id

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('id', 'from_user', 'to_user')



User = get_user_model()

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'members']
        extra_kwargs = {
            'members': {'required': False}
        }

class GroupMessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()

    class Meta:
        model = GroupMessage
        fields = ['id', 'sender', 'message', 'date']