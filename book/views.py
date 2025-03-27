from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Book, Chapter
from permissions import  BookIsOwnerOrReadOnly,ChapterIsOwnerOrReadOnly
from .serializers import BookSerializer, BookGetAllSerializer, ChapterGetSerializer, ChapterCreateSerializer, \
    BookAllGetSerializer, BookGetSerializer
from paginations import CustomPagination

class BookListAPIView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookAllGetSerializer(books, many=True)
        return Response(serializer.data)
class BookCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(Author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookDetailAPIView(APIView):
    permission_classes = [BookIsOwnerOrReadOnly]
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookGetAllSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        self.check_object_permissions(request,book)
        serializer = BookSerializer(book, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class ChapterDetailUpdateDeleteAPIView(APIView):
    permission_classes = [ChapterIsOwnerOrReadOnly]
    def get(self, request, id):
        chapter = get_object_or_404(Chapter, pk=id)
        if chapter.is_approved:
            ser_data = ChapterGetSerializer(chapter)
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response({'msg':'chapter not found'},status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        chapter = get_object_or_404(Chapter, pk=id)
        self.check_object_permissions(request,chapter)
        serializer = ChapterCreateSerializer(data=request.data, instance=chapter, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        chapter = get_object_or_404(Chapter, pk=id)
        self.check_object_permissions(request,chapter)
        chapter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ChapterCreateAPIView(APIView):
    permission_classes = [BookIsOwnerOrReadOnly]
    def post(self, request):
        book = get_object_or_404(Book, pk=request.data['book'])
        self.check_object_permissions(request,book)
        ser_data = ChapterCreateSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class BookSearchAPIView(APIView):
    def get(self, request,book_name):
        book_name = book_name.strip()
        if len(book_name) < 3:
            return Response({"error": 'book name must be greater than 3 letter'}, status=status.HTTP_400_BAD_REQUEST)
        books = Book.objects.filter(name__icontains=book_name)
        paginator = CustomPagination()
        page = paginator.paginate_queryset(books, request)
        data = BookGetSerializer(page, context={"hide_field": ['email']}, many=True).data
        return paginator.get_paginated_response(data)
