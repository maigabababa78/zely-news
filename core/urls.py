from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("article/<slug:slug>/", views.article_detail, name="article_detail"),
    path("webtv/", views.webtv_hub, name="webtv_hub"),
    path("sport/", views.sport_hub, name="sport_hub"),
    path("sport/match/<int:match_id>/", views.match_detail_view, name="match_detail"),
    path("communaute/", views.community_hub, name="community_hub"),
    path("studio/", views.editorial_studio, name="editorial_studio"),

    # Progressive Web App (PWA) Standards
    path("manifest.json", views.pwa_manifest, name="pwa_manifest"),
    path("sw.js", views.pwa_service_worker, name="pwa_service_worker"),

    # User Authentication & Personal Connected Space
    path("inscription/", views.register_view, name="register"),
    path("connexion/", views.login_view, name="login"),
    path("deconnexion/", views.logout_view, name="logout"),
    path("mon-espace/", views.user_dashboard, {"section": "flux"}, name="user_dashboard"),
    path("mon-espace/<slug:section>/", views.user_dashboard, name="user_dashboard_section"),

    # AJAX Interactive Endpoints
    path("api/polls/<int:poll_id>/vote/", views.api_vote_poll, name="api_vote_poll"),
    path("api/articles/<int:article_id>/comment/", views.api_add_comment, name="api_add_comment"),
    path("api/articles/<int:article_id>/react/", views.api_react_article, name="api_react_article"),
    path("api/comments/<int:comment_id>/upvote/", views.api_upvote_comment, name="api_upvote_comment"),
    path("api/chat/", views.api_live_chat, name="api_live_chat"),
    path("api/citizen/submit/", views.api_submit_citizen_report, name="api_submit_citizen_report"),
    path("api/citizen/<int:report_id>/upvote/", views.api_upvote_report, name="api_upvote_report"),

    # Sport, LiveScore & FootMercato Endpoints
    path("api/sport/match/<int:match_id>/", views.api_match_detail, name="api_match_detail"),
    path("api/sport/match/<int:match_id>/prono/", views.api_vote_match_prono, name="api_vote_match_prono"),
    path("api/sport/mercato/<int:transfer_id>/vote/", views.api_vote_mercato, name="api_vote_mercato"),
    path("api/sport/live-pulse/", views.api_live_pulse, name="api_live_pulse"),
    path("api/sport/providers/config/", views.api_save_provider_config, name="api_save_provider_config"),

    # Newsroom RSS, Studio Q&A, Video Likes & Notifications
    path("api/news/sync-rss/", views.api_sync_rss_wires, name="api_sync_rss_wires"),
    path("api/studio/question/submit/", views.api_submit_studio_question, name="api_submit_studio_question"),
    path("api/studio/question/<int:question_id>/upvote/", views.api_upvote_studio_question, name="api_upvote_studio_question"),
    path("api/videos/<int:video_id>/like/", views.api_like_video, name="api_like_video"),
    path("api/notifications/read/", views.api_mark_notifications_read, name="api_mark_notifications_read"),

    # User Preferences & Bookmarks Endpoints
    path("api/user/preferences/", views.api_update_preferences, name="api_update_preferences"),
    path("api/user/bookmark/article/<int:article_id>/", views.api_toggle_bookmark_article, name="api_toggle_bookmark_article"),
    path("api/user/bookmark/video/<int:video_id>/", views.api_toggle_bookmark_video, name="api_toggle_bookmark_video"),
    path("api/user/follow/match/<int:match_id>/", views.api_toggle_follow_match, name="api_toggle_follow_match"),
]
