from rest_framework import serializers
from .models import UserInfo, UserFollow


class UserInfoSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='name', read_only=True)
    favorite_count = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    class Meta:
        model = UserInfo
        fields = '__all__'

    def get_favorite_count(self, obj):
        return obj.user.favorite.book.count()

    def get_follower_count(self, obj):
        return obj.user.following.count()

    def get_following_count(self, obj):
        return obj.user.follower.count()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        hide_field = self.context.get('hide_field',[])
        for f in hide_field:
            data.pop(f, None)
        return data



class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.SlugRelatedField(slug_field='name', read_only=True)
    following = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = UserFollow
        fields = '__all__'


    def to_representation(self, instance):
        data = super().to_representation(instance)
        hidden_field = self.context.get('hide_field',[])
        for f in hidden_field:
            data.pop(f, None)
        return data