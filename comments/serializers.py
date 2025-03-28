from rest_framework import serializers
from .models import Comment,Review


class CommentSerializer(serializers.ModelSerializer):
    tag = serializers.SlugRelatedField(slug_field='name', read_only=True)
    reply_count = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields =['user',]

    def get_reply_count(self,obj):
        if obj.replies :
            return obj.replies.all().count()



class ReplyCommentSerializer(serializers.ModelSerializer):
    tag = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'chapter':{'read_only':True},
            'user': {'read_only': True},
        }



class ReviewSerializer(serializers.ModelSerializer):


    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user','book']


