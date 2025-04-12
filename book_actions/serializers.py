from rest_framework import serializers

from .models import Favorite, Rating


class RatingBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
        read_only_fields = ('user',)

    def validate_rating(self, data):
        if data >= 0 and data <= 5:
            return data
        raise serializers.ValidationError("rating must be between 0 and 5")



