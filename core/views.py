import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, F
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
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


def home(request):
    category_slug = request.GET.get("category")
    search_query = request.GET.get("q", "").strip()

    articles_qs = Article.objects.select_related("category").all()
    videos_qs = VideoItem.objects.select_related("category").all()
    citizen_qs = CitizenReport.objects.select_related("category").all()

    active_category = None
    if category_slug:
        active_category = Category.objects.filter(slug=category_slug).first()
        if active_category:
            articles_qs = articles_qs.filter(category=active_category)
            videos_qs = videos_qs.filter(category=active_category)
            citizen_qs = citizen_qs.filter(category=active_category)

    if search_query:
        articles_qs = articles_qs.filter(
            Q(title__icontains=search_query)
            | Q(summary__icontains=search_query)
            | Q(content__icontains=search_query)
        )
        videos_qs = videos_qs.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

    featured_article = articles_qs.filter(is_featured=True).first() or articles_qs.first()
    latest_articles = articles_qs.exclude(id=featured_article.id if featured_article else None)[:8]
    trending_articles = Article.objects.select_related("category").order_by("-views_count")[:5]

    live_stream = VideoItem.objects.filter(video_type="LIVE", is_live_now=True).first() or VideoItem.objects.filter(video_type="LIVE").first()
    vod_videos = videos_qs.filter(video_type="VOD")[:6]
    short_videos = videos_qs.filter(video_type="SHORT")[:6]

    active_polls = Poll.objects.prefetch_related("options").filter(is_active=True)[:2]
    chat_messages = LiveChatMessage.objects.all()[:20]
    citizen_reports = citizen_qs[:4]
    tv_schedule = TVScheduleItem.objects.select_related("category").all()[:5]
    top_contributors = CommunityContributor.objects.all()[:4]
    live_football_matches = FootballMatch.objects.select_related("competition").all()[:6]
    hot_mercato = MercatoTransfer.objects.all()[:3]
    live_wires = LiveNewsWire.objects.select_related("category").all()[:10]

    context = {
        "active_category": active_category,
        "search_query": search_query,
        "featured_article": featured_article,
        "latest_articles": latest_articles,
        "trending_articles": trending_articles,
        "live_stream": live_stream,
        "vod_videos": vod_videos,
        "short_videos": short_videos,
        "active_polls": active_polls,
        "chat_messages": reversed(list(chat_messages)),
        "citizen_reports": citizen_reports,
        "tv_schedule": tv_schedule,
        "top_contributors": top_contributors,
        "live_football_matches": live_football_matches,
        "hot_mercato": hot_mercato,
        "live_wires": live_wires,
    }
    return render(request, "core/home.html", context)


def article_detail(request, slug):
    article = get_object_or_404(Article.objects.select_related("category"), slug=slug)
    Article.objects.filter(pk=article.pk).update(views_count=F("views_count") + 1)
    article.refresh_from_db()

    related_articles = (
        Article.objects.filter(category=article.category)
        .exclude(pk=article.pk)[:3]
    )
    comments = article.comments.all()
    article_poll = article.polls.prefetch_related("options").first() or Poll.objects.prefetch_related("options").filter(is_active=True).first()

    pro_count = comments.filter(stance="PRO").count()
    con_count = comments.filter(stance="CON").count()
    neutral_count = comments.filter(stance="NEUTRAL").count()
    total_stances = pro_count + con_count
    pro_percent = round((pro_count / total_stances) * 100) if total_stances > 0 else 50
    con_percent = 100 - pro_percent if total_stances > 0 else 50

    context = {
        "article": article,
        "related_articles": related_articles,
        "comments": comments,
        "article_poll": article_poll,
        "pro_count": pro_count,
        "con_count": con_count,
        "neutral_count": neutral_count,
        "pro_percent": pro_percent,
        "con_percent": con_percent,
    }
    return render(request, "core/article_detail.html", context)


def webtv_hub(request):
    category_slug = request.GET.get("category")
    video_slug = request.GET.get("watch")

    active_category = None
    videos_qs = VideoItem.objects.select_related("category").all()
    if category_slug:
        active_category = Category.objects.filter(slug=category_slug).first()
        if active_category:
            videos_qs = videos_qs.filter(category=active_category)

    if video_slug:
        current_video = VideoItem.objects.filter(slug=video_slug).first()
    else:
        current_video = None

    if not current_video:
        current_video = (
            VideoItem.objects.filter(video_type="LIVE", is_live_now=True).first()
            or videos_qs.first()
        )

    vod_videos = videos_qs.filter(video_type="VOD")
    short_videos = videos_qs.filter(video_type="SHORT")
    live_streams = VideoItem.objects.filter(video_type="LIVE")
    chat_messages = LiveChatMessage.objects.all()[:25]
    tv_schedule = TVScheduleItem.objects.select_related("category").all()
    studio_questions = StudioQuestion.objects.all()[:8]

    context = {
        "active_category": active_category,
        "current_video": current_video,
        "vod_videos": vod_videos,
        "short_videos": short_videos,
        "live_streams": live_streams,
        "chat_messages": reversed(list(chat_messages)),
        "tv_schedule": tv_schedule,
        "studio_questions": studio_questions,
    }
    return render(request, "core/webtv.html", context)


