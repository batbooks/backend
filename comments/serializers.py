from rest_framework import serializers
from .models import Comment,Review


class CommentSerializer(serializers.ModelSerializer):
    tag = serializers.SlugRelatedField(slug_field='name', read_only=True)
    reply_count = serializers.SerializerMethodField()
    user = serializers.SlugRelatedField(slug_field='name', read_only=True)
    image = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields =['user',]

    def get_reply_count(self,obj):
        if obj.replies :
            return obj.replies.all().count()

    def get_image(self,obj):
        if obj.user.user_info.image :
            return obj.user.user_info.image.url

class ReplyCommentSerializer(serializers.ModelSerializer):
    tag = serializers.SlugRelatedField(slug_field='name', read_only=True)
    user = serializers.SlugRelatedField(slug_field='name', read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'chapter':{'read_only':True},
            'user': {'read_only': True},
        }

    def get_image(self,obj):
        if obj.user.user_info.image :
            return obj.user.user_info.image.url

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='name', read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user','book']

    def get_image(self,obj):
        if obj.user.user_info.image :
            return obj.user.user_info.image.url
