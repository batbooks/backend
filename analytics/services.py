from datetime import timedelta

from django.utils import timezone
from django.db import models
from django.db.models import Count, Sum, Avg, F, FloatField
from django.db.models.functions import Length, TruncDate
from django.contrib.auth import get_user_model
from datetime import datetime
from django.db.models.functions import TruncMonth

from book.models import Book, Chapter
from comments.models import Comment, Review
from book_actions.models import Favorite


# === Basic Book Stats ===

def get_recent_reviews_stats(book_id, days=30):
    """
    Returns count of recent reviews for a book within the given number of days.
    """
    now = timezone.now()
    since = now - timedelta(days=days)
    reviews_count = Review.objects.filter(book_id=book_id, created__gte=since).count()
    return {'reviews': reviews_count}


def get_recent_comments_stats(book_id, days=30):
    """
    Returns count of recent comments and average likes per comment for a book.
    """
    now = timezone.now()
    since = now - timedelta(days=days)

    comments = Comment.objects.filter(chapter__book_id=book_id, created__gte=since)
    comments_count = comments.count()

    return {
        'comments': comments_count,
    }


def get_favorites_and_blocks(book_id):
    """
    Returns count of favorites and blocks for a book.
    """
    book = Book.objects.get(id=book_id)
    favorites = book.favorite_groups.through.objects.filter(book=book).count()
    blocks = book.blocked_groups.through.objects.filter(book=book).count()

    return {
        'favorites': favorites,
        'blocks': blocks,
    }


# === Reviewer Insights ===

def get_top_reviewers_by_words(book_id, limit=10):
    """
    Returns top reviewers by total word count in their reviews.
    """
    return list(
        Review.objects.filter(book_id=book_id)
        .annotate(word_count=Length('body'))
        .values('user')
        .annotate(total_words=Sum('word_count'))
        .order_by('-total_words')[:limit]
    )





def get_top_users(limit=10):
    """
    Returns top users overall by total comments and reviews.
    """
    User = get_user_model()
    return list(
        User.objects.annotate(
            total_reviews=Count('u_comments_review'),
            total_comments=Count('u_comments_comment')
        )
        .order_by('-total_comments', '-total_reviews')[:limit]
        .values('id', 'name', 'total_reviews', 'total_comments')
    )


# === Engagement & Activity ===

def get_most_discussed_chapter(book_id):
    """
    Returns the chapter with the most comments.
    """
    return (
        Comment.objects.filter(chapter__book_id=book_id)
        .values('chapter')
        .annotate(num_comments=Count('id'))
        .order_by('-num_comments')
        .first()
    )


def get_highly_engaged_users(book_id):
    """
    Returns users who both commented and favorited the book.
    """
    favorited_users = set(
        Favorite.objects.filter(book__id=book_id).values_list('user_id', flat=True)
    )
    commented_users = set(
        Comment.objects.filter(chapter__book__id=book_id).values_list('user_id', flat=True)
    )
    return list(favorited_users & commented_users)


def get_daily_review_trends(book_id):
    """
    Returns count of reviews per day (last 5 days with reviews).
    """
    return list(
        Review.objects.filter(book_id=book_id)
        .annotate(day=TruncDate('created'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('-day')[:5]
    )


def get_chapter_engagement(book_id):
    """
    Returns comment count and average likes per comment per chapter.
    """
    return list(
        Chapter.objects.filter(book_id=book_id)
        .annotate(
            comment_count=Count('ch_comments_comment'),
        )
        .order_by('-comment_count')
        .values('id', 'comment_count')
    )


def get_top_comments(book_id, limit=5):
    """
    Returns top comments based on number of likes.
    """
    return list(
        Comment.objects.filter(chapter__book_id=book_id)
        .annotate(likes_count=Count('like'))
        .order_by('-likes_count')[:limit]
        .values('id', 'body', 'likes_count')
    )


# === Aggregated Reports ===

def get_book_basic_stats(book_id):
    """
    Combined basic stats for a book: reviews, comments, favorites, blocks.
    """
    stats = {}
    stats.update(get_recent_reviews_stats(book_id))
    stats.update(get_recent_comments_stats(book_id))
    stats.update(get_favorites_and_blocks(book_id))
    return stats


def get_book_reviewer_stats(book_id):
    """
    Reviewer-focused statistics for a book.
    """
    return {
        'top_reviewers_by_words': get_top_reviewers_by_words(book_id),
    }


def get_book_engagement_stats(book_id):
    """
    Engagement-related stats for a book.
    """
    return {
        'most_discussed_chapter': get_most_discussed_chapter(book_id),
        'daily_reviews': get_daily_review_trends(book_id),
        'chapter_engagement': get_chapter_engagement(book_id),
        'top_comments': get_top_comments(book_id),
    }



def get_monthly_stats_for_last_year(book_id):
    """
    Returns monthly review and comment stats for each month of last year.
    """
    now = timezone.now()
    start_year = now.year - 1
    monthly_stats = []

    for month in range(1, 13):
        # Get first day and next month start for filtering
        month_start = timezone.make_aware(datetime(start_year, month, 1))
        if month == 12:
            next_month_start = timezone.make_aware(datetime(start_year + 1, 1, 1))
        else:
            next_month_start = timezone.make_aware(datetime(start_year, month + 1, 1))

        # === Reviews ===
        reviews_count = Review.objects.filter(
            book_id=book_id,
            created__gte=month_start,
            created__lt=next_month_start
        ).count()

        # === Comments and avg likes ===
        comments_qs = Comment.objects.filter(
            chapter__book_id=book_id,
            created__gte=month_start,
            created__lt=next_month_start
        )
        comments_count = comments_qs.count()

        monthly_stats.append({
            'month': month_start.strftime('%Y-%m'),
            'reviews': reviews_count,
            'comments': comments_count,
        })

    return monthly_stats