def community_hub(request):
    category_slug = request.GET.get("category")
    reports_qs = CitizenReport.objects.select_related("category").all()
    active_category = None
    if category_slug:
        active_category = Category.objects.filter(slug=category_slug).first()
        if active_category:
            reports_qs = reports_qs.filter(category=active_category)

    polls = Poll.objects.prefetch_related("options").filter(is_active=True)
    recent_comments = Comment.objects.select_related("article").order_by("-created_at")[:8]
    top_contributors = CommunityContributor.objects.all()[:5]

    context = {
        "active_category": active_category,
        "citizen_reports": reports_qs,
        "polls": polls,
        "recent_comments": recent_comments,
        "top_contributors": top_contributors,
    }
    return render(request, "core/community.html", context)


# --- Interactive AJAX APIs ---

@require_POST
def api_vote_poll(request, poll_id):
    try:
        data = json.loads(request.body)
        option_id = data.get("option_id")
    except Exception:
        option_id = request.POST.get("option_id")

    poll = get_object_or_404(Poll, pk=poll_id)
    option = get_object_or_404(PollOption, pk=option_id, poll=poll)
    PollOption.objects.filter(pk=option.pk).update(votes=F("votes") + 1)

    poll.refresh_from_db()
    options_data = []
    total = poll.total_votes()
    for opt in poll.options.all():
        pct = round((opt.votes / total) * 100) if total > 0 else 0
        options_data.append({
            "id": opt.id,
            "text": opt.text,
            "votes": opt.votes,
            "percentage": pct,
        })

    return JsonResponse({
        "status": "ok",
        "poll_id": poll.id,
        "total_votes": total,
        "options": options_data,
    })


