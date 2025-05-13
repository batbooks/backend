from rest_framework.response import Response
from rest_framework.views import APIView

from book.models import Book
from book.serializers import BookSerializer
from .serializer import GenreSerializer
from tag.models import Genre
from django.db.models import Count
from user_info.serializers import UserInfoSerializer
from user_info.models import UserInfo
from rest_framework import status


class HomeCategoryView(APIView):
    def get(self, request):
        Genre_list = Genre.objects.annotate(book_count=Count('books'))[:8]
        ser_data = GenreSerializer(Genre_list, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)


class HomeSuggestionBookView(APIView):
    def get(self, request):
        books = Book.objects.order_by('?')[:5]
        ser_data = BookSerializer(books, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)


class HomeNewestBookView(APIView):
    def get(self, request):
        book = Book.objects.order_by('-created_at')[:5]
        ser_data = BookSerializer(book, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)


class HomeMostPopularAuthorsView(APIView):

    def get(self, request):
        author = UserInfo.objects.annotate(followed_count=Count('user__following')).order_by('-followed_count')[:6]
        ser_data = UserInfoSerializer(author, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)


class HomeMostActiveAuthorsView(APIView):

    def get(self, request):
        author = UserInfo.objects.annotate(books=Count('user__books')).order_by('-books')[:6]
        ser_data = UserInfoSerializer(author, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)
