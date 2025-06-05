from django.urls import path
from . import views
from .views import (
    BookBasicStatsView,
    BookReviewerStatsView,
    BookEngagementStatsView,
)




urlpatterns = [
    path('books/<int:book_id>/stats/basic/', views.BookBasicStatsView.as_view(), name='book-basic-stats'),
    path('books/<int:book_id>/stats/reviewers/', views.BookReviewerStatsView.as_view(), name='book-reviewer-stats'),
    path('books/<int:book_id>/stats/engagement/', views.BookEngagementStatsView.as_view(), name='book-engagement-stats'),
    path('<int:book_id>/monthly-stats/', views.BookMonthlyStatsView.as_view()),
]