@require_POST
def api_add_comment(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    try:
        data = json.loads(request.body)
    except Exception:
        data = request.POST

    user_name = (data.get("user_name") or "Citoyen Zely").strip()[:80]
    stance = data.get("stance", "NEUTRAL")
    if stance not in ("NEUTRAL", "PRO", "CON"):
        stance = "NEUTRAL"
    content = (data.get("content") or "").strip()

    if not content:
        return JsonResponse({"status": "error", "message": "Le commentaire ne peut pas être vide."}, status=400)

    badge_map = {
        "PRO": "Débatteur • Pour",
        "CON": "Débatteur • Contre",
        "NEUTRAL": "Analyste Citoyen",
    }

    comment = Comment.objects.create(
        article=article,
        user_name=user_name,
        user_badge=badge_map.get(stance, "Membre Zely"),
        stance=stance,
        content=content,
        upvotes=1,
    )

    comments = article.comments.all()
    pro_count = comments.filter(stance="PRO").count()
    con_count = comments.filter(stance="CON").count()
    total_stances = pro_count + con_count
    pro_percent = round((pro_count / total_stances) * 100) if total_stances > 0 else 50
    con_percent = 100 - pro_percent if total_stances > 0 else 50

    return JsonResponse({
        "status": "ok",
        "comment": {
            "id": comment.id,
            "user_name": comment.user_name,
            "user_badge": comment.user_badge,
            "stance": comment.stance,
            "content": comment.content,
            "upvotes": comment.upvotes,
            "created_at": "À l'instant",
        },
        "debate": {
            "pro_count": pro_count,
            "con_count": con_count,
            "pro_percent": pro_percent,
            "con_percent": con_percent,
        }
    })


@require_POST
def api_react_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    try:
        data = json.loads(request.body)
    except Exception:
        data = request.POST

    reaction = data.get("reaction", "like")
    if reaction == "fire":
        Article.objects.filter(pk=article.pk).update(fire_count=F("fire_count") + 1)
    elif reaction == "mindblown":
        Article.objects.filter(pk=article.pk).update(mindblown_count=F("mindblown_count") + 1)
    else:
        Article.objects.filter(pk=article.pk).update(likes_count=F("likes_count") + 1)

    article.refresh_from_db()
    return JsonResponse({
        "status": "ok",
        "likes_count": article.likes_count,
        "fire_count": article.fire_count,
        "mindblown_count": article.mindblown_count,
    })


def api_live_chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except Exception:
            data = request.POST

        user_name = (data.get("user_name") or "Spectateur").strip()[:60]
        message_text = (data.get("message") or "").strip()[:400]
        if not message_text:
            return JsonResponse({"status": "error"}, status=400)

        colors = ["text-cyan-400", "text-emerald-400", "text-amber-400", "text-purple-400", "text-pink-400"]
        color = colors[len(user_name) % len(colors)]

        msg = LiveChatMessage.objects.create(
            user_name=user_name,
            user_color=color,
            user_badge="LIVE",
            message=message_text,
        )
        return JsonResponse({
            "status": "ok",
            "message": {
                "id": msg.id,
                "user_name": msg.user_name,
                "user_color": msg.user_color,
                "user_badge": msg.user_badge,
                "message": msg.message,
                "time": msg.created_at.strftime("%H:%M"),
            }
        })

    messages = LiveChatMessage.objects.all()[:25]
    data = [
        {
            "id": m.id,
            "user_name": m.user_name,
            "user_color": m.user_color,
            "user_badge": m.user_badge,
            "message": m.message,
            "time": m.created_at.strftime("%H:%M"),
        }
        for m in reversed(list(messages))
    ]
    return JsonResponse({"status": "ok", "messages": data})


@require_POST
def api_submit_citizen_report(request):
    try:
        data = json.loads(request.body)
    except Exception:
        data = request.POST

    title = (data.get("title") or "").strip()
    location = (data.get("location") or "En direct").strip()
    reporter_name = (data.get("reporter_name") or "Reporter Citoyen").strip()
    category_id = data.get("category_id")
    media_type = data.get("media_type", "PHOTO")
    media_url = (data.get("media_url") or "").strip()
    description = (data.get("description") or "").strip()

    if not title or not description:
        return JsonResponse({"status": "error", "message": "Titre et description requis."}, status=400)

    category = Category.objects.filter(pk=category_id).first() or Category.objects.first()
    if not media_url:
        default_images = {
            "VIDEO": "https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=800&auto=format&fit=crop&q=80",
            "PHOTO": "https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=800&auto=format&fit=crop&q=80",
            "TEXT": "https://images.unsplash.com/photo-1495020689067-958852a7765e?w=800&auto=format&fit=crop&q=80",
        }
        media_url = default_images.get(media_type, default_images["PHOTO"])

    handle = "@" + "".join(c for c in reporter_name.lower() if c.isalnum())[:18]
    report = CitizenReport.objects.create(
        title=title,
        category=category,
        location=location,
        reporter_name=reporter_name,
        reporter_handle=handle,
        description=description,
        media_type=media_type,
        media_url=media_url,
        is_verified=True,
        upvotes=1,
    )

    return JsonResponse({
        "status": "ok",
        "report": {
            "id": report.id,
            "title": report.title,
            "category_name": report.category.name,
            "category_badge": report.category.badge_bg,
            "location": report.location,
            "reporter_name": report.reporter_name,
            "reporter_handle": report.reporter_handle,
            "description": report.description,
            "media_type": report.get_media_type_display(),
            "media_code": report.media_type,
            "media_url": report.media_url,
            "upvotes": report.upvotes,
        }
    })


@require_POST
def api_upvote_report(request, report_id):
    report = get_object_or_404(CitizenReport, pk=report_id)
    CitizenReport.objects.filter(pk=report.pk).update(upvotes=F("upvotes") + 1)
    report.refresh_from_db()
    return JsonResponse({"status": "ok", "upvotes": report.upvotes})


@require_POST
def api_upvote_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    Comment.objects.filter(pk=comment.pk).update(upvotes=F("upvotes") + 1)
    comment.refresh_from_db()
    return JsonResponse({"status": "ok", "upvotes": comment.upvotes})


# ==============================================================================
# SPORT, LIVESCORE & FOOTMERCATO HUB VIEWS & APIS
# ==============================================================================

def sport_hub(request):
    comp_slug = request.GET.get("comp", "").strip()
    status_filter = request.GET.get("status", "").strip()
    mercato_filter = request.GET.get("mercato", "").strip()

    competitions = Competition.objects.all()
    active_comp = Competition.objects.filter(slug=comp_slug).first() if comp_slug else None

    matches_qs = FootballMatch.objects.select_related("competition").prefetch_related("events").all()
    if active_comp:
        matches_qs = matches_qs.filter(competition=active_comp)
    if status_filter in ("LIVE", "HT", "FT", "UPCOMING"):
        matches_qs = matches_qs.filter(status=status_filter)

    featured_match = (
        matches_qs.filter(is_featured_match=True).first()
        or FootballMatch.objects.prefetch_related("events").filter(is_featured_match=True).first()
        or matches_qs.first()
    )

    mercato_qs = MercatoTransfer.objects.all()
    if mercato_filter in ("OFFICIAL", "ADVANCED", "NEGOTIATION", "RUMOR"):
        mercato_qs = mercato_qs.filter(status=mercato_filter)

    standings_comp = active_comp or competitions.first()
    standings = LeagueStanding.objects.filter(competition=standings_comp) if standings_comp else []
    top_scorers = TopScorer.objects.filter(competition=standings_comp)[:8] if standings_comp else []

    sport_category = Category.objects.filter(slug="sport-esport").first()
    sport_articles = Article.objects.filter(category=sport_category)[:6] if sport_category else []
    sport_videos = VideoItem.objects.filter(category=sport_category)[:4] if sport_category else []
    provider_config = LiveDataProviderConfig.get_solo()

    context = {
        "competitions": competitions,
        "active_comp": active_comp,
        "status_filter": status_filter,
        "mercato_filter": mercato_filter,
        "matches": matches_qs,
        "featured_match": featured_match,
        "mercato_transfers": mercato_qs,
        "standings_comp": standings_comp,
        "standings": standings,
        "top_scorers": top_scorers,
        "sport_articles": sport_articles,
        "sport_videos": sport_videos,
        "provider_config": provider_config,
    }
    return render(request, "core/sport_hub.html", context)


def match_detail_view(request, match_id):
    """Dedicated Match Center page for a selected football match."""
    match = get_object_or_404(
        FootballMatch.objects.select_related("competition").prefetch_related("events"),
        pk=match_id,
    )
    home_lineup_list = [p.strip() for p in match.home_lineup.split("-") if p.strip()]
    away_lineup_list = [p.strip() for p in match.away_lineup.split("-") if p.strip()]
    other_comp_matches = (
        FootballMatch.objects.select_related("competition")
        .filter(competition=match.competition)
        .exclude(pk=match.id)[:8]
    )
    live_matches = FootballMatch.objects.select_related("competition").filter(status__in=["LIVE", "HT"])[:10]
    standings = LeagueStanding.objects.filter(competition=match.competition)

    is_followed = False
    if request.user.is_authenticated and hasattr(request.user, "profile"):
        is_followed = request.user.profile.followed_matches.filter(pk=match.id).exists()

    return render(request, "core/match_detail.html", {
        "match": match,
        "home_lineup_list": home_lineup_list,
        "away_lineup_list": away_lineup_list,
        "other_comp_matches": other_comp_matches,
        "live_matches": live_matches,
        "standings": standings,
        "is_followed": is_followed,
    })


def api_match_detail(request, match_id):
    match = get_object_or_404(FootballMatch.objects.select_related("competition").prefetch_related("events"), pk=match_id)
    events = [
        {
            "minute": ev.minute,
            "type": ev.event_type,
            "label": ev.get_event_type_display(),
            "side": ev.team_side,
            "player": ev.player_name,
            "detail": ev.detail,
        }
        for ev in match.events.all()
    ]
    return JsonResponse({
        "status": "ok",
        "match": {
            "id": match.id,
            "competition": match.competition.name,
            "flag": match.competition.flag_emoji,
            "home_team": match.home_team,
            "home_short": match.home_short,
            "away_team": match.away_team,
            "away_short": match.away_short,
            "home_score": match.home_score,
            "away_score": match.away_score,
            "match_status": match.status,
            "minute": match.minute,
            "stadium": match.stadium,
            "tv_channel": match.tv_channel,
            "stream_url": match.stream_url,
            "home_possession": match.home_possession,
            "away_possession": match.away_possession,
            "home_shots": match.home_shots,
            "away_shots": match.away_shots,
            "home_shots_on_target": match.home_shots_on_target,
            "away_shots_on_target": match.away_shots_on_target,
            "home_xg": match.home_xg,
            "away_xg": match.away_xg,
            "home_corners": match.home_corners,
            "away_corners": match.away_corners,
            "home_formation": match.home_formation,
            "away_formation": match.away_formation,
            "home_lineup": [p.strip() for p in match.home_lineup.split("-")],
            "away_lineup": [p.strip() for p in match.away_lineup.split("-")],
            "votes_home": match.votes_home,
            "votes_draw": match.votes_draw,
            "votes_away": match.votes_away,
            "home_win_pct": match.home_win_pct(),
            "draw_pct": match.draw_pct(),
            "away_win_pct": match.away_win_pct(),
            "events": events,
        }
    })


@require_POST
def api_vote_match_prono(request, match_id):
    match = get_object_or_404(FootballMatch, pk=match_id)
    try:
        data = json.loads(request.body)
    except Exception:
        data = request.POST

    choice = data.get("choice", "1")
    if choice == "1":
        FootballMatch.objects.filter(pk=match.pk).update(votes_home=F("votes_home") + 1)
    elif choice == "N":
        FootballMatch.objects.filter(pk=match.pk).update(votes_draw=F("votes_draw") + 1)
    elif choice == "2":
        FootballMatch.objects.filter(pk=match.pk).update(votes_away=F("votes_away") + 1)

    match.refresh_from_db()
    return JsonResponse({
        "status": "ok",
        "total": match.total_prono_votes(),
        "votes_home": match.votes_home,
        "votes_draw": match.votes_draw,
        "votes_away": match.votes_away,
        "home_win_pct": match.home_win_pct(),
        "draw_pct": match.draw_pct(),
        "away_win_pct": match.away_win_pct(),
    })


@require_POST
def api_vote_mercato(request, transfer_id):
    transfer = get_object_or_404(MercatoTransfer, pk=transfer_id)
    try:
        data = json.loads(request.body)
    except Exception:
        data = request.POST

    verdict = data.get("verdict", "good")
    if verdict == "overrated":
        MercatoTransfer.objects.filter(pk=transfer.pk).update(overrated_votes=F("overrated_votes") + 1)
    else:
        MercatoTransfer.objects.filter(pk=transfer.pk).update(good_deal_votes=F("good_deal_votes") + 1)

    transfer.refresh_from_db()
    return JsonResponse({
        "status": "ok",
        "good_deal_votes": transfer.good_deal_votes,
        "overrated_votes": transfer.overrated_votes,
        "good_deal_pct": transfer.good_deal_pct(),
        "overrated_pct": transfer.overrated_pct(),
    })


# ==============================================================================
# USER AUTHENTICATION, CONNECTED SPACE ("MON ESPACE ZELY") & PREFERENCES
# ==============================================================================

def register_view(request):
    if request.user.is_authenticated:
        return redirect("user_dashboard")

    categories = Category.objects.all()
    competitions = Competition.objects.all()
    error = None

    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        email = (request.POST.get("email") or "").strip()
        password = request.POST.get("password") or ""
        display_name = (request.POST.get("display_name") or username).strip()
        city = (request.POST.get("city") or "Paris").strip()
        favorite_club = (request.POST.get("favorite_club") or "Paris Saint-Germain").strip()
        preferred_mode = request.POST.get("preferred_mode") or "HYBRID"
        selected_cats = request.POST.getlist("categories")
        selected_comps = request.POST.getlist("competitions")

        if not username or not password:
            error = "Veuillez renseigner un identifiant et un mot de passe."
        elif User.objects.filter(username__iexact=username).exists():
            error = "Cet identifiant est déjà utilisé. Choisissez-en un autre."
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=display_name[:30],
            )
            handle = "@" + "".join(c for c in username.lower() if c.isalnum())[:16]
            profile = UserProfile.objects.create(
                user=user,
                display_name=display_name,
                handle=handle,
                city=city,
                favorite_club=favorite_club,
                preferred_mode=preferred_mode,
                reputation_points=200,  # Bonus d'inscription
            )
            if selected_cats:
                profile.favorite_categories.set(Category.objects.filter(id__in=selected_cats))
            else:
                profile.favorite_categories.set(categories)

            if selected_comps:
                profile.favorite_competitions.set(Competition.objects.filter(id__in=selected_comps))
            else:
                profile.favorite_competitions.set(competitions[:2])

            login(request, user)
            return redirect("user_dashboard")

    return render(request, "core/auth.html", {
        "mode": "register",
        "categories": categories,
        "competitions": competitions,
        "error": error,
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect("user_dashboard")

    error = None
    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password = request.POST.get("password") or ""
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    "display_name": user.first_name or user.username,
                    "handle": f"@{user.username.lower()[:16]}",
                },
            )
            return redirect("user_dashboard")
        else:
            error = "Identifiant ou mot de passe incorrect."

    return render(request, "core/auth.html", {
        "mode": "login",
        "error": error,
    })


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required(login_url="/connexion/")
def user_dashboard(request, section="flux"):
    valid_sections = {"flux", "sport", "favoris", "contributions", "parametres"}
    if section not in valid_sections:
        section = "flux"

    profile, _ = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={
            "display_name": request.user.first_name or request.user.username,
            "handle": f"@{request.user.username.lower()[:16]}",
        },
    )

    fav_cats = profile.favorite_categories.all()
    if fav_cats.exists():
        personalized_articles = Article.objects.select_related("category").filter(category__in=fav_cats)[:6]
        personalized_videos = VideoItem.objects.select_related("category").filter(category__in=fav_cats)[:4]
    else:
        personalized_articles = Article.objects.select_related("category").all()[:6]
        personalized_videos = VideoItem.objects.select_related("category").all()[:4]

    fav_comps = profile.favorite_competitions.all()
    if fav_comps.exists():
        my_matches = FootballMatch.objects.select_related("competition").filter(
            Q(competition__in=fav_comps)
            | Q(home_team__icontains=profile.favorite_club)
            | Q(away_team__icontains=profile.favorite_club)
        ).distinct()[:6]
    else:
        my_matches = FootballMatch.objects.select_related("competition").all()[:4]

    club_mercato = MercatoTransfer.objects.filter(
        Q(from_club__icontains=profile.favorite_club) | Q(to_club__icontains=profile.favorite_club)
    )[:4]
    if not club_mercato.exists():
        club_mercato = MercatoTransfer.objects.all()[:3]

    saved_articles = profile.saved_articles.select_related("category").all()
    saved_videos = profile.saved_videos.select_related("category").all()
    followed_matches = profile.followed_matches.select_related("competition").all()

    user_comments = Comment.objects.select_related("article").filter(
        Q(user_name__iexact=profile.get_name()) | Q(user_name__iexact=request.user.username)
    )[:6]
    user_reports = CitizenReport.objects.select_related("category").filter(
        Q(reporter_name__iexact=profile.get_name()) | Q(reporter_handle__iexact=profile.handle)
    )[:6]

    all_categories = Category.objects.all()
    all_competitions = Competition.objects.all()

    context = {
        "section": section,
        "profile": profile,
        "personalized_articles": personalized_articles,
        "personalized_videos": personalized_videos,
        "my_matches": my_matches,
        "club_mercato": club_mercato,
        "saved_articles": saved_articles,
        "saved_videos": saved_videos,
        "followed_matches": followed_matches,
        "user_comments": user_comments,
        "user_reports": user_reports,
        "all_categories": all_categories,
        "all_competitions": all_competitions,
        "fav_cat_ids": set(fav_cats.values_list("id", flat=True)),
        "fav_comp_ids": set(fav_comps.values_list("id", flat=True)),
    }
    return render(request, "core/dashboard.html", context)


