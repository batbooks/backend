from rest_framework import serializers

class GenreSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=256)
    description = serializers.CharField(max_length=1024, required=False)
    book_count = serializers.IntegerField(default=0)

