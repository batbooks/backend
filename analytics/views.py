from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from analytics.services import (
    get_book_basic_stats,
    get_book_reviewer_stats,
    get_book_engagement_stats,
    get_monthly_stats_for_last_year
)

class BookBasicStatsView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, book_id):
        stats = get_book_basic_stats(book_id)
        return Response(stats)


class BookReviewerStatsView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, book_id):
        stats = get_book_reviewer_stats(book_id)
        return Response(stats)


class BookEngagementStatsView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, book_id):
        stats = get_book_engagement_stats(book_id)
        return Response(stats)




class BookMonthlyStatsView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, book_id):
        stats = get_monthly_stats_for_last_year(book_id)
        return Response(stats)