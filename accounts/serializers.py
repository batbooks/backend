from rest_framework import serializers
from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    c_password = serializers.CharField(write_only=True)

    class Meta:

        model = User
        fields = ['email', 'password', 'c_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters')

    def validate(self, attrs):
        if attrs['password'] != attrs['c_password']:
            raise serializers.ValidationError("Passwords do not match")

        user = User.objects.filter(email=attrs['email']).first()
        if user and not user.is_active:
            user.delete()

        return attrs
