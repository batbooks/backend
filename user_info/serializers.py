from rest_framework import serializers
from .models import UserInfo, UserFollow, UserNotInterested


class UserInfoSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='name', read_only=True)
    user_id = serializers.SerializerMethodField()
    favorite_count = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    joined_date = serializers.SerializerMethodField()
    book_count = serializers.SerializerMethodField()

    def get_user_id(self, obj):
        return obj.user.id

    def get_book_count(self, obj):
        return obj.user.books.count()

    class Meta:
        model = UserInfo
        fields = '__all__'

    def get_favorite_count(self, obj):
        return obj.user.favorite.book.count()

    def get_follower_count(self, obj):
        return obj.user.following.count()

    def get_joined_date(self, obj):
        return obj.user.joined_date

    def get_following_count(self, obj):
        return obj.user.follower.count()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        hide_field = self.context.get('hide_field', [])
        for f in hide_field:
            data.pop(f, None)
        return data


class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.SlugRelatedField(slug_field='name', read_only=True)
    following = serializers.SlugRelatedField(slug_field='name', read_only=True)
    follower_image = serializers.SerializerMethodField()
    following_image = serializers.SerializerMethodField()
    follower_user_id = serializers.SerializerMethodField()
    following_user_id = serializers.SerializerMethodField()

    def get_follower_user_id(self, obj):
        return obj.follower.id

    def get_following_user_id(self, obj):
        return obj.following.id

    def get_follower_image(self, obj):
        return obj.follower.user_info.image.url if obj.follower.user_info.image else None

    def get_following_image(self, obj):
        return obj.following.user_info.image.url if obj.following.user_info.image else None

    class Meta:
        model = UserFollow
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        hidden_field = self.context.get('hide_field', [])
        for f in hidden_field:
            data.pop(f, None)
        return data


class NotInterestedSerializer(serializers.ModelSerializer):
    not_interested = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    class Meta:
        model = UserNotInterested
        fields = ['not_interested', 'created_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        hidden_fields = self.context.get('hide_field', [])
        for field in hidden_fields:
            data.pop(field, None)
        return data


class UsernameUpdateSerializer(serializers.Serializer):
    name = serializers.CharField()

class EmptySerializer(serializers.Serializer):
    pass

class IsFollowUserSerializer(serializers.Serializer):
    is_follow = serializers.BooleanField(read_only=True)

class IsNotinterestedUserSerializer(serializers.Serializer):
    is_not_interested = serializers.BooleanField(read_only=True)