from rest_framework import serializers

from .models import  Rating

class RatingBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'book', 'rating','user']
        read_only_fields = ['id','user']




