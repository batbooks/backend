from django.db.models import Count
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from playlist.models import Playlist,PlaylistBook
from playlist.serializer import PlaylistSerializer,AddBookToPlaylistSerializer,PlaylistBookSerializer,PlaylistDetailSerializer
from django.shortcuts import get_object_or_404
from permissions import IsPlaylistOwnerOrReadOnly
from django.contrib.auth import get_user_model
from rest_framework import generics
from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters
from .filters import PlaylistFilter




error = {'error1': 'اجازه دیدن این پلی لیست را ندارید.'}
User = get_user_model()


class PublicPlaylistListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        playlists = Playlist.objects.filter(is_public=True)
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data)

class AnotherUserPublicPlaylistsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        playlists = Playlist.objects.filter(user=user, is_public=True)
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data)


class UserPlaylistListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        playlists = Playlist.objects.filter(user=request.user)
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data)

class PlaylistListCreateView(APIView):
    permission_classes = [IsAuthenticated,IsPlaylistOwnerOrReadOnly]

    def post(self, request):
        serializer = PlaylistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PlaylistDetailView(APIView):
    permission_classes = [IsAuthenticated,IsPlaylistOwnerOrReadOnly]
    def get_object(self, pk, user):
        return get_object_or_404(Playlist, pk=pk, user=user)

    def put(self, request, pk):
        playlist = self.get_object(pk, request.user)
        serializer = PlaylistSerializer(playlist, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        playlist = self.get_object(pk, request.user)
        playlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlaylistBookListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, playlist_id, *args, **kwargs):
        playlist = get_object_or_404(Playlist, pk=playlist_id)
        if not playlist.is_public:
            return Response({"error": error['error1']}, status=status.HTTP_403_FORBIDDEN)

        serializer = PlaylistDetailSerializer(playlist)
        return Response(serializer.data)


class AddBookToPlaylistView(APIView):
    permission_classes = [IsAuthenticated, IsPlaylistOwnerOrReadOnly]

    def post(self, request, playlist_id):
        playlist = get_object_or_404(Playlist, id=playlist_id)

        serializer = AddBookToPlaylistSerializer(data=request.data, context={'playlist': playlist})

        if serializer.is_valid():
            playlist_book = serializer.save()

            return Response(
                {"message": "Book added to playlist", "id": playlist_book.book.id},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlaylistBookDetailView(APIView):
    permission_classes = [IsAuthenticated, IsPlaylistOwnerOrReadOnly]
    def get_object(self, playlist_id, book_id):
        return get_object_or_404(PlaylistBook, playlist_id=playlist_id, book_id=book_id)
    def put(self, request, playlist_id, book_id):
        playlist_book = self.get_object(playlist_id, book_id)
        serializer = PlaylistBookSerializer(playlist_book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, playlist_id, book_id):
        playlist_book = self.get_object(playlist_id, book_id)
        playlist = playlist_book.playlist  # keep reference to the playlist
        playlist_book.delete()

        # Rerank remaining items
        remaining_books = PlaylistBook.objects.filter(playlist=playlist).order_by('rank', 'id')
        for index, item in enumerate(remaining_books, start=1):
            if item.rank != index:  # update only if rank is out of order
                item.rank = index
                item.save(update_fields=['rank'])

        return Response(status=status.HTTP_204_NO_CONTENT)



class PlaylistSearchView(generics.ListAPIView):
    queryset = Playlist.objects.annotate(
        book_count=Count('playlistbook')
    )
    serializer_class = PlaylistSerializer
    filter_backends = (filters.DjangoFilterBackend, drf_filters.SearchFilter)
    filterset_class = PlaylistFilter
    search_fields = ['name', 'description']