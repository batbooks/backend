from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from book.models import Chapter, Book
from book_actions.models import Rating
from .serializers import CommentSerializer, ReplyCommentSerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Comment, Review
from django.shortcuts import get_object_or_404
from paginations import CustomPagination
from django.db.models import Case, When, Value, IntegerField
from book_actions.serializers import RatingBookSerializer

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
        comments = get_object_or_404(
            Chapter.objects.prefetch_related('ch_comments_comment', 'ch_comments_comment__like',
                                             'ch_comments_comment__dislike'),
            pk=chapter_id).ch_comments_comment.filter(reply__isnull=True)
        paginator = CustomPagination()
        page = paginator.paginate_queryset(comments, request)
        ser_data = CommentSerializer(page, many=True)
        return paginator.get_paginated_response(ser_data.data)


class CommentGetAllReplyAPIView(APIView):
    def get(self, request, comment_id):
        comments = get_object_or_404(Comment.objects.prefetch_related('replies', 'replies__like', 'replies__dislike'),
                                     pk=comment_id).replies.all()
        paginator = CustomPagination()
        page = paginator.paginate_queryset(comments, request)
        ser_data = CommentSerializer(page, many=True)
        return paginator.get_paginated_response(ser_data.data)


class ReviewCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        existing_review = Review.objects.filter(user=request.user, book=book).first()

        if existing_review:
            return Response(
                {"error": "You have already reviewed this book. Please update your existing review."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ReviewSerializer(data=request.data)


        if serializer.is_valid():

            rate = request.data['rating']
            book_id = request.data['book']
            book = get_object_or_404(Book, pk=book_id)
            rating = Rating.objects.filter(user=request.user, book=book)
            if rating.exists():
                rating = rating.first()
                rating.rating = rate
                rating.save()
            else:
                Rating.objects.create(user=request.user, book=book, rating=rate)

            serializer.save(user=request.user, book=book)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewListAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)

        reviews = Review.objects.filter(book=book).annotate(
            priority=Case(When(user=request.user, then=Value(0)), default=Value(1),
                          output_field=IntegerField())).order_by('priority', '-created')

        paginator = CustomPagination()
        page = paginator.paginate_queryset(reviews, request)
        serializer = ReviewSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class ReviewUpdateDeleteAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        review = get_object_or_404(Review, user=request.user, book=book)

        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            if 'rating' in request.data:
                rate = request.data['rating']
                rating = Rating.objects.get(user=request.user, book=book)
                rating.delete()
                book.refresh_from_db(fields=['rating_sum', 'rating_count'])
                Rating.objects.create(user=request.user, book=book, rating=rate)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        review = get_object_or_404(Review, user=request.user, book=book)
        review.delete()
        rating = get_object_or_404(Rating,user=request.user, book=book)
        rating.delete()
        return Response({"message": "Review deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class ReviewLikeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, review_id):
        review = get_object_or_404(Review, pk=review_id)
        user = request.user
        if user in review.dislike.all():
            review.dislike.remove(user)
        if user in review.like.all():
            review.like.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        review.like.add(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewDisLikeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, review_id):
        review = get_object_or_404(Review, pk=review_id)
        user = request.user

        if user in review.like.all():
            review.like.remove(user)

        if user in review.dislike.all():
            review.dislike.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        review.dislike.add(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
