from django.urls import path
from . import views
urlpatterns =[
    path('create/',views.CommentCreateAPIView.as_view(),name='comment-create'),
    path('like/<int:comment_id>/',views.CommentLikeAPIView.as_view(),name='comment-like'),
    path('dislike/<int:comment_id>/',views.CommentDisLikeAPIView.as_view(),name='comment-dislike'),
    path('reply/<int:comment_id>/',views.CommentReplyAPIView.as_view(),name='comment-reply'),
    path('chapter/<int:chapter_id>/',views.CommentChapterAPIView.as_view(),name='comment-chapter'),
]