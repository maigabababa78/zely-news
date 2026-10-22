from django.contrib import admin
from .models import (
    Category,
    Article,
    VideoItem,
    TVScheduleItem,
    Poll,
    PollOption,
    Comment,
    LiveChatMessage,
    CitizenReport,
    CommunityContributor,
    Competition,
    FootballMatch,
    MatchEvent,
    MercatoTransfer,
    LeagueStanding,
    UserProfile,
    LiveDataProviderConfig,
    TopScorer,
    StudioQuestion,
    UserNotification,
    LiveNewsWire,
)


class PollOptionInline(admin.TabularInline):
    model = PollOption
    extra = 3


class MatchEventInline(admin.TabularInline):
    model = MatchEvent
    extra = 2


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon", "color")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author_name", "is_breaking", "is_featured", "views_count", "created_at")
    list_filter = ("category", "is_breaking", "is_featured")
    search_fields = ("title", "summary", "content")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(VideoItem)
class VideoItemAdmin(admin.ModelAdmin):
    list_display = ("title", "video_type", "category", "show_name", "is_live_now", "viewers_count")
    list_filter = ("video_type", "category", "is_live_now")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(TVScheduleItem)
class TVScheduleItemAdmin(admin.ModelAdmin):
    list_display = ("order", "time_slot", "show_title", "host_name", "category", "is_on_air", "is_interactive")
    list_editable = ("is_on_air", "is_interactive")


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ("question", "category", "is_active", "created_at")
    inlines = [PollOptionInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user_name", "article", "stance", "upvotes", "created_at")
    list_filter = ("stance",)


@admin.register(LiveChatMessage)
class LiveChatMessageAdmin(admin.ModelAdmin):
    list_display = ("user_name", "message", "created_at")


@admin.register(CitizenReport)
class CitizenReportAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "reporter_name", "category", "media_type", "is_verified", "upvotes")
    list_filter = ("category", "media_type", "is_verified")


@admin.register(CommunityContributor)
class CommunityContributorAdmin(admin.ModelAdmin):
    list_display = ("name", "handle", "role_badge", "points", "reports_count", "debates_count")


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ("order", "flag_emoji", "name", "country", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(FootballMatch)
class FootballMatchAdmin(admin.ModelAdmin):
    list_display = ("home_team", "home_score", "away_score", "away_team", "competition", "status", "minute", "is_featured_match")
    list_filter = ("competition", "status", "is_featured_match")
    inlines = [MatchEventInline]


@admin.register(MercatoTransfer)
class MercatoTransferAdmin(admin.ModelAdmin):
    list_display = ("player_name", "from_club", "to_club", "transfer_fee", "status", "reliability_score", "is_exclusive")
    list_filter = ("status", "is_exclusive")


@admin.register(LeagueStanding)
class LeagueStandingAdmin(admin.ModelAdmin):
    list_display = ("competition", "rank", "team_name", "played", "won", "drawn", "lost", "goal_diff", "points")
    list_filter = ("competition",)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "display_name", "handle", "favorite_club", "preferred_mode", "reputation_points")
    list_filter = ("preferred_mode", "alert_breaking_news", "alert_mercato_foot")


@admin.register(LiveDataProviderConfig)
class LiveDataProviderConfigAdmin(admin.ModelAdmin):
    list_display = (
        "active_strategy",
        "last_active_source",
        "espn_calls_today",
        "thesportsdb_calls_today",
        "football_data_calls_today",
        "api_football_calls_today",
        "last_sync_at",
    )


@admin.register(TopScorer)
class TopScorerAdmin(admin.ModelAdmin):
    list_display = ("competition", "rank", "player_name", "club_name", "goals", "assists")
    list_filter = ("competition",)


@admin.register(StudioQuestion)
class StudioQuestionAdmin(admin.ModelAdmin):
    list_display = ("user_name", "show_name", "question_text", "upvotes", "is_answered_on_air", "created_at")
    list_editable = ("is_answered_on_air",)


@admin.register(UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):
    list_display = ("notif_type", "title", "user", "is_read", "created_at")
    list_filter = ("notif_type", "is_read")


@admin.register(LiveNewsWire)
class LiveNewsWireAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "source_name", "is_urgent", "created_at")
    list_filter = ("category", "is_urgent")



