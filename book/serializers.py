from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Book, Chapter

User = get_user_model()


class BookSerializer(serializers.ModelSerializer):
    Author = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'rating', 'status', 'Author']
        read_only_fields = ['id', 'created_at', 'updated_at', 'Author']

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("The book name must be at least 3 characters long.")
        return value

    def validate_rating(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError("Rating must be between 0.0 and 5.0.")
        return value

    def validate_status(self, value):
        valid_statuses = {choice[0] for choice in Book.STATUS_CHOICE}
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Invalid status. Choose from {valid_statuses}.")
        return value


class BookAllGetSerializer(serializers.ModelSerializer):
    Author = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'rating', 'status', 'Author', ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'Author']


class BookGetSerializer(serializers.ModelSerializer):
    Author = serializers.SlugRelatedField(slug_field='name', read_only=True)
    chapters = serializers.SerializerMethodField()

    def get_chapters(self, obj):
        res = obj.chapters.all()
        return ChapterGetSerializer(instance=res, many=True).data

    class Meta:
        model = Book
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'rating', 'status', 'Author', 'chapters']
        read_only_fields = ['id', 'created_at', 'updated_at', 'Author']


class ChapterGetSerializer(serializers.ModelSerializer):
    book = serializers.SlugRelatedField(slug_field='name', read_only=True)
    Author = serializers.SerializerMethodField()

    class Meta:
        model = Chapter
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'book']

    def get_Author(self, obj):
        return obj.book.Author.name


class ChapterCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at','is_approved']
