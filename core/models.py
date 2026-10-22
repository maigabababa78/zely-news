from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, default="fa-newspaper")
    color = models.CharField(max_length=30, default="#3b82f6")
    badge_bg = models.CharField(max_length=50, default="bg-blue-500/20 text-blue-400 border-blue-500/30")
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="articles")
    summary = models.TextField()
    content = models.TextField()
    image_url = models.URLField(max_length=500)
    video_url = models.URLField(max_length=500, blank=True, null=True)
    author_name = models.CharField(max_length=100)
    author_role = models.CharField(max_length=100, default="Rédaction Zely News")
    author_avatar = models.URLField(max_length=500, default="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80")
    reading_time = models.PositiveIntegerField(default=4)
    is_breaking = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=120)
    likes_count = models.PositiveIntegerField(default=24)
    fire_count = models.PositiveIntegerField(default=15)
    mindblown_count = models.PositiveIntegerField(default=8)
    key_points = models.TextField(
        blank=True,
        default="Synthèse vérifiée par la rédaction Zely News.\nImpact direct sur l'écosystème européen et international.\nDébat citoyen ouvert en bas d'article avec nos experts.",
        help_text="3 points clés (1 par ligne) affichés dans l'encadré 'L'Essentiel en 3 points'"
    )
    source_trust_score = models.PositiveIntegerField(default=98, help_text="Indice de vérification des sources en %")
    sources_label = models.CharField(max_length=200, default="Enquête Rédaction Zely • Sources croisées & Dépêches")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def key_points_list(self):
        return [line.strip() for line in self.key_points.splitlines() if line.strip()]

    def __str__(self):
        return self.title


class VideoItem(models.Model):
    VIDEO_TYPES = [
        ("LIVE", "Direct (Live Stream)"),
        ("VOD", "Replay / Émission VOD"),
        ("SHORT", "Format Court (Short / Reel)"),
    ]
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="videos")
    video_type = models.CharField(max_length=10, choices=VIDEO_TYPES, default="VOD")
    show_name = models.CharField(max_length=120, default="Le Grand Direct Zely")
    host_name = models.CharField(max_length=100, default="Clara Vance")
    thumbnail_url = models.URLField(max_length=500)
    stream_url = models.URLField(
        max_length=500,
        default="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"
    )
    duration = models.CharField(max_length=20, default="12:45")
    viewers_count = models.PositiveIntegerField(default=1420)
    likes_count = models.PositiveIntegerField(default=310)
    is_live_now = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-is_live_now", "-created_at"]

    def __str__(self):
        return f"[{self.video_type}] {self.title}"


class TVScheduleItem(models.Model):
    time_slot = models.CharField(max_length=30, help_text="Ex: 20:00 - 21:30")
    show_title = models.CharField(max_length=180)
    host_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="schedules")
    is_on_air = models.BooleanField(default=False)
    is_interactive = models.BooleanField(default=True, help_text="Indique si les spectateurs peuvent intervenir en direct")
    description = models.CharField(max_length=300, blank=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.time_slot} - {self.show_title}"


class Poll(models.Model):
    question = models.CharField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="polls")
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, blank=True, related_name="polls")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def total_votes(self):
        return sum(opt.votes for opt in self.options.all())

    def __str__(self):
        return self.question


class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=200)
    votes = models.PositiveIntegerField(default=0)

    def percentage(self):
        total = self.poll.total_votes()
        if total == 0:
            return 0
        return round((self.votes / total) * 100)

    def __str__(self):
        return f"{self.text} ({self.votes})"


class Comment(models.Model):
    STANCE_CHOICES = [
        ("NEUTRAL", "Analyse / Avis"),
        ("PRO", "D'accord / Pour"),
        ("CON", "Nuance / Contre"),
    ]
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    user_name = models.CharField(max_length=80)
    user_badge = models.CharField(max_length=50, default="Lecteur Vérifié")
    stance = models.CharField(max_length=15, choices=STANCE_CHOICES, default="NEUTRAL")
    content = models.TextField()
    upvotes = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-upvotes", "-created_at"]

    def __str__(self):
        return f"{self.user_name} sur {self.article.title}"