@login_required(login_url="/connexion/")
@require_POST
def api_update_preferences(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    try:
        data = json.loads(request.body)
    except Exception:
        data = request.POST

    profile.display_name = (data.get("display_name") or profile.display_name).strip()[:80]
    profile.bio = (data.get("bio") or profile.bio).strip()[:300]
    profile.city = (data.get("city") or profile.city).strip()[:80]
    profile.favorite_club = (data.get("favorite_club") or profile.favorite_club).strip()[:80]
    profile.preferred_mode = data.get("preferred_mode") or profile.preferred_mode
    if data.get("avatar_url"):
        profile.avatar_url = data.get("avatar_url").strip()

    profile.alert_breaking_news = bool(data.get("alert_breaking_news", True))
    profile.alert_live_tv = bool(data.get("alert_live_tv", True))
    profile.alert_mercato_foot = bool(data.get("alert_mercato_foot", True))
    profile.autoplay_pip = bool(data.get("autoplay_pip", True))
    profile.save()

    cat_ids = data.get("category_ids", [])
    if isinstance(cat_ids, list):
        profile.favorite_categories.set(Category.objects.filter(id__in=cat_ids))

    comp_ids = data.get("competition_ids", [])
    if isinstance(comp_ids, list):
        profile.favorite_competitions.set(Competition.objects.filter(id__in=comp_ids))

    return JsonResponse({"status": "ok", "message": "Vos préférences et abonnements ont été enregistrés."})


@require_POST
def api_toggle_bookmark_article(request, article_id):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "auth_required", "redirect": "/connexion/"}, status=401)
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    article = get_object_or_404(Article, pk=article_id)
    if profile.saved_articles.filter(pk=article.pk).exists():
        profile.saved_articles.remove(article)
        saved = False
    else:
        profile.saved_articles.add(article)
        profile.reputation_points = F("reputation_points") + 5
        profile.save(update_fields=["reputation_points"])
        saved = True
    return JsonResponse({"status": "ok", "saved": saved, "count": profile.saved_articles.count()})


