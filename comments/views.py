from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from book.models import Chapter
from .serializers import CommentSerializer,ReplyCommentSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Comment
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination

# Create your views here.
class CommentCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        ser_data = CommentSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save(user=request.user)
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentLikeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        user = request.user
        if user in comment.dislike.all():
            return Response({"error": 'you are dislike this comment'}, status=status.HTTP_400_BAD_REQUEST)
        if user in comment.like.all():
            comment.like.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        comment.like.add(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentDisLikeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        user = request.user

        if user in comment.like.all():
            return Response({"error": 'you are like this comment'}, status=status.HTTP_400_BAD_REQUEST)

        if user in comment.dislike.all():
            comment.dislike.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        comment.dislike.add(user)
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentReplyAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request,comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        ser_data = ReplyCommentSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save(user=request.user,reply=comment,chapter=comment.chapter)
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })
class CommentChapterAPIView(APIView):
    def get(self, request, chapter_id):
        chapter = get_object_or_404(Chapter, pk=chapter_id)
        comments = Comment.objects.filter(chapter=chapter)
        paginator = CustomPagination()
        page = paginator.paginate_queryset(comments,request)
        ser_data = CommentSerializer(page, many=True)
        return paginator.get_paginated_response(ser_data.data)
