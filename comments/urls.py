from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CommentCreateAPIView.as_view(), name='comment-create'),
    path('like/<int:comment_id>/', views.CommentLikeAPIView.as_view(), name='comment-like'),
    path('dislike/<int:comment_id>/', views.CommentDisLikeAPIView.as_view(), name='comment-dislike'),
    path('reply_to/<int:comment_id>/', views.CommentReplyAPIView.as_view(), name='comment-reply'),
    path('chapter/<int:chapter_id>/', views.CommentChapterAPIView.as_view(), name='comment-chapter'),
    path('comment/<int:comment_id>/', views.CommentGetAllReplyAPIView.as_view(), name='comment-chapter'),
    path('user/reviews/', views.UserReviewListAPIView.as_view(), name='user-reviews'),
    path('user/comments/', views.UserCommentListAPIView.as_view(), name='user-comments'),
    path('user/posts/', views.UserPostListAPIView.as_view(), name='user-posts'),

    path('book/<int:book_id>/reviews/', views.ReviewListAPIView.as_view(), name='book-reviews'),
    path('book/<int:book_id>/reviews/create/', views.ReviewCreateAPIView.as_view(), name='create-review'),
    path('review/dislike/<int:review_id>/', views.ReviewDisLikeAPIView.as_view(), name='review-dislike'),
    path('review/like/<int:review_id>/', views.ReviewLikeAPIView.as_view(), name='review-like'),
    path('book/<int:book_id>/reviews/my-review/', views.ReviewUpdateDeleteAPIView.as_view(),
         name='update-delete-review'),

    path('threads/<int:thread_id>/posts/', views.PostGetAPIView.as_view(), name='api_thread_posts'),
    path('threads/<int:thread_id>/create/', views.PostCreateAPIView().as_view(), name='api_creating_post'),
    path('posts/<int:pk>/', views.PostUpdateAPIView.as_view(), name='api_Update_post'),
    path('posts/<int:post_id>/like/', views.PostLikeAPIView.as_view(), name='post-like'),
    path('posts/<int:post_id>/dislike/', views.PostDisLikeAPIView.as_view(), name='post-dislike'),
    path('post/reply/<int:post_id>/', views.PostReplyAPIView.as_view(), name='post-reply'),
]
