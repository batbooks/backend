from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from book.models import Book
from .models import Favorite
from rest_framework.response import Response
from rest_framework import status
from book.serializers import BookAllGetSerializer
from paginations import CustomPagination
class BookToggleFavoriteView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request,book_id, *args, **kwargs):
        book = Book.objects.get(pk=book_id)
        favorite = Favorite.objects.filter(user=request.user)
        if favorite.exists():
            favorite = favorite.first()
            if book in favorite.book.all() :
                favorite.book.remove(book)
            else:
                favorite.book.add(book)
            return Response(status=status.HTTP_204_NO_CONTENT)
        favorite = Favorite.objects.create(user=request.user)
        favorite.book.add(book)
        return Response(status=status.HTTP_201_CREATED)


class UserFavoriteView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        favorite = Favorite.objects.get(user=request.user)
        paginator = CustomPagination()
        page = paginator.paginate_queryset(favorite.book.all(), request)
        ser_date = BookAllGetSerializer(page,many=True)
        return paginator.get_paginated_response(ser_date.data)