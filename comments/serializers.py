from rest_framework import serializers
from .models import Comment,Review,Post
from rest_framework.exceptions import ValidationError


class CommentSerializer(serializers.ModelSerializer):
    tag = serializers.SlugRelatedField(slug_field='name', read_only=True)
    reply_count = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    tag_id = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['user']

    def get_tag_id(self, obj):
        return obj.tag.id if obj.tag else 0

    def get_reply_count(self, obj):
        # Use prefetched replies if available
        if hasattr(obj, 'replies') and isinstance(obj.replies, list):
            return len(obj.replies)
        return obj.replies.count()

    def get_image(self, obj):
        if obj.user.user_info.image :
            return obj.user.user_info.image.url

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "name": obj.user.name
        }



class ReplyCommentSerializer(serializers.ModelSerializer):
    tag = serializers.SlugRelatedField(slug_field='name', read_only=True)
    user = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()


    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'chapter':{'read_only':True},
            'user': {'read_only': True},
            'tag_id': {'read_only': True},
        }

    def get_image(self, obj):
        if obj.user.user_info.image :
            return obj.user.user_info.image.url

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "name": obj.user.name
        }

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    chapter_name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user','book']

    def get_image(self, obj):
        if obj.user.user_info.image :
            return obj.user.user_info.image.url

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "name": obj.user.name
        }
    def get_chapter_name(self, obj):
        return obj.chapter.title if obj.chapter else None
class PostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['user', 'thread']

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "name": obj.user.name
        }