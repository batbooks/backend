from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from forum.models import Thread,Forum
from forum.serializer import ThreadSerializer,ForumSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated,AllowAny
from permissions import ForumIsOwnerOrReadOnly

# Create your views here.

class ForumListAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        forums = Forum.objects.all()
        serializer = ForumSerializer(forums, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        serializer = ThreadSerializer(threads, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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