@require_POST
def api_toggle_bookmark_video(request, video_id):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "auth_required", "redirect": "/connexion/"}, status=401)
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    video = get_object_or_404(VideoItem, pk=video_id)
    if profile.saved_videos.filter(pk=video.pk).exists():
        profile.saved_videos.remove(video)
        saved = False
    else:
        profile.saved_videos.add(video)
        saved = True
    return JsonResponse({"status": "ok", "saved": saved, "count": profile.saved_videos.count()})


@require_POST
def api_toggle_follow_match(request, match_id):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "auth_required", "redirect": "/connexion/"}, status=401)
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    match = get_object_or_404(FootballMatch, pk=match_id)
    if profile.followed_matches.filter(pk=match.pk).exists():
        profile.followed_matches.remove(match)
        followed = False
    else:
        profile.followed_matches.add(match)
        followed = True
    return JsonResponse({"status": "ok", "followed": followed, "count": profile.followed_matches.count()})


# ==============================================================================
# REAL-TIME LIVESCORE PULSE & GOAL NOTIFICATION ENDPOINTS
# ==============================================================================

def api_live_pulse(request):
    from .livescore_service import LiveScoreSyncService

    force_ext = request.GET.get("force_external") == "1"
    force_goal = request.GET.get("simulate_goal") == "1"
    provider_param = (request.GET.get("provider") or "").strip().upper() or None

    sync_info = LiveScoreSyncService.sync_or_tick(
        force_external=force_ext,
        force_goal_sim=force_goal,
        specific_provider=provider_param,
    )

    fav_club = ""
    alert_enabled = True
    if request.user.is_authenticated:
        prof = UserProfile.objects.filter(user=request.user).first()
        if prof:
            fav_club = prof.favorite_club or ""
            alert_enabled = prof.alert_mercato_foot

    matches = FootballMatch.objects.select_related("competition").all()
    matches_payload = [
        {
            "id": m.id,
            "home_team": m.home_team,
            "home_short": m.home_short,
            "away_team": m.away_team,
            "away_short": m.away_short,
            "home_score": m.home_score,
            "away_score": m.away_score,
            "status": m.status,
            "minute": m.minute,
            "home_shots": m.home_shots,
            "away_shots": m.away_shots,
            "home_shots_on_target": m.home_shots_on_target,
            "away_shots_on_target": m.away_shots_on_target,
            "home_xg": m.home_xg,
            "away_xg": m.away_xg,
        }
        for m in matches
    ]

    # Mark if any goal alert involves the logged-in user's favorite club
    for alert in sync_info["goal_alerts"]:
        is_fav = False
        if fav_club:
            fc_low = fav_club.lower()
            if fc_low in alert["home_team"].lower() or fc_low in alert["away_team"].lower():
                is_fav = True
        alert["is_favorite_club"] = is_fav

    return JsonResponse({
        "status": "ok",
        "source": sync_info["source"],
        "strategy": sync_info.get("strategy", "AUTO_CASCADE"),
        "synced_at": sync_info["synced_at"],
        "last_message": sync_info.get("last_message", ""),
        "quotas": sync_info.get("quotas", {}),
        "alert_enabled": alert_enabled,
        "favorite_club": fav_club,
        "goal_alerts": sync_info["goal_alerts"],
        "matches": matches_payload,
    })


