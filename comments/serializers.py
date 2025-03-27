from rest_framework import serializers
from book.models import Chapter
from .models import Comment,Review


class CommentSerializer(serializers.ModelSerializer):
    tag = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields =['is_approved','user']



class ReplyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'chapter':{'read_only':True},
        }


class ReviewSerializer(serializers.ModelSerializer):

    last_read_chapter = serializers.PrimaryKeyRelatedField(queryset=Chapter.objects.all(), allow_null=True, required=False)
    class Meta:
        model = Review
        fields = ['id', 'user', 'book', 'rating', 'body', 'created']
        read_only_fields = ['user','book']
