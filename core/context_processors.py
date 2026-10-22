from django.db.models import Q
from .models import Category, Article, VideoItem, UserProfile, UserNotification


def global_news_context(request):
    """Provides global categories, breaking news ticker, active live stream, user profile, and notifications."""
    user_profile = None
    saved_article_ids = set()
    saved_video_ids = set()
    followed_match_ids = set()
    notifications = []
    unread_notif_count = 0

    try:
        categories = Category.objects.all()
        breaking_articles = Article.objects.filter(is_breaking=True)[:6]
        active_live = VideoItem.objects.filter(video_type="LIVE", is_live_now=True).first()
        if not active_live:
            active_live = VideoItem.objects.filter(video_type="LIVE").first()

        if request.user.is_authenticated:
            user_profile, _ = UserProfile.objects.get_or_create(
                user=request.user,
                defaults={
                    "display_name": request.user.first_name or request.user.username,
                    "handle": f"@{request.user.username.lower()[:16]}",
                },
            )
            saved_article_ids = set(user_profile.saved_articles.values_list("id", flat=True))
            saved_video_ids = set(user_profile.saved_videos.values_list("id", flat=True))
            followed_match_ids = set(user_profile.followed_matches.values_list("id", flat=True))
            notifs_qs = UserNotification.objects.filter(Q(user=request.user) | Q(user__isnull=True))[:8]
            notifications = list(notifs_qs)
            unread_notif_count = sum(1 for n in notifications if not n.is_read)
        else:
            notifs_qs = UserNotification.objects.filter(user__isnull=True)[:6]
            notifications = list(notifs_qs)
            unread_notif_count = sum(1 for n in notifications if not n.is_read)
    except Exception:
        categories = []
        breaking_articles = []
        active_live = None

    return {
        "global_categories": categories,
        "breaking_articles": breaking_articles,
        "global_live": active_live,
        "current_profile": user_profile,
        "saved_article_ids": saved_article_ids,
        "saved_video_ids": saved_video_ids,
        "followed_match_ids": followed_match_ids,
        "global_notifications": notifications,
        "unread_notif_count": unread_notif_count,
    }
