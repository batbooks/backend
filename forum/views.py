from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from forum.models import Thread,Forum
from forum.serializer import ThreadSerializer,ForumSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated,AllowAny
from permissions import ForumIsOwnerOrReadOnly
from paginations import CustomPagination
# Create your views here.

class ForumListAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        forums = Forum.objects.all()
        paginator = CustomPagination()
        page = paginator.paginate_queryset(forums, request)
        serializer = ForumSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class ThreadCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ThreadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForumThreadListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        forum = get_object_or_404(Forum, id=pk)
        threads = forum.threads.all()
        paginator = CustomPagination()
        page = paginator.paginate_queryset(threads, request)
        serializer = ThreadSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class ThreadUpdateAPIView(APIView):
    permission_classes = [ForumIsOwnerOrReadOnly]
    def put(self, request, pk):
        thread = get_object_or_404(Thread, pk=pk)
        serializer = ThreadSerializer(thread, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        thread = get_object_or_404(Thread, pk=pk)
        thread.delete()
        return Response({'message': 'با موفقیت حذف شد.'}, status=status.HTTP_204_NO_CONTENT)


