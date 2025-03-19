from rest_framework import serializers
from .models import UserInfo


class UserInfoSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = UserInfo
        fields = '__all__'