@require_POST
def api_save_provider_config(request):
    config = LiveDataProviderConfig.get_solo()
    try:
        data = json.loads(request.body)
    except Exception:
        data = request.POST

    if "active_strategy" in data:
        config.active_strategy = data["active_strategy"]
    if "enable_espn_free" in data:
        config.enable_espn_free = bool(data["enable_espn_free"])
    if "enable_thesportsdb_free" in data:
        config.enable_thesportsdb_free = bool(data["enable_thesportsdb_free"])
    if "thesportsdb_key" in data:
        config.thesportsdb_key = (data["thesportsdb_key"] or "3").strip()
    if "enable_football_data_pro" in data:
        config.enable_football_data_pro = bool(data["enable_football_data_pro"])
    if "football_data_api_key" in data:
        config.football_data_api_key = data["football_data_api_key"].strip()
    if "enable_api_football_pro" in data:
        config.enable_api_football_pro = bool(data["enable_api_football_pro"])
    if "api_football_key" in data:
        config.api_football_key = data["api_football_key"].strip()
    if "enable_simulation_fallback" in data:
        config.enable_simulation_fallback = bool(data["enable_simulation_fallback"])

    config.save()
    return JsonResponse({
        "status": "ok",
        "message": "Configuration des connecteurs Score en direct enregistrée.",
        "active_strategy": config.get_active_strategy_display(),
    })


