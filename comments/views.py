from collections import defaultdict
from math import floor
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from book.models import Chapter, Book
from forum.models import Thread
from book_actions.models import Rating
from comments.serializers import CommentSerializer, ReplyCommentSerializer, ReviewSerializer, PostSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from permissions import ReviewPostIsOwnerOrReadOnly
from comments.models import Comment, Review, Post
from django.shortcuts import get_object_or_404
from paginations import CustomPagination
from django.db.models import Case, When, Value, IntegerField, Count


class CommentCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    def post(self, request):
        ser_data = CommentSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save(user=request.user)
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response({"error": 'درخواست بد داده شده است.'}, status=status.HTTP_400_BAD_REQUEST)


class CommentLikeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            return Response(
                {"error": "کامنت مورد نظر پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )
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
        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            return Response(
                {"error": "کامنت مورد نظر پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )
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
    serializer_class = ReplyCommentSerializer

    def post(self, request, comment_id):

        try:
            reply_to_comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            return Response(
                {"error": "کامنتی برای پاسخ دادن پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )
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
    serializer_class = CommentSerializer

    def get(self, request, chapter_id):
        try:
            chapter = Chapter.objects.prefetch_related(
                'ch_comments_comment',
                'ch_comments_comment__like',
                'ch_comments_comment__dislike'
            ).get(pk=chapter_id)
        except Chapter.DoesNotExist:
            return Response(
                {"error": "چپتری با این شناسه پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )

        comments = chapter.ch_comments_comment.filter(reply__isnull=True)
        paginator = CustomPagination()
        page = paginator.paginate_queryset(comments, request)
        ser_data = CommentSerializer(page, many=True)
        return paginator.get_paginated_response(ser_data.data)


class CommentGetAllReplyAPIView(APIView):
    serializer_class = CommentSerializer

    def get(self, request, comment_id):
        try:
            comment = Comment.objects.prefetch_related(
                'replies',
                'replies__like',
                'replies__dislike'
            ).get(pk=comment_id)
        except Comment.DoesNotExist:
            return Response(
                {"error": "کامنتی با این شناسه پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )

        comments = comment.replies.all().order_by('created')
        paginator = CustomPagination()
        page = paginator.paginate_queryset(comments, request)
        ser_data = CommentSerializer(page, many=True)
        return paginator.get_paginated_response(ser_data.data)


class ReviewCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReviewSerializer

    def post(self, request, book_id):
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response(
                {"error": "کتابی با این شناسه پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )

        existing_review = Review.objects.filter(user=request.user, book=book).first()
        if existing_review:
            return Response(
                {"error": "شما قبلا در مورد این کتاب نظر داده اید.لطفا نظر ثبت شده خود را تغییر دهید."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, book=book)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewListAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ReviewSerializer

    def get(self, request, book_id):
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response(
                {"error": "کتابی با این شناسه پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )

        reviews = Review.objects.filter(book=book)

        if request.user.is_authenticated:
            reviews = reviews.annotate(
                priority=Case(
                    When(user=request.user, then=Value(0)),
                    default=Value(1),
                    output_field=IntegerField()
                )
            ).order_by('priority', '-created')
        else:
            reviews = reviews.order_by('-created')

        paginator = CustomPagination()
        page = paginator.paginate_queryset(reviews, request)
        serializer = ReviewSerializer(page, many=True)

        rating_data = (
            Rating.objects.filter(book=book)
            .values('rating')
            .annotate(count=Count('rating'))
        )

        rating_counts = defaultdict(int)

        for item in rating_data:
            quantized_rating = floor(float(item['rating']))
            rating_counts[quantized_rating] += item['count']

        return paginator.get_paginated_response({
            'reviews': serializer.data,
            'rating_counts': rating_counts
        })


class ReviewUpdateDeleteAPIView(APIView):
    permission_classes = (IsAuthenticated, ReviewPostIsOwnerOrReadOnly)
    serializer_class = ReviewSerializer

    def put(self, request, book_id):
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response(
                {"error": "کتابی با این شناسه پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            review = Review.objects.get(user=request.user, book=book)
        except Review.DoesNotExist:
            return Response(
                {"error": "نظری برای این کتاب توسط این کاربر پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )

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
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response(
                {"error": "کتاب مورد نظر پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            review = Review.objects.get(user=request.user, book=book)
        except Review.DoesNotExist:
            return Response(
                {"error": "نظرات مورد نظر پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )
        review.delete()
        return Response({"message": "نظر شما با موفقیت حذف شد."}, status=status.HTTP_204_NO_CONTENT)


class ReviewLikeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, review_id):
        try:
            review = Review.objects.get(pk=review_id)
        except Review.DoesNotExist:
            return Response(
                {"error": "نقدی با این شناسه پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )
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
        try:
            review = Review.objects.get(pk=review_id)
        except Review.DoesNotExist:
            return Response(
                {"error": "نقدی با این شناسه پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )
        user = request.user

        if user in review.like.all():
            review.like.remove(user)

        if user in review.dislike.all():
            review.dislike.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        review.dislike.add(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostGetAPIView(APIView):
    serializer_class = PostSerializer

    def get(self, request, thread_id):
        thread = get_object_or_404(Thread, id=thread_id)
        posts = thread.posts.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class PostCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def post(self, request, thread_id):
        thread = get_object_or_404(Thread, id=thread_id)

        if thread.status == Thread.STATUS_CLOSED:
            return Response({"messeage": "این گفت و گو بسته شده است. نمیتوانید در اینجا پست بگذارید.."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, thread=thread)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostUpdateAPIView(APIView):
    permission_classes = (IsAuthenticated, ReviewPostIsOwnerOrReadOnly)
    serializer_class = PostSerializer

    def get_object(self, pk):
        return get_object_or_404(Post, pk=pk)

    def check_thread_status(self, post):
        if post.thread.status == Thread.STATUS_CLOSED:
            return Response({"detail": "این گفت و گو بسته شده است. نمیتوانبد پستتات را تغییر دهید یا حذف کنید."},
                            status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk):
        post = self.get_object(pk)
        status_check = self.check_thread_status(post)
        if status_check:
            return status_check

        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        status_check = self.check_thread_status(post)
        if status_check:
            return status_check

        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostLikeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response(
                {"error": "پستی با این شناسه پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )

        user = request.user

        if user in post.dislike.all():
            post.dislike.remove(user)

        if user in post.like.all():
            post.like.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)

        post.like.add(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostDisLikeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response(
                {"error": "پستی با این شناسه پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )

        user = request.user

        if user in post.like.all():
            post.like.remove(user)

        if user in post.dislike.all():
            post.dislike.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)

        post.dislike.add(user)
        return Response(status=status.HTTP_204_NO_CONTENT)



class UserReviewListAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReviewSerializer

    def get(self, request):
        reviews = Review.objects.filter(user=request.user).order_by('-created')
        paginator = CustomPagination()
        page = paginator.paginate_queryset(reviews, request)
        serializer = self.serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class UserCommentListAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    def get(self, request):
        comments = Comment.objects.filter(user=request.user).order_by('-created')
        paginator = CustomPagination()
        page = paginator.paginate_queryset(comments, request)
        serializer = self.serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)










