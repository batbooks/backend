from collections import defaultdict
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
    Returns top reviewers by total word count and includes review bodies.
    """
    top_reviewers_qs = (
        Review.objects.filter(book_id=book_id)
        .annotate(word_count=Length('body'))
        .values('user')
        .annotate(total_words=Sum('word_count'))
        .order_by('-total_words')[:limit]
    )

    top_user_ids = [r['user'] for r in top_reviewers_qs]

    review_bodies = Review.objects.filter(book_id=book_id, user__in=top_user_ids).values(
        'user', 'body'
    )

    user_reviews_map = defaultdict(list)
    for r in review_bodies:
        user_reviews_map[r['user']].append(r['body'])

    enriched_results = []
    for reviewer in top_reviewers_qs:
        user_id = reviewer['user']
        enriched_results.append({
            'user': user_id,
            'total_words': reviewer['total_words'],
            'reviews': user_reviews_map[user_id]
        })

    return enriched_results




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
    stats = {}

    stats['total_reviews'] = Review.objects.filter(book_id=book_id).count()
    stats['total_comments'] = Comment.objects.filter(chapter__book_id=book_id).count()
    stats['recent_reviews'] = get_recent_reviews_stats(book_id)['reviews']
    stats['recent_comments'] = get_recent_comments_stats(book_id)['comments']

    stats.update(get_favorites_and_blocks(book_id))

    stats['unique_reviewers'] = Review.objects.filter(book_id=book_id).values('user_id').distinct().count()
    stats['unique_commenters'] = Comment.objects.filter(chapter__book_id=book_id).values('user_id').distinct().count()

    stats['average_rating'] = (
        Review.objects.filter(book_id=book_id).aggregate(avg=Avg('rating'))['avg'] or 0
    )

    stats['recent_review_bodies'] = list(
        Review.objects.filter(book_id=book_id).order_by('-created').values('user_id', 'body', 'created')[:3]
    )

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
    Returns monthly review, comment stats, most active chapter, top commenters,
    and top reviewers by word count including review content.
    """
    now = timezone.now()
    start_year = now.year - 1
    monthly_stats = []

    for month in range(1, 13):
        month_start = timezone.make_aware(datetime(start_year, month, 1))
        if month == 12:
            next_month_start = timezone.make_aware(datetime(start_year + 1, 1, 1))
        else:
            next_month_start = timezone.make_aware(datetime(start_year, month + 1, 1))


        reviews_qs = Review.objects.filter(
            book_id=book_id,
            created__gte=month_start,
            created__lt=next_month_start
        )
        reviews_count = reviews_qs.count()


        comments_qs = Comment.objects.filter(
            chapter__book_id=book_id,
            created__gte=month_start,
            created__lt=next_month_start
        )
        comments_count = comments_qs.count()


        most_active_chapter_data = comments_qs.values('chapter_id').annotate(
            count=Count('id')
        ).order_by('-count').first()
        most_active_chapter = most_active_chapter_data['chapter_id'] if most_active_chapter_data else None


        top_commenters = list(
            comments_qs.values('user_id').annotate(
                count=Count('id')
            ).order_by('-count')[:3]
        )


        top_reviewers_ids = (
            reviews_qs
            .annotate(word_count=Length('body'))
            .values('user_id')
            .annotate(total_words=Sum('word_count'))
            .order_by('-total_words')[:3]
        )


        reviewer_ids = [r['user_id'] for r in top_reviewers_ids]
        reviews_with_content = (
            reviews_qs
            .filter(user_id__in=reviewer_ids)
            .values('user_id', 'body', 'created')
            .order_by('user_id', '-created')
        )


        from collections import defaultdict
        reviewer_content_map = defaultdict(list)
        for review in reviews_with_content:
            reviewer_content_map[review['user_id']].append(review['body'])


        top_reviewers = []
        for reviewer in top_reviewers_ids:
            reviewer['reviews'] = reviewer_content_map.get(reviewer['user_id'], [])
            top_reviewers.append(reviewer)

        monthly_stats.append({
            'month': month_start.strftime('%Y-%m'),
            'reviews': reviews_count,
            'comments': comments_count,
            'most_active_chapter': most_active_chapter,
            'top_commenters': top_commenters,
            'top_reviewers_by_words': top_reviewers,
        })

    return monthly_stats
