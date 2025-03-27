from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from book.models import Chapter
from .serializers import CommentSerializer, ReplyCommentSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Comment
from django.shortcuts import get_object_or_404
from paginations import CustomPagination


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
            comment.dislike.remove(user)
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
            comment.like.remove(user)

        if user in comment.dislike.all():
            comment.dislike.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        comment.dislike.add(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentReplyAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, comment_id):
        reply_to_comment = get_object_or_404(Comment, pk=comment_id)
        ser_data = ReplyCommentSerializer(data=request.data)
        if ser_data.is_valid():
            if not reply_to_comment.reply:
                ser_data.save(user=request.user, reply=reply_to_comment, chapter=reply_to_comment.chapter,
                              tag=reply_to_comment.user)
            else:
                ser_data.save(user=request.user, reply=reply_to_comment.reply, chapter=reply_to_comment.chapter,
                              tag=reply_to_comment.user)
            return Response(ser_data.data, status=status.HTTP_201_CREATED)

        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)





class CommentChapterAPIView(APIView):
    def get(self, request, chapter_id):
        comments = Chapter.objects.prefetch_related('c_comments', 'c_comments__like', 'c_comments__dislike').get(
            pk=chapter_id).c_comments.all()
        paginator = CustomPagination()
        page = paginator.paginate_queryset(comments, request)
        ser_data = CommentSerializer(page, many=True)
        return paginator.get_paginated_response(ser_data.data)


class CommentGetAllReplyAPIView(APIView):
    def get(self, request, comment_id):
        comments = Comment.objects.prefetch_related('replies', 'replies__like', 'replies__dislike').get(
            pk=comment_id).replies.all()
        paginator = CustomPagination()
        page = paginator.paginate_queryset(comments, request)
        ser_data = CommentSerializer(page, many=True)
        return paginator.get_paginated_response(ser_data.data)
