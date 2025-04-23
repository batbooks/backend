from rest_framework import serializers
from tag.models import Tag,TagCategory,Genre





class TagSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source='category.id', read_only=True)

    class Meta:
        model = Tag
        fields = ['id', 'title', 'description', 'category_id']

class TagCategorySerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = TagCategory
        fields = ['id', 'title', 'description', 'tags']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'title','description']