# ==============================================================================
# INDUSTRY STANDARDS: RSS WIRE SYNC, STUDIO Q&A, NOTIFICATIONS, STUDIO CMS & PWA
# ==============================================================================

@require_POST
def api_sync_rss_wires(request):
    from .news_rss_service import LiveNewsRssService

    imported = LiveNewsRssService.sync_latest_wires()
    wires = LiveNewsWire.objects.select_related("category").all()[:10]
    wires_data = [
        {
            "id": w.id,
            "time": w.created_at.strftime("%H:%M"),
            "title": w.title,
            "category": w.category.name,
            "source": w.source_name,
            "is_urgent": w.is_urgent,
            "external_url": w.external_url,
        }
        for w in wires
    ]
    return JsonResponse({
        "status": "ok",
        "imported": imported,
        "wires": wires_data,
    })


@require_POST
def api_submit_studio_question(request):
    try:
        data = json.loads(request.body)
    except Exception:
        data = request.POST

    user_name = (data.get("user_name") or "").strip()
    if not user_name and request.user.is_authenticated:
        user_name = request.user.first_name or request.user.username
    user_name = (user_name or "Spectateur Connecté")[:80]

    show_name = (data.get("show_name") or "Zely Live 24/7").strip()[:120]
    question_text = (data.get("question_text") or "").strip()[:350]
    if not question_text:
        return JsonResponse({"status": "error", "message": "Veuillez écrire votre question."}, status=400)

    handle = "@" + "".join(c for c in user_name.lower() if c.isalnum())[:16]
    sq = StudioQuestion.objects.create(
        user_name=user_name,
        user_handle=handle,
        show_name=show_name,
        question_text=question_text,
        upvotes=1,
    )
    if request.user.is_authenticated:
        UserProfile.objects.filter(user=request.user).update(reputation_points=F("reputation_points") + 15)

    return JsonResponse({
        "status": "ok",
        "question": {
            "id": sq.id,
            "user_name": sq.user_name,
            "user_handle": sq.user_handle,
            "show_name": sq.show_name,
            "question_text": sq.question_text,
            "upvotes": sq.upvotes,
        },
    })


@require_POST
def api_upvote_studio_question(request, question_id):
    sq = get_object_or_404(StudioQuestion, pk=question_id)
    StudioQuestion.objects.filter(pk=sq.pk).update(upvotes=F("upvotes") + 1)
    sq.refresh_from_db()
    return JsonResponse({"status": "ok", "upvotes": sq.upvotes})


@require_POST
def api_like_video(request, video_id):
    video = get_object_or_404(VideoItem, pk=video_id)
    VideoItem.objects.filter(pk=video.pk).update(likes_count=F("likes_count") + 1)
    video.refresh_from_db()
    return JsonResponse({"status": "ok", "likes_count": video.likes_count})


