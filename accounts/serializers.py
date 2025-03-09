from rest_framework import serializers
from .models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    c_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields= ['email', 'password','c_password']
        extra_kwargs = {
            'password':{'write_only':True}
        }

