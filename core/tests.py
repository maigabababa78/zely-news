from django.test import TestCase, Client
from django.urls import reverse
from .models import Category, Article, Poll, PollOption, VideoItem, Competition, FootballMatch, MercatoTransfer


class ZelyNewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.cat = Category.objects.create(name="Sport & eSport", slug="sport-esport")
        self.article = Article.objects.create(
            title="Test Article",
            slug="test-article",
            category=self.cat,
            summary="Résumé test",
            content="Contenu complet",
            image_url="https://example.com/img.jpg",
            author_name="Tester",
        )
        self.video = VideoItem.objects.create(
            title="Live Test",
            slug="live-test",
            category=self.cat,
            video_type="LIVE",
            thumbnail_url="https://example.com/thumb.jpg",
            is_live_now=True,
        )
        self.poll = Poll.objects.create(question="Test Poll?", category=self.cat, article=self.article)
        self.opt = PollOption.objects.create(poll=self.poll, text="Oui", votes=5)

        self.comp = Competition.objects.create(name="Champions League", slug="ucl")
        self.match = FootballMatch.objects.create(
            competition=self.comp,
            home_team="PSG",
            home_short="PSG",
            away_team="Real Madrid",
            away_short="RMA",
            home_score=2,
            away_score=1,
            status="LIVE",
        )
        self.transfer = MercatoTransfer.objects.create(
            player_name="Kylian Test",
            from_club="Club A",
            to_club="Club B",
            transfer_fee="80 M€",
            summary="Mercato test",
        )

    def test_pages_render(self):
        self.assertEqual(self.client.get(reverse("home")).status_code, 200)
        self.assertEqual(self.client.get(reverse("article_detail", args=[self.article.slug])).status_code, 200)
        self.assertEqual(self.client.get(reverse("webtv_hub")).status_code, 200)
        self.assertEqual(self.client.get(reverse("sport_hub")).status_code, 200)
        self.assertEqual(self.client.get(reverse("match_detail", args=[self.match.id])).status_code, 200)
        self.assertEqual(self.client.get(reverse("community_hub")).status_code, 200)
        self.assertEqual(self.client.get(reverse("editorial_studio")).status_code, 200)
        self.assertEqual(self.client.get(reverse("pwa_manifest")).status_code, 200)
        self.assertEqual(self.client.get(reverse("pwa_service_worker")).status_code, 200)

    def test_interactive_apis(self):
        # Poll vote
        res = self.client.post(
            reverse("api_vote_poll", args=[self.poll.id]),
            data='{"option_id": %d}' % self.opt.id,
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 200)
        self.opt.refresh_from_db()
        self.assertEqual(self.opt.votes, 6)

        # Comment debate
        res2 = self.client.post(
            reverse("api_add_comment", args=[self.article.id]),
            data='{"user_name": "Alice", "stance": "PRO", "content": "Bravo"}',
            content_type="application/json",
        )
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(self.article.comments.count(), 1)

        # Match detail & 1N2 Prono API
        res3 = self.client.get(reverse("api_match_detail", args=[self.match.id]))
        self.assertEqual(res3.status_code, 200)

        res4 = self.client.post(
            reverse("api_vote_match_prono", args=[self.match.id]),
            data='{"choice": "1"}',
            content_type="application/json",
        )
        self.assertEqual(res4.status_code, 200)

        # Mercato vote API
        res5 = self.client.post(
            reverse("api_vote_mercato", args=[self.transfer.id]),
            data='{"verdict": "good"}',
            content_type="application/json",
        )
        self.assertEqual(res5.status_code, 200)

    def test_user_auth_and_preferences(self):
        # Register new user
        res_reg = self.client.post(
            reverse("register"),
            {
                "username": "testuser",
                "display_name": "Test User",
                "password": "secretpassword",
                "city": "Marseille",
                "favorite_club": "OM",
                "preferred_mode": "SPORT",
            },
        )
        self.assertEqual(res_reg.status_code, 302)  # Redirects to dashboard

        # Access dashboard and all 5 dedicated profile pages
        res_dash = self.client.get(reverse("user_dashboard"))
        self.assertEqual(res_dash.status_code, 200)
        for sec in ["flux", "sport", "favoris", "contributions", "parametres"]:
            res_sec = self.client.get(reverse("user_dashboard_section", args=[sec]))
            self.assertEqual(res_sec.status_code, 200)

        # Toggle bookmark article
        res_bm = self.client.post(reverse("api_toggle_bookmark_article", args=[self.article.id]))
        self.assertEqual(res_bm.status_code, 200)
        self.assertTrue(res_bm.json()["saved"])

        # Update preferences API
        res_pref = self.client.post(
            reverse("api_update_preferences"),
            data='{"display_name": "Updated User", "favorite_club": "PSG", "category_ids": [%d]}' % self.cat.id,
            content_type="application/json",
        )
        self.assertEqual(res_pref.status_code, 200)

        # Real-time live pulse & goal alert simulation
        res_pulse = self.client.get(reverse("api_live_pulse") + "?simulate_goal=1")
        self.assertEqual(res_pulse.status_code, 200)
        data_pulse = res_pulse.json()
        self.assertEqual(data_pulse["status"], "ok")
        self.assertTrue(len(data_pulse["goal_alerts"]) >= 1)

        # Save multi-provider config API
        res_prov = self.client.post(
            reverse("api_save_provider_config"),
            data='{"active_strategy": "AUTO_CASCADE", "enable_espn_free": true, "thesportsdb_key": "3"}',
            content_type="application/json",
        )
        self.assertEqual(res_prov.status_code, 200)
        self.assertEqual(res_prov.json()["status"], "ok")

        # Studio Q&A submit and upvote
        res_sq = self.client.post(
            reverse("api_submit_studio_question"),
            data='{"user_name": "Karim", "show_name": "Zely Live", "question_text": "Quel avenir pour l IA ?"}',
            content_type="application/json",
        )
        self.assertEqual(res_sq.status_code, 200)
        sq_id = res_sq.json()["question"]["id"]

        res_sq_up = self.client.post(reverse("api_upvote_studio_question", args=[sq_id]))
        self.assertEqual(res_sq_up.status_code, 200)
        self.assertEqual(res_sq_up.json()["upvotes"], 2)

        # Video like & notifications read
        res_vlike = self.client.post(reverse("api_like_video", args=[self.video.id]))
        self.assertEqual(res_vlike.status_code, 200)

        res_nread = self.client.post(reverse("api_mark_notifications_read"))
        self.assertEqual(res_nread.status_code, 200)

        # Editorial studio POST publish flash
        res_studio = self.client.post(
            reverse("editorial_studio"),
            {
                "studio_action": "publish_flash",
                "title": "Flash Test Studio",
                "category_id": self.cat.id,
                "summary": "Résumé flash test",
                "is_breaking": "on",
            },
        )
        self.assertEqual(res_studio.status_code, 200)



