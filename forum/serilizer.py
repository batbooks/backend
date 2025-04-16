from rest_framework import serializers
from forum.models import Thread

class ThreadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Thread
        fields = ['id', 'forum', 'name', 'status', 'created_at','author']
        read_only_fields = ['id', 'created_at', 'author']