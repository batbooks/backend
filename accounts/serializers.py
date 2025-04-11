from rest_framework import serializers

from .models import User
from user_info.serializers import UserInfoSerializer

class UserReadSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'email', 'name','user_info']

    def get_user_info(self, obj):
        user_inf = obj.user_info
        return UserInfoSerializer(user_inf).data
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        hide_field = self.context.get('hide_field',[])
        for f in hide_field:
            data.pop(f, None)
        return data

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
            raise serializers.ValidationError('گذرواژه باید حتما حداقل هشت حرف داشته باشد.')
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['c_password']:
            raise serializers.ValidationError("گذرواژه‌ها یکسان نیستند.")

        user = User.objects.filter(email=attrs['email']).first()
        if user and not user.is_active:
            user.delete()

        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.IntegerField()
    new_password = serializers.CharField(write_only=True)
    new_password_conf = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('گذرواژه باید حتما حداقل هشت حرف داشته باشد.')
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_conf']:
            raise serializers.ValidationError("گذرواژه‌ها یکسان نیستند.")

        user = User.objects.filter(email=attrs['email']).first()

        return attrs


