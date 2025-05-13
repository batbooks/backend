from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from book.models import Book
from .models import Favorite, Blocked, Rating
from rest_framework.response import Response
from rest_framework import status
from book.serializers import BookAllGetSerializer
from paginations import CustomPagination
from .serializers import RatingBookSerializer


class BookToggleFavoriteView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, book_id, *args, **kwargs):
        book = Book.objects.get(pk=book_id)
        favorite = Favorite.objects.filter(user=request.user)
        if favorite.exists():
            favorite = favorite.first()
            if book in favorite.book.all():
                favorite.book.remove(book)
            else:
                favorite.book.add(book)
            return Response(status=status.HTTP_204_NO_CONTENT)
        favorite = Favorite.objects.create(user=request.user)
        favorite.book.add(book)
        return Response(status=status.HTTP_201_CREATED)


class UserFavoriteView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookAllGetSerializer

    def get(self, request, *args, **kwargs):
        favorite = Favorite.objects.get(user=request.user)
        paginator = CustomPagination()
        page = paginator.paginate_queryset(favorite.book.all(), request)
        ser_date = BookAllGetSerializer(page, many=True)
        return paginator.get_paginated_response(ser_date.data)


class BookIsFavoriteView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        favorite = Favorite.objects.filter(user=request.user, book=book)
        return Response({"is_favorite": favorite.exists()}, status=status.HTTP_200_OK)


class BookToggleBlockedView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, book_id, *args, **kwargs):
        book = Book.objects.get(pk=book_id)
        blocked = Blocked.objects.filter(user=request.user)
        if blocked.exists():
            blocked = blocked.first()
            if book in blocked.book.all():
                blocked.book.remove(book)
            else:
                blocked.book.add(book)
            return Response(status=status.HTTP_204_NO_CONTENT)
        blocked = Blocked.objects.create(user=request.user)
        blocked.book.add(book)
        return Response(status=status.HTTP_201_CREATED)


class UserBlockedView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookAllGetSerializer

    def get(self, request, *args, **kwargs):
        blocked = Blocked.objects.get(user=request.user)
        paginator = CustomPagination()
        page = paginator.paginate_queryset(blocked.book.all(), request)
        ser_date = BookAllGetSerializer(page, many=True)
        return paginator.get_paginated_response(ser_date.data)


class BookRatingView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RatingBookSerializer

    def post(self, request, *args, **kwargs):
        ser_data = RatingBookSerializer(data=request.data, context={'request': request})
        if ser_data.is_valid():
            ser_data.save(user=request.user)
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
