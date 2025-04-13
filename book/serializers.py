from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Book, Chapter

User = get_user_model()


class BookSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(
        choices=Book.STATUS_CHOICE,
        error_messages={
            "invalid_choice": (
                f"وضعیتی که انتخاب کردی درست نیست. "
                f"از بین گزینه‌های مجاز یکی رو انتخاب کن: "
                f"{', '.join([choice[1] for choice in Book.STATUS_CHOICE])}."
            )
        }
    )


    Author = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'rating', 'status', 'Author','image','genres','tags']
        read_only_fields = ['id', 'created_at', 'updated_at', 'Author']

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError({'error': "نام کتاب باید دست‌کم ۳ حرف داشته باشد."})
        return value

    def validate_rating(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError({'error': "لطفاً عددی بین ۰ تا ۵ برای امتیاز وارد کن :)"} )
        return value



class BookAllGetSerializer(serializers.ModelSerializer):
    Author = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'rating', 'status', 'Author', 'image']
        read_only_fields = ['id', 'created_at', 'updated_at', 'Author']


class BookGetAllSerializer(serializers.ModelSerializer):
    Author = serializers.SlugRelatedField(slug_field='name', read_only=True)
    chapters = serializers.SerializerMethodField()
    genres = serializers.StringRelatedField(many=True)
    tags = serializers.StringRelatedField(many=True)

    def get_chapters(self, obj):
        res = obj.chapters.all()
        return ChapterGetSerializer(instance=res, many=True).data

    class Meta:
        model = Book
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'rating', 'status', 'Author', 'chapters','image','genres','tags']
        read_only_fields = ['id', 'created_at', 'updated_at', 'Author']


class BookGetSerializer(serializers.ModelSerializer):
    Author = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'rating', 'status', 'Author','image']
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