class LiveChatMessage(models.Model):
    user_name = models.CharField(max_length=80)
    user_color = models.CharField(max_length=30, default="text-cyan-400")
    user_badge = models.CharField(max_length=40, blank=True, default="")
    message = models.CharField(max_length=400)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user_name}: {self.message[:30]}"


class CitizenReport(models.Model):
    MEDIA_TYPES = [
        ("VIDEO", "Témoignage Vidéo"),
        ("PHOTO", "Photo sur le vif"),
        ("TEXT", "Alerte / Info Locale"),
    ]
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="citizen_reports")
    location = models.CharField(max_length=120)
    reporter_name = models.CharField(max_length=80)
    reporter_handle = models.CharField(max_length=60, default="@citoyen_zely")
    description = models.TextField()
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default="PHOTO")
    media_url = models.URLField(
        max_length=500,
        blank=True,
        default="https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=800&auto=format&fit=crop&q=80"
    )
    is_verified = models.BooleanField(default=True)
    upvotes = models.PositiveIntegerField(default=12)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.location})"


class CommunityContributor(models.Model):
    name = models.CharField(max_length=80)
    handle = models.CharField(max_length=60)
    role_badge = models.CharField(max_length=80, default="Grand Reporter Citoyen")
    avatar_url = models.URLField(max_length=500)
    points = models.PositiveIntegerField(default=450)
    reports_count = models.PositiveIntegerField(default=8)
    debates_count = models.PositiveIntegerField(default=24)

    class Meta:
        ordering = ["-points"]

    def __str__(self):
        return f"{self.name} ({self.points} pts)"


# ==============================================================================
# SPORT, FOOTBALL LIVESCORE & MERCATO MODELS (LiveScore + FootMercato Inspired)
# ==============================================================================

class Competition(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    country = models.CharField(max_length=60, default="Europe")
    flag_emoji = models.CharField(max_length=20, default="🇪🇺")
    badge_color = models.CharField(max_length=60, default="bg-emerald-500/20 text-emerald-400 border-emerald-500/30")
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.flag_emoji} {self.name}"


class FootballMatch(models.Model):
    STATUS_CHOICES = [
        ("LIVE", "En Direct"),
        ("HT", "Mi-Temps"),
        ("FT", "Terminé"),
        ("UPCOMING", "À Venir"),
    ]
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="matches")
    home_team = models.CharField(max_length=80)
    home_short = models.CharField(max_length=10, default="HOM")
    home_badge_color = models.CharField(max_length=40, default="from-blue-600 to-indigo-800")
    away_team = models.CharField(max_length=80)
    away_short = models.CharField(max_length=10, default="AWY")
    away_badge_color = models.CharField(max_length=40, default="from-red-600 to-rose-800")

    home_score = models.PositiveIntegerField(default=0)
    away_score = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="LIVE")
    minute = models.CharField(max_length=15, default="67'", help_text="Ex: 67', MT, Terminé, 21:00")
    stadium = models.CharField(max_length=100, default="Arena Stadium")
    tv_channel = models.CharField(max_length=80, default="Zely Sport Live")
    stream_url = models.URLField(
        max_length=500,
        blank=True,
        default="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"
    )

    # Detailed Match Stats (LiveScore style)
    home_possession = models.PositiveIntegerField(default=54)
    away_possession = models.PositiveIntegerField(default=46)
    home_shots = models.PositiveIntegerField(default=14)
    away_shots = models.PositiveIntegerField(default=9)
    home_shots_on_target = models.PositiveIntegerField(default=6)
    away_shots_on_target = models.PositiveIntegerField(default=4)
    home_xg = models.CharField(max_length=10, default="1.85")
    away_xg = models.CharField(max_length=10, default="1.12")
    home_corners = models.PositiveIntegerField(default=7)
    away_corners = models.PositiveIntegerField(default=3)

    # Tactical Formations (4-3-3, etc.)
    home_formation = models.CharField(max_length=20, default="4-3-3")
    away_formation = models.CharField(max_length=20, default="4-2-3-1")
    home_lineup = models.TextField(
        default="Donnarumma - Hakimi, Marquinhos, Pacho, Nuno Mendes - Vitinha, Zaïre-Emery, João Neves - Dembélé, Barcola, Doué",
        help_text="Titulaires domicile"
    )
    away_lineup = models.TextField(
        default="Courtois - Carvajal, Rüdiger, Militão, Mendy - Valverde, Tchouaméni, Bellingham - Rodrygo, Mbappé, Vinícius Jr",
        help_text="Titulaires extérieur"
    )

    # Community 1N2 Pronostics
    votes_home = models.PositiveIntegerField(default=142)
    votes_draw = models.PositiveIntegerField(default=48)
    votes_away = models.PositiveIntegerField(default=110)

    is_featured_match = models.BooleanField(default=False)

    class Meta:
        ordering = ["competition__order", "-is_featured_match", "id"]

    def total_prono_votes(self):
        return self.votes_home + self.votes_draw + self.votes_away

    def home_win_pct(self):
        t = self.total_prono_votes()
        return round((self.votes_home / t) * 100) if t else 33

    def draw_pct(self):
        t = self.total_prono_votes()
        return round((self.votes_draw / t) * 100) if t else 34

    def away_win_pct(self):
        t = self.total_prono_votes()
        return max(0, 100 - self.home_win_pct() - self.draw_pct()) if t else 33

    def __str__(self):
        return f"{self.home_team} {self.home_score}-{self.away_score} {self.away_team} ({self.minute})"


