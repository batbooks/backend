from rest_framework import serializers
from playlist.models import Playlist,PlaylistBook
from book.models import Book
from book.serializers import BookGetSerializer
from tag.models import Tag,Genre
from tag.serializer import TagTitleSerializer,GenreTitleSerializer


error = {'error1': 'این کتاب در پلی لیست وجود دارد.'}

class PlaylistSerializer(serializers.ModelSerializer):
    tags = TagTitleSerializer(many=True, read_only=True)
    genres = GenreTitleSerializer(many=True, read_only=True)
    book_count = serializers.SerializerMethodField()

    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, write_only=True, source='tags'
    )
    genre_ids = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), many=True, write_only=True, source='genres'
    )

    def get_book_count(self, obj):
        return PlaylistBook.objects.filter(playlist=obj).count()

    class Meta:
        model = Playlist
        fields = [
            'id', 'user', 'name', 'description',
            'tags', 'tag_ids', 'genres', 'genre_ids',
            'is_public', 'created_at','book_count'
        ]
        read_only_fields = ['id', 'created_at','user','book_count']



class PlaylistBookSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = PlaylistBook
        fields = ['id', 'playlist', 'book', 'rank']
        read_only_fields = ['id']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['book'] = BookGetSerializer(instance.book).data
        return rep


class AddBookToPlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistBook
        fields = ['book', 'rank']  # Playlist will come from the context

    def create(self, validated_data):
        # Access the playlist from the context
        playlist = self.context.get('playlist')
        book = validated_data['book']

        # Check if the book is already in the playlist
        if PlaylistBook.objects.filter(playlist=playlist, book=book).exists():
            raise serializers.ValidationError('این کتاب در پلی لیست وجود دارد.')

        # Create the PlaylistBook entry
        playlist_book = PlaylistBook.objects.create(playlist=playlist, **validated_data)

        return playlist_book