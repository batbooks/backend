from django.urls import path
from . import views
urlpatterns =[
    path('create/',views.CommentCreateAPIView.as_view(),name='comment-create'),
    path('like/<int:comment_id>/',views.CommentLikeAPIView.as_view(),name='comment-like'),
    path('dislike/<int:comment_id>/',views.CommentDisLikeAPIView.as_view(),name='comment-dislike'),
    path('reply_to/<int:comment_id>/',views.CommentReplyAPIView.as_view(),name='comment-reply'),
    path('chapter/<int:chapter_id>/',views.CommentChapterAPIView.as_view(),name='comment-chapter'),
    path('comment/<int:comment_id>/',views.CommentGetAllReplyAPIView.as_view(),name='comment-chapter'),

    path('books/<int:book_id>/reviews/', views.ReviewListAPIView.as_view(), name='book-reviews'),
    path('books/<int:book_id>/review/create/', views.ReviewCreateAPIView.as_view(), name='create-review'),
    path('books/<int:book_id>/review/my-review/', views.ReviewUpdateDeleteAPIView.as_view(), name='update-delete-review'),
]