class MatchEvent(models.Model):
    EVENT_TYPES = [
        ("GOAL", "⚽ But"),
        ("YELLOW", "🟨 Carton Jaune"),
        ("RED", "🟥 Carton Rouge"),
        ("SUB", "🔄 Remplacement"),
        ("VAR", "🖥️ Décision VAR"),
    ]
    TEAM_SIDE = [
        ("HOME", "Domicile"),
        ("AWAY", "Extérieur"),
    ]
    match = models.ForeignKey(FootballMatch, on_delete=models.CASCADE, related_name="events")
    minute = models.PositiveIntegerField(default=15)
    event_type = models.CharField(max_length=10, choices=EVENT_TYPES, default="GOAL")
    team_side = models.CharField(max_length=10, choices=TEAM_SIDE, default="HOME")
    player_name = models.CharField(max_length=80)
    detail = models.CharField(max_length=120, blank=True, help_text="Passeur décisif, joueur remplacé ou motif")

    class Meta:
        ordering = ["minute"]

    def __str__(self):
        return f"{self.minute}' {self.get_event_type_display()} - {self.player_name}"


class MercatoTransfer(models.Model):
    STATUS_CHOICES = [
        ("OFFICIAL", "Officiel ✅"),
        ("ADVANCED", "Accord proche 🔥"),
        ("NEGOTIATION", "Négociations ⏳"),
        ("RUMOR", "Rumeur Mercato 👀"),
    ]
    player_name = models.CharField(max_length=100)
    player_age = models.PositiveIntegerField(default=23)
    player_position = models.CharField(max_length=50, default="Attaquant")
    player_photo = models.URLField(
        max_length=500,
        default="https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=400&auto=format&fit=crop&q=80"
    )
    from_club = models.CharField(max_length=80)
    to_club = models.CharField(max_length=80)
    transfer_fee = models.CharField(max_length=60, default="65 M€ + bonus")
    contract_duration = models.CharField(max_length=50, default="Jusqu'en 2030")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="ADVANCED")
    reliability_score = models.PositiveIntegerField(default=85, help_text="Indice de fiabilité en % (0-100)")
    is_exclusive = models.BooleanField(default=False, help_text="Badge EXCLU ZELY MERCATO")
    summary = models.TextField()

    # Fan Community Approval ("Bon coup" vs "Surcoté")
    good_deal_votes = models.PositiveIntegerField(default=88)
    overrated_votes = models.PositiveIntegerField(default=24)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-is_exclusive", "-created_at"]

    def total_fan_votes(self):
        return self.good_deal_votes + self.overrated_votes

    def good_deal_pct(self):
        t = self.total_fan_votes()
        return round((self.good_deal_votes / t) * 100) if t else 50

    def overrated_pct(self):
        t = self.total_fan_votes()
        return 100 - self.good_deal_pct() if t else 50

    def __str__(self):
        return f"{self.player_name}: {self.from_club} -> {self.to_club} ({self.transfer_fee})"


