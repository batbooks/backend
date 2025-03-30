from rest_framework import serializers
from .models import UserInfo


class UserInfoSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='name', read_only=True)
    favorite_count = serializers.SerializerMethodField()
    class Meta:
        model = UserInfo
        fields = '__all__'

    def get_favorite_count(self, obj):
        return obj.user.favorite.book.count()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        hide_field = self.context.get('hide_field',[])
        for f in hide_field:
            data.pop(f, None)
        return data