@require_POST
def api_mark_notifications_read(request):
    if request.user.is_authenticated:
        UserNotification.objects.filter(Q(user=request.user) | Q(user__isnull=True)).update(is_read=True)
    else:
        UserNotification.objects.filter(user__isnull=True).update(is_read=True)
    return JsonResponse({"status": "ok"})


def editorial_studio(request):
    """Newsroom & Broadcast Control Room ('Studio Rédaction & Régie Direct')."""
    categories = Category.objects.all()
    competitions = Competition.objects.all()
    matches = FootballMatch.objects.select_related("competition").all()[:8]
    studio_questions = StudioQuestion.objects.all()[:10]
    recent_wires = LiveNewsWire.objects.select_related("category").all()[:8]
    provider_config = LiveDataProviderConfig.get_solo()

    feedback = None
    if request.method == "POST":
        action = request.POST.get("studio_action")
        if action == "publish_flash":
            title = (request.POST.get("title") or "").strip()
            cat_id = request.POST.get("category_id")
            summary = (request.POST.get("summary") or "").strip()
            is_breaking = request.POST.get("is_breaking") == "on"
            if title and summary:
                cat = Category.objects.filter(pk=cat_id).first() or Category.objects.first()
                slug = slugify(title)[:45] + f"-{Article.objects.count() + 1}"
                art = Article.objects.create(
                    title=title,
                    slug=slug,
                    category=cat,
                    summary=summary,
                    content=summary + "\n\nDéveloppement complet par la rédaction Zely News en direct.",
                    image_url=request.POST.get("image_url") or "https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=1000&auto=format&fit=crop&q=80",
                    author_name=request.user.username if request.user.is_authenticated else "Rédaction Zely",
                    is_breaking=is_breaking,
                )
                LiveNewsWire.objects.create(
                    title=title,
                    category=cat,
                    source_name="Rédaction Zely",
                    is_urgent=is_breaking,
                )
                UserNotification.objects.create(
                    notif_type="BREAKING",
                    title=f"Flash Info : {title[:120]}",
                    link_url=f"/article/{art.slug}/",
                )
                feedback = f"Article & Dépêche « {title} » publiés en direct avec notification envoyée !"

        elif action == "publish_mercato":
            player_name = (request.POST.get("player_name") or "").strip()
            from_club = (request.POST.get("from_club") or "").strip()
            to_club = (request.POST.get("to_club") or "").strip()
            fee = (request.POST.get("transfer_fee") or "50 M€").strip()
            status = request.POST.get("status") or "ADVANCED"
            summary = (request.POST.get("summary") or "").strip()
            if player_name and from_club and to_club:
                MercatoTransfer.objects.create(
                    player_name=player_name,
                    from_club=from_club,
                    to_club=to_club,
                    transfer_fee=fee,
                    status=status,
                    reliability_score=90,
                    is_exclusive=True,
                    summary=summary or f"Accord imminent pour {player_name} vers {to_club}.",
                )
                UserNotification.objects.create(
                    notif_type="MERCATO",
                    title=f"EXCLU MERCATO : {player_name} ({from_club} → {to_club})",
                    link_url="/sport/",
                )
                feedback = f"Alerte Mercato « {player_name} » publiée en direct !"

        elif action == "answer_question":
            q_id = request.POST.get("question_id")
            reply_txt = (request.POST.get("host_reply") or "").strip()
            sq = StudioQuestion.objects.filter(pk=q_id).first()
            if sq and reply_txt:
                sq.is_answered_on_air = True
                sq.host_reply = reply_txt
                sq.save()
                feedback = f"Réponse à l'antenne enregistrée pour la question de {sq.user_name}."

    return render(request, "core/studio_cms.html", {
        "categories": categories,
        "competitions": competitions,
        "matches": matches,
        "studio_questions": studio_questions,
        "recent_wires": recent_wires,
        "provider_config": provider_config,
        "feedback": feedback,
    })


def pwa_manifest(request):
    manifest = {
        "name": "Zely News — Texte, Web TV, Score en direct & Citoyen",
        "short_name": "Zely News",
        "description": "Application d'actualités multi-domaines en modes Texte, Studio Web TV 24/7, Score en direct ZeMercato et Journalisme Participatif.",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#07090e",
        "theme_color": "#06b6d4",
        "orientation": "portrait-primary",
        "icons": [
            {
                "src": "https://cdn-icons-png.flaticon.com/512/2965/2965879.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any maskable",
            }
        ],
    }
    return JsonResponse(manifest)


def pwa_service_worker(request):
    sw_js = """
    const CACHE_NAME = 'zely-news-v2';
    self.addEventListener('install', (event) => {
        self.skipWaiting();
    });
    self.addEventListener('activate', (event) => {
        event.waitUntil(clients.claim());
    });
    self.addEventListener('fetch', (event) => {
        event.respondWith(
            fetch(event.request).catch(() => caches.match(event.request))
        );
    });
    """
    return HttpResponse(sw_js.strip(), content_type="application/javascript")