class LeagueStanding(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="standings")
    rank = models.PositiveIntegerField(default=1)
    team_name = models.CharField(max_length=80)
    played = models.PositiveIntegerField(default=10)
    won = models.PositiveIntegerField(default=7)
    drawn = models.PositiveIntegerField(default=2)
    lost = models.PositiveIntegerField(default=1)
    goal_diff = models.CharField(max_length=10, default="+15")
    points = models.PositiveIntegerField(default=23)
    form = models.CharField(max_length=20, default="V V N V V", help_text="5 derniers matchs")

    class Meta:
        ordering = ["competition", "rank"]

    def form_list(self):
        return self.form.split()

    def __str__(self):
        return f"{self.rank}. {self.team_name} ({self.points} pts)"


# ==============================================================================
# USER PROFILE, PREFERENCES & PERSONALIZED ENGAGEMENT SPACE
# ==============================================================================

class UserProfile(models.Model):
    MODE_CHOICES = [
        ("HYBRID", "Mode Hybride (Texte + Web TV PiP)"),
        ("TEXT", "Mode Lecture Focus (Articles & Débats)"),
        ("WEBTV", "Mode Studio Web TV & Shorts"),
        ("SPORT", "Mode Foot Score en direct & ZeMercato"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    display_name = models.CharField(max_length=80, blank=True)
    handle = models.CharField(max_length=60, default="@membre_zely")
    bio = models.TextField(blank=True, default="Passionné d'actualité, de débats citoyens et de direct sur Zely News.")
    city = models.CharField(max_length=80, blank=True, default="Paris")
    avatar_url = models.URLField(
        max_length=500,
        default="https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=200&auto=format&fit=crop&q=80"
    )
    role_badge = models.CharField(max_length=60, default="Membre Connecté Zely")
    reputation_points = models.PositiveIntegerField(default=150)

    # Personalization & Preferences
    favorite_categories = models.ManyToManyField(Category, blank=True, related_name="interested_users")
    favorite_competitions = models.ManyToManyField(Competition, blank=True, related_name="fan_users")
    favorite_club = models.CharField(max_length=80, blank=True, default="Paris Saint-Germain")
    preferred_mode = models.CharField(max_length=15, choices=MODE_CHOICES, default="HYBRID")

    # Saved Content / Watchlist
    saved_articles = models.ManyToManyField(Article, blank=True, related_name="saved_by_users")
    saved_videos = models.ManyToManyField(VideoItem, blank=True, related_name="saved_by_users")
    followed_matches = models.ManyToManyField(FootballMatch, blank=True, related_name="followed_by_users")

    # Notification & Playback Toggles
    alert_breaking_news = models.BooleanField(default=True)
    alert_live_tv = models.BooleanField(default=True)
    alert_mercato_foot = models.BooleanField(default=True)
    autoplay_pip = models.BooleanField(default=True)

    created_at = models.DateTimeField(default=timezone.now)

    def get_name(self):
        return self.display_name or self.user.first_name or self.user.username

    def level_title(self):
        if self.reputation_points >= 1000:
            return "Ambassadeur & Grand Reporter Zely"
        if self.reputation_points >= 500:
            return "Analyste & Reporter Vérifié"
        if self.reputation_points >= 250:
            return "Débatteur Actif"
        return "Membre Connecté Zely"

    def __str__(self):
        return f"Profil de {self.user.username} ({self.reputation_points} pts)"


# ==============================================================================
# LIVE DATA PROVIDERS CONFIGURATION & QUOTA TRACKING
# ==============================================================================

class LiveDataProviderConfig(models.Model):
    STRATEGY_CHOICES = [
        ("AUTO_CASCADE", "Cascade Intelligente (Pro Gratuit -> Gratuit Sans Clé -> Simulation)"),
        ("PRO_FIRST", "Priorité Pro (API-Football & Football-Data.org)"),
        ("FREE_ONLY", "100% Gratuit Sans Clé (ESPN Live + TheSportsDB)"),
        ("SIMULATION", "Simulateur Temps Réel Continu (Démo 24/7)"),
    ]
    active_strategy = models.CharField(max_length=25, choices=STRATEGY_CHOICES, default="AUTO_CASCADE")

    # 1. Free Unlimited Providers (No API Key Needed)
    enable_espn_free = models.BooleanField(default=True, help_text="ESPN Hidden Public API (Illimité, sans clé)")
    enable_thesportsdb_free = models.BooleanField(default=True, help_text="TheSportsDB Public API v1 (Clé publique '3' incluse)")
    thesportsdb_key = models.CharField(max_length=50, default="3", blank=True)

    # 2. Best Pro Providers with Generous Free Plans
    enable_football_data_pro = models.BooleanField(default=True, help_text="Football-Data.org (Plan Gratuit: 10 req/min sur 12 grandes ligues)")
    football_data_api_key = models.CharField(max_length=120, blank=True, default="", help_text="Clé X-Auth-Token Football-Data.org")

    enable_api_football_pro = models.BooleanField(default=True, help_text="API-Football v3 (Plan Gratuit: 100 req/jour sur +1000 ligues)")
    api_football_key = models.CharField(max_length=120, blank=True, default="", help_text="Clé x-apisports-key API-Football")

    # 3. Real-Time Simulation Fallback (Disabled by default so only real scores are shown)
    enable_simulation_fallback = models.BooleanField(default=False, help_text="Fait évoluer les minutes et buts si aucun match réel n'est en cours")

    # Telemetry & Quota Tracking
    api_football_calls_today = models.PositiveIntegerField(default=0)
    football_data_calls_today = models.PositiveIntegerField(default=0)
    espn_calls_today = models.PositiveIntegerField(default=0)
    thesportsdb_calls_today = models.PositiveIntegerField(default=0)
    last_active_source = models.CharField(max_length=80, default="ESPN_PUBLIC_FREE")
    last_sync_at = models.DateTimeField(null=True, blank=True)
    last_sync_message = models.CharField(max_length=250, default="Prêt pour la synchronisation multi-sources.")

    class Meta:
        verbose_name = "Configuration API Temps Réel"
        verbose_name_plural = "Configurations API Temps Réel"

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return f"Connecteur Score en direct ({self.get_active_strategy_display()})"


# ==============================================================================
# INDUSTRY STANDARDS EXPANSION: TOP SCORERS, NOTIFICATIONS, STUDIO Q&A & WIRES
# ==============================================================================

class TopScorer(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="top_scorers")
    rank = models.PositiveIntegerField(default=1)
    player_name = models.CharField(max_length=100)
    club_name = models.CharField(max_length=80)
    goals = models.PositiveIntegerField(default=10)
    assists = models.PositiveIntegerField(default=4)
    matches_played = models.PositiveIntegerField(default=9)
    avatar_url = models.URLField(
        max_length=500,
        default="https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=150&auto=format&fit=crop&q=80"
    )

    class Meta:
        ordering = ["competition", "rank", "-goals"]

    def __str__(self):
        return f"{self.rank}. {self.player_name} ({self.goals} buts)"


class StudioQuestion(models.Model):
    user_name = models.CharField(max_length=80)
    user_handle = models.CharField(max_length=60, default="@spectateur_zely")
    show_name = models.CharField(max_length=120, default="Zely Live 24/7")
    question_text = models.CharField(max_length=350)
    upvotes = models.PositiveIntegerField(default=5)
    is_answered_on_air = models.BooleanField(default=False)
    host_reply = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-is_answered_on_air", "-upvotes", "-created_at"]

    def __str__(self):
        return f"Q plateau de {self.user_name}: {self.question_text[:40]}"


class UserNotification(models.Model):
    NOTIF_TYPES = [
        ("BREAKING", "🚨 Flash Breaking News"),
        ("GOAL", "⚽ Alerte But Score en direct"),
        ("MERCATO", "🔥 Exclu ZeMercato"),
        ("TV", "📺 Direct Web TV"),
        ("COMMUNITY", "💬 Débat & Communauté"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="notifications")
    notif_type = models.CharField(max_length=15, choices=NOTIF_TYPES, default="BREAKING")
    title = models.CharField(max_length=200)
    link_url = models.CharField(max_length=250, default="/")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.notif_type}] {self.title}"


class LiveNewsWire(models.Model):
    """24/7 chronological news wire ('Fil Continu') synced from RSS or Newsroom."""
    title = models.CharField(max_length=260)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="wires")
    source_name = models.CharField(max_length=80, default="AFP / Zely Fil Info")
    external_url = models.URLField(max_length=500, blank=True, default="")
    is_urgent = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.created_at.strftime('%H:%M')}] {self.title}"




