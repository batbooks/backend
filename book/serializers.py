from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Book, Chapter,UserBookProgress
from rest_framework.reverse import reverse
from django.db.models import Avg

User = get_user_model()


class BookSerializer(serializers.ModelSerializer):
    chapter_count = serializers.SerializerMethodField()
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

    forum_link = serializers.SerializerMethodField()
    Author = serializers.SlugRelatedField(slug_field='name', read_only=True)
    rating = serializers.SerializerMethodField()

    def get_chapter_count(self, obj):
        if obj.chapters:
            return obj.chapters.count()
        return 0

    def get_rating(self, obj):
        rating = obj.rating_avg

        return str(rating) if rating else '0'

    def get_forum_link(self, obj):
        if hasattr(obj, 'forum'):
            request = self.context.get('request')
            return reverse('api_threads_of_forum', kwargs={'pk': obj.forum.pk}, request=request)
        return None

    class Meta:
        model = Book
        fields = ['id', 'chapter_count', 'name', 'description', 'created_at', 'updated_at', 'rating', 'status',
                  'Author', 'image', 'genres', 'tags', 'forum_link']
        read_only_fields = ['id', 'created_at', 'updated_at', 'Author', 'forum_link']

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError({'error': "نام کتاب باید دست‌کم ۳ حرف داشته باشد."})
        return value

    def validate_rating(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError({'error': "لطفاً عددی بین ۰ تا ۵ برای امتیاز وارد کن :)"})
        return value


class BookAllGetSerializer(serializers.ModelSerializer):
    Author = serializers.SlugRelatedField(slug_field='name', read_only=True)
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        rating = obj.rating_avg

        return str(rating) if rating else '0'

    class Meta:
        model = Book
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'rating', 'status', 'Author', 'image']
        read_only_fields = ['id', 'created_at', 'updated_at', 'Author']


class BookGetAllSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        rating = obj.rating_avg

        return str(rating) if rating else '0'

    forum_link = serializers.SerializerMethodField()

    def get_forum_link(self, obj):
        if hasattr(obj, 'forum'):
            request = self.context.get('request')
            return reverse('api_threads_of_forum', kwargs={'pk': obj.forum.pk}, request=request)
        return None

    Author = serializers.SlugRelatedField(slug_field='name', read_only=True)
    chapters = serializers.SerializerMethodField()
    genres = serializers.StringRelatedField(many=True)
    tags = serializers.StringRelatedField(many=True)

    def get_chapters(self, obj):
        res = obj.chapters.filter(is_approved=True).order_by('chapter_num')
        return ChapterSummarySerializer(instance=res, many=True).data

    class Meta:
        model = Book
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'rating', 'status', 'Author', 'chapters',
                  'image', 'genres', 'tags', 'forum_link']
        read_only_fields = ['id', 'created_at', 'updated_at', 'Author', 'forum_link']


class BookGetSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        rating = obj.rating_avg

        return str(rating) if rating else '0'

    Author = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'rating', 'status', 'Author', 'image']
        read_only_fields = ['id', 'created_at', 'updated_at', 'Author']


class ChapterGetSerializer(serializers.ModelSerializer):
    book = serializers.SlugRelatedField(slug_field='name', read_only=True)
    Author = serializers.SerializerMethodField()
    book_image = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    next_chapter = serializers.SerializerMethodField()
    previous_chapter = serializers.SerializerMethodField()

    def get_rating(self, obj):
        return obj.book.rating_avg

    def get_book_image(self, obj):
        return obj.book.image.url if obj.book.image else None

    def get_next_chapter(self, obj):
        next_chapter = Chapter.objects.filter(
            book=obj.book,
            chapter_num__gt=obj.chapter_num
        ).order_by('chapter_num').first()
        if next_chapter:
            return next_chapter.id
        return None

    def get_previous_chapter(self, obj):
        previous_chapter = Chapter.objects.filter(
            book=obj.book,
            chapter_num__lt=obj.chapter_num
        ).order_by('-chapter_num').first()
        if previous_chapter:
            return previous_chapter.id
        return None

    def get_Author(self, obj):
        return obj.book.Author.name

    class Meta:
        model = Chapter
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'book', 'book_image']


class ChapterSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        exclude = ['body', 'book']
        read_only_fields = ['id', 'created_at', 'updated_at', ]


class ChapterCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_approved']




class UserBookProgressSerializer(serializers.ModelSerializer):
    book_name = serializers.CharField(source='book.name', read_only=True)
    book_image = serializers.ImageField(source='book.image', read_only=True)
    chapter_title = serializers.CharField(source='last_read_chapter.title', read_only=True)

    class Meta:
        model = UserBookProgress
        fields = [
            'id',
            'user',
            'book',
            'book_name',
            'book_image',
            'last_read_chapter',
            'chapter_title',
            'status',
            'updated_at',
        ]
        read_only_fields = ['id', 'updated_at', 'user']

    def validate(self, data):
        book = data.get('book') or getattr(self.instance, 'book', None)
        chapter = data.get('last_read_chapter') or getattr(self.instance, 'last_read_chapter', None)

        if chapter and book and chapter.book_id != book.id:
            raise serializers.ValidationError({
                "last_read_chapter": "This chapter does not belong to the selected book."
            })

        return data




