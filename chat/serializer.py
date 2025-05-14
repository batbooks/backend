from rest_framework import serializers

from .models import Message


class ShowMessageSerializer(serializers.ModelSerializer):
    from_user = serializers.SlugRelatedField(slug_field='name', read_only=True)
    to_user = serializers.SlugRelatedField(slug_field='name', read_only=True)
    to_user_id = serializers.SerializerMethodField()
    from_user_id = serializers.SerializerMethodField()

    def get_to_user_id(self, obj):
        return obj.to_user.id

    def get_from_user_id(self, obj):
        return obj.from_user.id

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('id', 'from_user', 'to_user')
