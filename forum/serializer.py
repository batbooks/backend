from rest_framework import serializers
from forum.models import Thread,Forum

class ThreadSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = Thread
        fields = ['id', 'forum', 'name', 'status','text', 'created_at','author']
        read_only_fields = ['id', 'created_at', 'author']

class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = '__all__'