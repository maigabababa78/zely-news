from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import (
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
    TopScorer,
    StudioQuestion,
    UserNotification,
    LiveNewsWire,
)


class Command(BaseCommand):
    help = "Populate Zely News database with initial categories, articles, Web TV streams, polls, and citizen reports."

    def handle(self, *args, **options):
        self.stdout.write("Initialisation des données Zely News...")

        # 1. Categories (4 main domains chosen by user)
        categories_data = [
            {
                "name": "Politique, Éco & Monde",
                "slug": "politique-economie-monde",
                "icon": "fa-landmark",
                "color": "#38bdf8",
                "badge_bg": "bg-sky-500/20 text-sky-300 border-sky-500/40",
                "description": "Géopolitique, marchés internationaux, grandes réformes et coulisses du pouvoir.",
            },
            {
                "name": "Tech, Science & IA",
                "slug": "tech-science-innovation",
                "icon": "fa-microchip",
                "color": "#a855f7",
                "badge_bg": "bg-purple-500/20 text-purple-300 border-purple-500/40",
                "description": "Intelligence artificielle, découvertes spatiales, transition énergétique et startups.",
            },
            {
                "name": "Culture, Cinéma & Musique",
                "slug": "culture-musique-cinema",
                "icon": "fa-masks-theater",
                "color": "#f43f5e",
                "badge_bg": "bg-rose-500/20 text-rose-300 border-rose-500/40",
                "description": "Sorties cinéma, festivals, tendances urbaines, littérature et création numérique.",
            },
            {
                "name": "Sport & eSport",
                "slug": "sport-esport",
                "icon": "fa-trophy",
                "color": "#10b981",
                "badge_bg": "bg-emerald-500/20 text-emerald-300 border-emerald-500/40",
                "description": "Ligue des Champions, grands tournois eSport, athlétisme et coulisses des clubs.",
            },
        ]

        cat_map = {}
        for cdata in categories_data:
            cat, _ = Category.objects.update_or_create(slug=cdata["slug"], defaults=cdata)
            cat_map[cdata["slug"]] = cat

        # 2. Articles
        articles_data = [
            {
                "title": "Sommet Mondial de l'IA Souveraine : l'Europe et l'Afrique lancent un réseau de supercalculateurs ouverts",
                "slug": "sommet-mondial-ia-souveraine-reseau-supercalculateurs",
                "category": cat_map["tech-science-innovation"],
                "summary": "Douze pays viennent de signer l'accord historique 'Horizon Neuronal' visant à mutualiser la puissance de calcul publique pour les chercheurs, startups et médias indépendants.",
                "content": (
                    "C'est un tournant majeur dans la gouvernance technologique mondiale. Réunis ce matin lors du Forum Zely Tech, les ministres du Numérique et les directeurs de laboratoires publics ont dévoilé une alliance inédite.\n\n"
                    "Concrètement, six nouveaux centres de calcul haute performance alimentés à 90% par des énergies décarbonées (géothermie et solaire thermique) seront interconnectés d'ici la fin de l'année.\n\n"
                    "« L'objectif est simple : permettre aux universités, aux hôpitaux et aux jeunes pousses locales d'entraîner des modèles scientifiques et linguistiques sans dépendre d'un monopole privé », explique la professeure Nadia Khelifi, coordinatrice du programme.\n\n"
                    "Sur notre plateau Web TV, les réactions des entrepreneurs sont enthousiastes, même si certains observateurs soulignent le défi du recrutement d'ingénieurs spécialisés pour maintenir ces infrastructures."
                ),
                "image_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1200&auto=format&fit=crop&q=80",
                "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
                "author_name": "Sarah Mansouri",
                "author_role": "Cheffe du pôle Tech & Futur",
                "reading_time": 5,
                "is_breaking": True,
                "is_featured": True,
                "views_count": 3420,
                "likes_count": 412,
                "fire_count": 289,
                "mindblown_count": 134,
            },
            {
                "title": "Transition Économique : pourquoi les monnaies numériques de banques centrales accélèrent les échanges régionaux",
                "slug": "transition-economique-monnaies-numeriques-echanges",
                "category": cat_map["politique-economie-monde"],
                "summary": "Les premiers bilans trimestriels montrent une baisse de 65% des frais de transfert transfrontaliers pour les PME grâce aux nouveaux corridors de paiement instantané.",
                "content": (
                    "Depuis six mois, plusieurs banques centrales expérimentent un pont de règlement instantané dédié au commerce réel. Les résultats dépassent les prévisions initiales.\n\n"
                    "Pour les petites et moyennes entreprises d'import-export, le délai de règlement est passé de quatre jours ouvrés à moins de huit secondes, avec une traçabilité complète.\n\n"
                    "Toutefois, le débat reste vif chez les citoyens : la protection de la vie privée dans les transactions du quotidien demeure la condition numéro un posée par les associations de consommateurs."
                ),
                "image_url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=1000&auto=format&fit=crop&q=80",
                "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
                "author_name": "Marc Delacroix",
                "author_role": "Éditorialiste Économie",
                "reading_time": 6,
                "is_breaking": True,
                "is_featured": False,
                "views_count": 2150,
                "likes_count": 195,
                "fire_count": 110,
                "mindblown_count": 42,
            },
            {
                "title": "Festival Ciné-Pulse : le cinéma interactif où le public vote pour la scène suivante fait salle comble",
                "slug": "festival-cine-pulse-cinema-interactif-vote-public",
                "category": cat_map["culture-musique-cinema"],
                "summary": "À mi-chemin entre le long-métrage d'auteur et l'expérience collective en direct, trois réalisateurs présentent des œuvres à embranchements multiples.",
                "content": (
                    "Imaginez une salle de 600 personnes munies de boîtiers lumineux où, à trois moments clés du film, la tension dramatique bascule selon le choix majoritaire des spectateurs.\n\n"
                    "Présenté en avant-première hier soir, le thriller 'Les Échos de Novembre' a offert une séance électrique. Deux salles situées dans deux villes différentes ont d'ailleurs abouti à deux dénouements opposés.\n\n"
                    "« Ce n'est pas un gadget, c'est un retour à l'essence du théâtre antique où le chœur et la cité vibrent avec les personnages », confie le réalisateur Idriss Sylla au micro de Zely TV."
                ),
                "image_url": "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=1000&auto=format&fit=crop&q=80",
                "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
                "author_name": "Léa Kovács",
                "author_role": "Critique Culture & Médias",
                "reading_time": 4,
                "is_breaking": False,
                "is_featured": False,
                "views_count": 1680,
                "likes_count": 260,
                "fire_count": 145,
                "mindblown_count": 88,
            },
            {
                "title": "Finale Mondiale d'eSport & Football Hybride : 45 000 spectateurs au stade et 4 millions en streaming",
                "slug": "finale-mondiale-esport-football-hybride-record-audience",
                "category": cat_map["sport-esport"],
                "summary": "Le nouveau format mêlant match sur pelouse réelle en première période et affrontement tactique sur simulateur en seconde période pulvérise tous les records d'audience.",
                "content": (
                    "On pensait les deux univers irréconciliables : ils viennent de signer le spectacle sportif le plus suivi du mois. Dans une arène comble, chaque club alignait onze joueurs sur le terrain et trois tacticiens eSport sur scène.\n\n"
                    "Les points cumulés des deux manches ont maintenu le suspense jusqu'à la dernière seconde, offrant une dramaturgie inédite pour les fans des deux générations."
                ),
                "image_url": "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=1000&auto=format&fit=crop&q=80",
                "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoy.mp4",
                "author_name": "Yanis Benali",
                "author_role": "Grand Reporter Sport & eSport",
                "reading_time": 4,
                "is_breaking": True,
                "is_featured": False,
                "views_count": 4190,
                "likes_count": 530,
                "fire_count": 390,
                "mindblown_count": 175,
            },
            {
                "title": "Fusion Nucléaire Compacte : un prototype civil atteint 18 minutes de plasma stable en laboratoire",
                "slug": "fusion-nucleaire-compacte-prototype-plasma-stable",
                "category": cat_map["tech-science-innovation"],
                "summary": "Grâce à de nouveaux aimants supraconducteurs à haute température, l'équipe internationale franchit un cap décisif vers la production nette d'électricité propre.",
                "content": (
                    "Dix-huit minutes et quarante secondes à plus de 100 millions de degrés Celsius. Le chiffre paraît technique, mais il représente un bond de géant pour la physique appliquée.\n\n"
                    "Les chercheurs ont utilisé un algorithme prédictif en temps réel pour stabiliser les turbulences magnétiques du plasma avant même qu'elles ne se forment."
                ),
                "image_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1000&auto=format&fit=crop&q=80",
                "video_url": "",
                "author_name": "Sarah Mansouri",
                "author_role": "Cheffe du pôle Tech & Futur",
                "reading_time": 5,
                "is_breaking": False,
                "is_featured": False,
                "views_count": 1920,
                "likes_count": 310,
                "fire_count": 205,
                "mindblown_count": 190,
            },
            {
                "title": "Trains de Nuit Nouvelle Génération : capsules silence, studios de travail et tarifs populaires",
                "slug": "trains-de-nuit-nouvelle-generation-capsules-europe",
                "category": cat_map["politique-economie-monde"],
                "summary": "Cinq nouvelles lignes transfrontalières entrent en service ce mois-ci avec des rames entièrement repensées pour concurrencer l'avion sur les trajets de 800 à 1 500 km.",
                "content": (
                    "Fini les compartiments exigus des années 1980 : les nouvelles rames offrent des mini-cabines individuelles dotées d'une isolation acoustique renforcée, d'un éclairage circadien et du Wi-Fi haut débit par satellite.\n\n"
                    "Avec un taux de remplissage déjà supérieur à 92% sur les réservations d'automne, le rail nocturne s'impose comme le symbole d'une mobilité bas-carbone désirable."
                ),
                "image_url": "https://images.unsplash.com/photo-1474487548417-781cb71495f3?w=1000&auto=format&fit=crop&q=80",
                "video_url": "",
                "author_name": "Marc Delacroix",
                "author_role": "Éditorialiste Économie",
                "reading_time": 3,
                "is_breaking": False,
                "is_featured": False,
                "views_count": 1450,
                "likes_count": 215,
                "fire_count": 98,
                "mindblown_count": 34,
            },
            {
                "title": "Scène Musicale : comment les concerts acoustiques dans les lieux patrimoniaux séduisent la génération Z",
                "slug": "concerts-acoustiques-lieux-patrimoniaux-generation-z",
                "category": cat_map["culture-musique-cinema"],
                "summary": "Bibliothèques historiques, anciens phares et jardins botaniques accueillent des sessions intimistes sans téléphones, filmées en 4K pour les absents.",
                "content": (
                    "Le paradoxe est fascinant : plus la musique se consomme en streaming rapide, plus le public jeune recherche des expériences physiques rares et intenses.\n\n"
                    "Le collectif 'Onde Pure' affiche complet en quelques minutes à chaque annonce secrète de lieu."
                ),
                "image_url": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=1000&auto=format&fit=crop&q=80",
                "video_url": "",
                "author_name": "Léa Kovács",
                "author_role": "Critique Culture & Médias",
                "reading_time": 4,
                "is_breaking": False,
                "is_featured": False,
                "views_count": 1180,
                "likes_count": 180,
                "fire_count": 92,
                "mindblown_count": 29,
            },
        ]

        created_articles = []
        for adata in articles_data:
            art, _ = Article.objects.update_or_create(slug=adata["slug"], defaults=adata)
            created_articles.append(art)

        # 3. Web TV Videos (LIVE, VOD, SHORTS)
        videos_data = [
            {
                "title": "LE GRAND DIRECT : Souveraineté Tech, Économie & Questions des Spectateurs",
                "slug": "grand-direct-souverainete-tech-economie",
                "category": cat_map["tech-science-innovation"],
                "video_type": "LIVE",
                "show_name": "Zely Live 24/7",
                "host_name": "Clara Vance & invités",
                "thumbnail_url": "https://images.unsplash.com/photo-1598387993441-a364f854c3e1?w=1000&auto=format&fit=crop&q=80",
                "stream_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
                "duration": "EN DIRECT",
                "viewers_count": 2845,
                "likes_count": 940,
                "is_live_now": True,
                "description": "Suivez notre plateau spécial en direct : décryptage des annonces technologiques et économiques de la journée, duplex avec nos correspondants et réponses en temps réel aux messages du chat citoyen.",
            },
            {
                "title": "Enquête : Dans les coulisses des nouveaux trains de nuit transfrontaliers",
                "slug": "enquete-coulisses-nouveaux-trains-de-nuit",
                "category": cat_map["politique-economie-monde"],
                "video_type": "VOD",
                "show_name": "Grand Angle Zely",
                "host_name": "Marc Delacroix",
                "thumbnail_url": "https://images.unsplash.com/photo-1515165562839-978bbcf18277?w=800&auto=format&fit=crop&q=80",
                "stream_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
                "duration": "18:24",
                "viewers_count": 12400,
                "likes_count": 1120,
                "is_live_now": False,
                "description": "Reportage exclusif à bord de la ligne inaugurale : interviews des ingénieurs ferroviaires et des voyageurs.",
            },
            {
                "title": "Le Débat Tech : Faut-il rendre open-source tous les modèles d'IA financés par l'État ?",
                "slug": "debat-tech-open-source-ia-publique",
                "category": cat_map["tech-science-innovation"],
                "video_type": "VOD",
                "show_name": "Futur & Société",
                "host_name": "Sarah Mansouri",
                "thumbnail_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800&auto=format&fit=crop&q=80",
                "stream_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
                "duration": "26:10",
                "viewers_count": 9850,
                "likes_count": 870,
                "is_live_now": False,
                "description": "Face-à-face entre chercheurs en sécurité informatique et entrepreneurs du logiciel libre.",
            },
            {
                "title": "Session Live & Interview : Les secrets du cinéma interactif au Festival Ciné-Pulse",
                "slug": "session-live-secrets-cinema-interactif",
                "category": cat_map["culture-musique-cinema"],
                "video_type": "VOD",
                "show_name": "Zely Culture Club",
                "host_name": "Léa Kovács",
                "thumbnail_url": "https://images.unsplash.com/photo-1514306191717-452ec28c7814?w=800&auto=format&fit=crop&q=80",
                "stream_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoy.mp4",
                "duration": "14:50",
                "viewers_count": 6420,
                "likes_count": 610,
                "is_live_now": False,
                "description": "Immersion dans la salle où les spectateurs votent en temps réel pour orienter l'intrigue.",
            },
            {
                "title": "Analyse Tactique : Comment la finale hybride Football/eSport a basculé à la 88e minute",
                "slug": "analyse-tactique-finale-hybride-football-esport",
                "category": cat_map["sport-esport"],
                "video_type": "VOD",
                "show_name": "L'Arène Sport",
                "host_name": "Yanis Benali",
                "thumbnail_url": "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=800&auto=format&fit=crop&q=80",
                "stream_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4",
                "duration": "11:15",
                "viewers_count": 15300,
                "likes_count": 1840,
                "is_live_now": False,
                "description": "Palette tactique complète et réactions dans les vestiaires après le sacre.",
            },
            # Vertical Shorts
            {
                "title": "60s pour comprendre la fusion nucléaire compacte",
                "slug": "short-60s-fusion-nucleaire",
                "category": cat_map["tech-science-innovation"],
                "video_type": "SHORT",
                "show_name": "Zely Short",
                "host_name": "Sarah M.",
                "thumbnail_url": "https://images.unsplash.com/photo-1507413245164-6160d8298b31?w=600&auto=format&fit=crop&q=80",
                "stream_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
                "duration": "0:58",
                "viewers_count": 18400,
                "likes_count": 2310,
                "is_live_now": False,
            },
            {
                "title": "L'ambiance folle dans l'arène eSport hier soir !",
                "slug": "short-ambiance-arene-esport",
                "category": cat_map["sport-esport"],
                "video_type": "SHORT",
                "show_name": "Zely Short",
                "host_name": "Yanis B.",
                "thumbnail_url": "https://images.unsplash.com/photo-1511512578047-dfb367046420?w=600&auto=format&fit=crop&q=80",
                "stream_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoy.mp4",
                "duration": "0:45",
                "viewers_count": 24100,
                "likes_count": 3890,
                "is_live_now": False,
            },
            {
                "title": "Visite express d'une cabine de train de nuit futuriste",
                "slug": "short-visite-cabine-train-nuit",
                "category": cat_map["politique-economie-monde"],
                "video_type": "SHORT",
                "show_name": "Zely Short",
                "host_name": "Marc D.",
                "thumbnail_url": "https://images.unsplash.com/photo-1532105956626-9569c03602f6?w=600&auto=format&fit=crop&q=80",
                "stream_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
                "duration": "0:52",
                "viewers_count": 14200,
                "likes_count": 1650,
                "is_live_now": False,
            },
            {
                "title": "3 films interactifs à voir absolument cet automne",
                "slug": "short-3-films-interactifs-automne",
                "category": cat_map["culture-musique-cinema"],
                "video_type": "SHORT",
                "show_name": "Zely Short",
                "host_name": "Léa K.",
                "thumbnail_url": "https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=600&auto=format&fit=crop&q=80",
                "stream_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
                "duration": "0:49",
                "viewers_count": 9800,
                "likes_count": 1120,
                "is_live_now": False,
            },
            {
                "title": "Pourquoi l'or et les métaux critiques bougent cette semaine",
                "slug": "short-or-metaux-critiques-semaine",
                "category": cat_map["politique-economie-monde"],
                "video_type": "SHORT",
                "show_name": "Zely Short",
                "host_name": "Marc D.",
                "thumbnail_url": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=600&auto=format&fit=crop&q=80",
                "stream_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4",
                "duration": "0:55",
                "viewers_count": 11600,
                "likes_count": 980,
                "is_live_now": False,
            },
            {
                "title": "Backstage : répétition acoustique dans une bibliothèque centenaire",
                "slug": "short-backstage-concert-bibliotheque",
                "category": cat_map["culture-musique-cinema"],
                "video_type": "SHORT",
                "show_name": "Zely Short",
                "host_name": "Léa K.",
                "thumbnail_url": "https://images.unsplash.com/photo-1507838153414-b4b713384a76?w=600&auto=format&fit=crop&q=80",
                "stream_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
                "duration": "0:41",
                "viewers_count": 8700,
                "likes_count": 1040,
                "is_live_now": False,
            },
        ]

        for vdata in videos_data:
            VideoItem.objects.update_or_create(slug=vdata["slug"], defaults=vdata)

        # 4. Interactive Polls
        if Poll.objects.count() == 0:
            p1 = Poll.objects.create(
                question="Faut-il investir massivement dans des supercalculateurs publics européens & africains pour l'IA ?",
                category=cat_map["tech-science-innovation"],
                article=created_articles[0],
                is_active=True,
            )
            PollOption.objects.create(poll=p1, text="Oui, c'est vital pour notre souveraineté", votes=184)
            PollOption.objects.create(poll=p1, text="Oui, mais uniquement avec garantie écologique", votes=96)
            PollOption.objects.create(poll=p1, text="Non, laissons le secteur privé innover", votes=38)

            p2 = Poll.objects.create(
                question="Quel format d'actualité préférez-vous sur Zely News au quotidien ?",
                category=cat_map["culture-musique-cinema"],
                is_active=True,
            )
            PollOption.objects.create(poll=p2, text="Le mode Hybride (Lire un article + Direct en PiP)", votes=245)
            PollOption.objects.create(poll=p2, text="Les articles de fond & débats écrits", votes=130)
            PollOption.objects.create(poll=p2, text="Les Zely Shorts (60s) & plateaux Web TV", votes=162)

        # 5. Comments & Debates
        if Comment.objects.count() == 0:
            Comment.objects.create(
                article=created_articles[0],
                user_name="Dr. Antoine V.",
                user_badge="Chercheur IA",
                stance="PRO",
                content="Excellente initiative ! En tant que chercheur universitaire, l'accès à des clusters de calcul publics va nous permettre de publier des modèles ouverts et auditables par tous.",
                upvotes=34,
            )
            Comment.objects.create(
                article=created_articles[0],
                user_name="Sonia_Tech",
                user_badge="Ingénieure Cloud",
                stance="CON",
                content="L'idée est bonne sur le papier, mais attention aux coûts de maintenance et au renouvellement des puces tous les 24 mois. Il faudra une gouvernance ultra agile.",
                upvotes=19,
            )
            Comment.objects.create(
                article=created_articles[0],
                user_name="Mehdi K.",
                user_badge="Lecteur Vérifié",
                stance="NEUTRAL",
                content="Le vrai sujet sera l'ouverture des données d'entraînement aux médias locaux et aux écoles d'ingénieurs.",
                upvotes=12,
            )

        # 6. Live Chat Messages
        if LiveChatMessage.objects.count() == 0:
            chat_seed = [
                ("Inès_75", "text-cyan-400", "Super clair le décryptage sur le plateau ce soir 👏"),
                ("Thomas_Lyon", "text-emerald-400", "Est-ce que les startups pourront demander un accès gratuit aux serveurs ?"),
                ("Kenza_M", "text-amber-400", "Je regarde le direct en mode PiP tout en lisant le dossier sur les trains de nuit, hyper fluide !"),
                ("Lucas_eSport", "text-purple-400", "À quelle heure commence le résumé vidéo de la finale eSport ?"),
                ("Clara_Studio", "text-pink-400", "Bienvenue à tous sur le chat Zely TV ! Posez vos questions, nous les affichons à l'écran."),
            ]
            for uname, ucolor, msg in chat_seed:
                LiveChatMessage.objects.create(user_name=uname, user_color=ucolor, message=msg)

        # 7. Citizen Journalism Reports
        if CitizenReport.objects.count() == 0:
            CitizenReport.objects.create(
                title="Inauguration de la nouvelle rame de train de nuit en gare centrale : affluence record",
                category=cat_map["politique-economie-monde"],
                location="Lyon Part-Dieu",
                reporter_name="Julien Morel",
                reporter_handle="@julien_rail",
                description="Je suis sur le quai D où la nouvelle rame vient d'entrer en gare. Des centaines de curieux visitent les cabines capsules, l'isolation phonique est impressionnante !",
                media_type="PHOTO",
                media_url="https://images.unsplash.com/photo-1515165562839-978bbcf18277?w=800&auto=format&fit=crop&q=80",
                is_verified=True,
                upvotes=48,
            )
            CitizenReport.objects.create(
                title="File d'attente géante devant le cinéma Odéon pour la séance interactive",
                category=cat_map["culture-musique-cinema"],
                location="Paris 6e",
                reporter_name="Amélie D.",
                reporter_handle="@amelie_cine",
                description="Plus de 300 personnes débattent déjà sur le trottoir de la fin qu'elles vont voter pendant la projection de 21h.",
                media_type="VIDEO",
                media_url="https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?w=800&auto=format&fit=crop&q=80",
                is_verified=True,
                upvotes=35,
            )
            CitizenReport.objects.create(
                title="Hackathon étudiant : 40 équipes connectées au nouveau réseau de calcul ouvert",
                category=cat_map["tech-science-innovation"],
                location="Campus Polytechnique",
                reporter_name="Rayane B.",
                reporter_handle="@rayane_dev",
                description="Nuit blanche sur le campus ! Les étudiants testent en direct un modèle météo haute résolution pour prévenir les crues locales.",
                media_type="PHOTO",
                media_url="https://images.unsplash.com/photo-1531482615713-2afd69097998?w=800&auto=format&fit=crop&q=80",
                is_verified=True,
                upvotes=62,
            )
            CitizenReport.objects.create(
                title="Écran géant installé sur la place publique pour le match retour eSport/Foot",
                category=cat_map["sport-esport"],
                location="Marseille, Vieux-Port",
                reporter_name="Sofiane T.",
                reporter_handle="@sofiane_om",
                description="Ambiance des grands soirs ! Les familles et les gamers sont réunis devant l'écran géant.",
                media_type="PHOTO",
                media_url="https://images.unsplash.com/photo-1511886929837-354d827aae26?w=800&auto=format&fit=crop&q=80",
                is_verified=True,
                upvotes=51,
            )

        # 8. Web TV Schedule (Grille des programmes interactive)
        if TVScheduleItem.objects.count() == 0:
            schedules = [
                (1, "07:00 - 10:00", "La Matinale Hybride", "Marc Delacroix", cat_map["politique-economie-monde"], False, True, "Le grand réveil de l'info : revue de presse internationale, marchés et appels des auditeurs."),
                (2, "12:30 - 14:00", "Zely Tech & Labo", "Sarah Mansouri", cat_map["tech-science-innovation"], False, True, "Démonstrations d'innovations en direct, IA souveraine et questions-réponses avec les chercheurs."),
                (3, "18:00 - 20:00", "Culture Pulse & Ciné", "Léa Kovács", cat_map["culture-musique-cinema"], False, True, "Sessions musicales acoustiques en studio et critiques cinéma interactives."),
                (4, "20:00 - 22:30", "LE GRAND DIRECT : Souveraineté & Société", "Clara Vance & invités", cat_map["tech-science-innovation"], True, True, "Le grand plateau du soir connecté au chat citoyen et aux reporters de terrain."),
                (5, "22:30 - 00:00", "L'Arène Sport & eSport", "Yanis Benali", cat_map["sport-esport"], False, True, "Débriefing tactique des matchs européens et des grands tournois eSport."),
            ]
            for order, slot, title, host, cat, on_air, inter, desc in schedules:
                TVScheduleItem.objects.create(
                    order=order,
                    time_slot=slot,
                    show_title=title,
                    host_name=host,
                    category=cat,
                    is_on_air=on_air,
                    is_interactive=inter,
                    description=desc,
                )

        # 9. Community Contributors Leaderboard
        if CommunityContributor.objects.count() == 0:
            contributors = [
                ("Rayane B.", "@rayane_dev", "Vérificateur & Reporter Tech", "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150&auto=format&fit=crop&q=80", 1420, 19, 64),
                ("Amélie D.", "@amelie_cine", "Ambassadrice Culture", "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&auto=format&fit=crop&q=80", 1185, 14, 52),
                ("Julien Morel", "@julien_rail", "Correspondant Mobilités", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80", 990, 11, 41),
                ("Dr. Antoine V.", "@antoine_ia", "Expert Débatteur", "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80", 875, 6, 78),
                ("Sofiane T.", "@sofiane_om", "Reporter Terrain Sport", "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=150&auto=format&fit=crop&q=80", 760, 9, 33),
            ]
            for name, handle, badge, avatar, pts, reps, debs in contributors:
                CommunityContributor.objects.create(
                    name=name,
                    handle=handle,
                    role_badge=badge,
                    avatar_url=avatar,
                    points=pts,
                    reports_count=reps,
                    debates_count=debs,
                )

        # 10. Default Admin Superuser for easy Studio testing
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@zelynews.tv", "zely2026")
            self.stdout.write(self.style.SUCCESS("Compte Studio Admin créé : identifiant 'admin' / mot de passe 'zely2026'"))

        # 11. LiveScore Competitions, Football Matches, Events, Standings & FootMercato Transfers
        if Competition.objects.count() == 0:
            c_ucl = Competition.objects.create(name="UEFA Champions League", slug="champions-league", country="Europe", flag_emoji="🇪🇺", order=1)
            c_l1 = Competition.objects.create(name="Ligue 1 McDonald's", slug="ligue-1", country="France", flag_emoji="🇫🇷", order=2)
            c_pl = Competition.objects.create(name="Premier League", slug="premier-league", country="Angleterre", flag_emoji="🏴󠁧󠁢󠁥󠁮󠁧󠁿", order=3)
            c_liga = Competition.objects.create(name="LaLiga EA Sports", slug="laliga", country="Espagne", flag_emoji="🇪🇸", order=4)
            c_can = Competition.objects.create(name="Qualifications CAN / Afrique", slug="afrique-can", country="Afrique", flag_emoji="🌍", order=5)

            # Match 1 (Featured UCL Live)
            m1 = FootballMatch.objects.create(
                competition=c_ucl,
                home_team="Paris Saint-Germain",
                home_short="PSG",
                home_badge_color="from-blue-700 to-red-600",
                away_team="Real Madrid",
                away_short="RMA",
                away_badge_color="from-indigo-500 to-purple-800",
                home_score=2,
                away_score=1,
                status="LIVE",
                minute="74'",
                stadium="Parc des Princes, Paris",
                tv_channel="Zely Sport 1 UHD",
                home_possession=56,
                away_possession=44,
                home_shots=16,
                away_shots=11,
                home_shots_on_target=7,
                away_shots_on_target=5,
                home_xg="2.14",
                away_xg="1.38",
                home_corners=8,
                away_corners=4,
                home_formation="4-3-3",
                away_formation="4-3-1-2",
                home_lineup="Donnarumma - Hakimi - Marquinhos - Pacho - Nuno Mendes - Vitinha - Zaïre-Emery - João Neves - Dembélé - Barcola - Doué",
                away_lineup="Courtois - Carvajal - Rüdiger - Militão - Mendy - Valverde - Tchouaméni - Camavinga - Bellingham - Mbappé - Vinícius Jr",
                votes_home=640,
                votes_draw=180,
                votes_away=520,
                is_featured_match=True,
            )
            MatchEvent.objects.create(match=m1, minute=14, event_type="GOAL", team_side="HOME", player_name="Bradley Barcola", detail="Passe de Achraf Hakimi")
            MatchEvent.objects.create(match=m1, minute=31, event_type="YELLOW", team_side="AWAY", player_name="Antonio Rüdiger", detail="Faute tactique")
            MatchEvent.objects.create(match=m1, minute=42, event_type="GOAL", team_side="AWAY", player_name="Kylian Mbappé", detail="Passe de Jude Bellingham")
            MatchEvent.objects.create(match=m1, minute=61, event_type="SUB", team_side="HOME", player_name="Désiré Doué", detail="Remplace Lee Kang-In")
            MatchEvent.objects.create(match=m1, minute=68, event_type="GOAL", team_side="HOME", player_name="Ousmane Dembélé", detail="Frappe enroulée 20m")

            # Match 2 (UCL Live)
            m2 = FootballMatch.objects.create(
                competition=c_ucl,
                home_team="FC Barcelone",
                home_short="BAR",
                home_badge_color="from-blue-800 to-rose-700",
                away_team="Bayern Munich",
                away_short="BAY",
                away_badge_color="from-red-600 to-red-900",
                home_score=3,
                away_score=1,
                status="LIVE",
                minute="81'",
                stadium="Estadi Olímpic Montjuïc",
                tv_channel="Zely Sport 2",
                home_possession=52,
                away_possession=48,
                home_shots=15,
                away_shots=13,
                home_shots_on_target=8,
                away_shots_on_target=5,
                home_xg="2.45",
                away_xg="1.52",
                home_corners=6,
                away_corners=7,
                home_formation="4-2-3-1",
                away_formation="4-2-3-1",
                home_lineup="Peña - Koundé - Cubarsí - Iñigo Martínez - Balde - Pedri - Casadó - Lamine Yamal - Dani Olmo - Raphinha - Lewandowski",
                away_lineup="Neuer - Guerreiro - Upamecano - Kim - Davies - Kimmich - Pavlović - Olise - Musiala - Gnabry - Harry Kane",
                votes_home=490,
                votes_draw=120,
                votes_away=380,
            )
            MatchEvent.objects.create(match=m2, minute=2, event_type="GOAL", team_side="HOME", player_name="Raphinha", detail="Passe de Pedri")
            MatchEvent.objects.create(match=m2, minute=18, event_type="GOAL", team_side="AWAY", player_name="Harry Kane", detail="Centre de Michael Olise")
            MatchEvent.objects.create(match=m2, minute=36, event_type="GOAL", team_side="HOME", player_name="Robert Lewandowski", detail="Passe de Lamine Yamal")
            MatchEvent.objects.create(match=m2, minute=56, event_type="GOAL", team_side="HOME", player_name="Lamine Yamal", detail="Exploit individuel")

            # Match 3 (Ligue 1 Live)
            m3 = FootballMatch.objects.create(
                competition=c_l1,
                home_team="Olympique de Marseille",
                home_short="OM",
                home_badge_color="from-sky-400 to-blue-600",
                away_team="AS Monaco",
                away_short="ASM",
                away_badge_color="from-red-500 to-rose-700",
                home_score=1,
                away_score=1,
                status="HT",
                minute="MT",
                stadium="Stade Vélodrome, Marseille",
                tv_channel="Zely Ligue 1",
                home_possession=58,
                away_possession=42,
                home_shots=9,
                away_shots=6,
                home_shots_on_target=4,
                away_shots_on_target=3,
                home_xg="1.10",
                away_xg="0.95",
                home_corners=5,
                away_corners=2,
                votes_home=320,
                votes_draw=140,
                votes_away=190,
            )
            MatchEvent.objects.create(match=m3, minute=22, event_type="GOAL", team_side="AWAY", player_name="Maghnes Akliouche", detail="Contre-attaque rapide")
            MatchEvent.objects.create(match=m3, minute=44, event_type="GOAL", team_side="HOME", player_name="Mason Greenwood", detail="Penalty transformé")

            # Match 4 (Premier League Finished)
            m4 = FootballMatch.objects.create(
                competition=c_pl,
                home_team="Arsenal FC",
                home_short="ARS",
                home_badge_color="from-red-600 to-rose-800",
                away_team="Manchester City",
                away_short="MCI",
                away_badge_color="from-sky-400 to-cyan-600",
                home_score=2,
                away_score=2,
                status="FT",
                minute="Terminé",
                stadium="Emirates Stadium, Londres",
                tv_channel="Zely Premier",
                home_possession=45,
                away_possession=55,
                home_shots=11,
                away_shots=18,
                home_shots_on_target=5,
                away_shots_on_target=7,
                home_xg="1.65",
                away_xg="2.05",
                votes_home=410,
                votes_draw=250,
                votes_away=430,
            )
            MatchEvent.objects.create(match=m4, minute=9, event_type="GOAL", team_side="AWAY", player_name="Erling Haaland", detail="Passe de Savinho")
            MatchEvent.objects.create(match=m4, minute=22, event_type="GOAL", team_side="HOME", player_name="Bukayo Saka", detail="Frappe croisée")
            MatchEvent.objects.create(match=m4, minute=45, event_type="GOAL", team_side="HOME", player_name="Gabriel Magalhães", detail="Tête sur corner")
            MatchEvent.objects.create(match=m4, minute=90, event_type="GOAL", team_side="AWAY", player_name="John Stones", detail="Égalisation à la dernière seconde")

            # Match 5 (Afrique CAN Upcoming)
            FootballMatch.objects.create(
                competition=c_can,
                home_team="Maroc",
                home_short="MAR",
                home_badge_color="from-red-600 to-emerald-700",
                away_team="Sénégal",
                away_short="SEN",
                away_badge_color="from-emerald-500 to-amber-500",
                home_score=0,
                away_score=0,
                status="UPCOMING",
                minute="21:00",
                stadium="Complexe Prince Moulay Abdellah, Rabat",
                tv_channel="Zely Afrique Direct",
                votes_home=540,
                votes_draw=210,
                votes_away=495,
            )

            # Match 6 (LaLiga Upcoming)
            FootballMatch.objects.create(
                competition=c_liga,
                home_team="Atlético de Madrid",
                home_short="ATM",
                home_badge_color="from-red-600 to-blue-800",
                away_team="Real Sociedad",
                away_short="RSO",
                away_badge_color="from-blue-500 to-sky-700",
                home_score=0,
                away_score=0,
                status="UPCOMING",
                minute="21:30",
                stadium="Riyadh Air Metropolitano",
                tv_channel="Zely Liga",
                votes_home=280,
                votes_draw=95,
                votes_away=110,
            )

            # League Standings (Champions League Phase de Ligue)
            standings_data = [
                (1, "Paris Saint-Germain", 7, 6, 0, 1, "+14", 18, "V V V D V"),
                (2, "FC Barcelone", 7, 6, 0, 1, "+13", 18, "V V V V D"),
                (3, "Arsenal FC", 7, 5, 2, 0, "+11", 17, "V N V V N"),
                (4, "Inter Milan", 7, 5, 1, 1, "+8", 16, "V V N V D"),
                (5, "Real Madrid", 7, 5, 0, 2, "+9", 15, "V D V V D"),
                (6, "Bayern Munich", 7, 4, 1, 2, "+7", 13, "V N D V D"),
                (7, "Manchester City", 7, 4, 1, 2, "+6", 13, "N V D V V"),
                (8, "AS Monaco", 7, 4, 1, 2, "+4", 13, "V D N V V"),
            ]
            for r, team, pl, w, d, l, gd, pts, form in standings_data:
                LeagueStanding.objects.create(
                    competition=c_ucl,
                    rank=r,
                    team_name=team,
                    played=pl,
                    won=w,
                    drawn=d,
                    lost=l,
                    goal_diff=gd,
                    points=pts,
                    form=form,
                )

        # 12. FootMercato Transfers & Exclusives
        if MercatoTransfer.objects.count() == 0:
            mercato_list = [
                {
                    "player_name": "Viktor Gyökeres",
                    "player_age": 26,
                    "player_position": "Avant-Centre (#9)",
                    "player_photo": "https://images.unsplash.com/photo-1517466787929-bc90951d0974?w=400&auto=format&fit=crop&q=80",
                    "from_club": "Sporting CP",
                    "to_club": "Paris Saint-Germain",
                    "transfer_fee": "85 M€ + 15 M€ bonus",
                    "contract_duration": "Contrat 5 ans (2031)",
                    "status": "ADVANCED",
                    "reliability_score": 92,
                    "is_exclusive": True,
                    "summary": "INFO ZELY MERCATO : Accord de principe trouvé entre la direction parisienne et l'entourage du buteur suédois après une réunion décisive à Lisbonne.",
                    "good_deal_votes": 642,
                    "overrated_votes": 118,
                },
                {
                    "player_name": "Florian Wirtz",
                    "player_age": 22,
                    "player_position": "Milieu Offensif (#10)",
                    "player_photo": "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=400&auto=format&fit=crop&q=80",
                    "from_club": "Bayer Leverkusen",
                    "to_club": "Real Madrid",
                    "transfer_fee": "120 M€",
                    "contract_duration": "Jusqu'en 2031",
                    "status": "OFFICIAL",
                    "reliability_score": 100,
                    "is_exclusive": False,
                    "summary": "C'est désormais officiel ! Le prodige allemand s'engage avec la Casa Blanca pour renforcer l'entrejeu madrilène dès l'ouverture du marché.",
                    "good_deal_votes": 890,
                    "overrated_votes": 95,
                },
                {
                    "player_name": "Rayan Cherki",
                    "player_age": 21,
                    "player_position": "Meneur de Jeu",
                    "player_photo": "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=400&auto=format&fit=crop&q=80",
                    "from_club": "Olympique Lyonnais",
                    "to_club": "Liverpool FC",
                    "transfer_fee": "38 M€",
                    "contract_duration": "Contrat jusqu'en 2030",
                    "status": "NEGOTIATION",
                    "reliability_score": 78,
                    "is_exclusive": True,
                    "summary": "Les Reds ont transmis une première offre écrite. Le joueur privilégie un projet offensif disputant le titre en Premier League.",
                    "good_deal_votes": 510,
                    "overrated_votes": 140,
                },
                {
                    "player_name": "Achraf Hakimi",
                    "player_age": 26,
                    "player_position": "Latéral Droit",
                    "player_photo": "https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=400&auto=format&fit=crop&q=80",
                    "from_club": "Paris Saint-Germain",
                    "to_club": "PSG (Prolongation)",
                    "transfer_fee": "Prolongation Majeure",
                    "contract_duration": "Prolongé jusqu'en 2030",
                    "status": "OFFICIAL",
                    "reliability_score": 100,
                    "is_exclusive": False,
                    "summary": "Le capitaine des Lions de l'Atlas scelle son avenir à Paris avec un nouveau contrat longue durée et un rôle central dans le vestiaire.",
                    "good_deal_votes": 945,
                    "overrated_votes": 32,
                },
                {
                    "player_name": "Jonathan David",
                    "player_age": 25,
                    "player_position": "Attaquant",
                    "player_photo": "https://images.unsplash.com/photo-1543326727-cf6c39e8f84c?w=400&auto=format&fit=crop&q=80",
                    "from_club": "LOSC Lille",
                    "to_club": "FC Barcelone",
                    "transfer_fee": "Libre (Prime 15 M€)",
                    "contract_duration": "Contrat 4 ans",
                    "status": "RUMOR",
                    "reliability_score": 68,
                    "is_exclusive": False,
                    "summary": "Le club catalan multiplie les prises de contact pour sécuriser l'attaquant canadien afin d'épauler Robert Lewandowski.",
                    "good_deal_votes": 480,
                    "overrated_votes": 115,
                },
                {
                    "player_name": "Maghnes Akliouche",
                    "player_age": 23,
                    "player_position": "Ailier Créatif",
                    "player_photo": "https://images.unsplash.com/photo-1518604666860-9ed391f76460?w=400&auto=format&fit=crop&q=80",
                    "from_club": "AS Monaco",
                    "to_club": "Manchester City",
                    "transfer_fee": "60 M€",
                    "contract_duration": "Négociations salariales",
                    "status": "ADVANCED",
                    "reliability_score": 84,
                    "is_exclusive": True,
                    "summary": "Pep Guardiola a validé le profil technique du Monégasque. Les discussions entre les deux clubs avancent rapidement.",
                    "good_deal_votes": 430,
                    "overrated_votes": 160,
                },
            ]
            for mdata in mercato_list:
                MercatoTransfer.objects.create(**mdata)

        # 13. Demo User Account ("karim") with pre-configured preferences & bookmarks
        if not User.objects.filter(username="karim").exists():
            u_karim = User.objects.create_user("karim", "karim@zelynews.tv", "zely2026", first_name="Karim")
            prof_karim = UserProfile.objects.create(
                user=u_karim,
                display_name="Karim L.",
                handle="@karim_zely",
                bio="Passionné de Tech, d'IA souveraine et grand supporter du PSG. Toujours en mode Hybride Web TV !",
                city="Lyon",
                favorite_club="Paris Saint-Germain",
                preferred_mode="HYBRID",
                reputation_points=580,
            )
            prof_karim.favorite_categories.set([cat_map["tech-science-innovation"], cat_map["sport-esport"]])
            prof_karim.favorite_competitions.set(Competition.objects.all()[:3])
            prof_karim.saved_articles.set(created_articles[:3])
            self.stdout.write(self.style.SUCCESS("Compte Membre Démo créé : identifiant 'karim' / mot de passe 'zely2026'"))

        # 14. Top Scorers (Buteurs & Passeurs LiveScore / FootMercato)
        if TopScorer.objects.count() == 0:
            c_ucl = Competition.objects.filter(slug="champions-league").first() or Competition.objects.first()
            if c_ucl:
                scorers_seed = [
                    (1, "Kylian Mbappé", "Real Madrid", 9, 3, 8, "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=150&auto=format&fit=crop&q=80"),
                    (2, "Robert Lewandowski", "FC Barcelone", 9, 2, 8, "https://images.unsplash.com/photo-1543326727-cf6c39e8f84c?w=150&auto=format&fit=crop&q=80"),
                    (3, "Ousmane Dembélé", "Paris Saint-Germain", 8, 5, 8, "https://images.unsplash.com/photo-1517466787929-bc90951d0974?w=150&auto=format&fit=crop&q=80"),
                    (4, "Harry Kane", "Bayern Munich", 8, 3, 8, "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=150&auto=format&fit=crop&q=80"),
                    (5, "Erling Haaland", "Manchester City", 7, 1, 8, "https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=150&auto=format&fit=crop&q=80"),
                    (6, "Bradley Barcola", "Paris Saint-Germain", 6, 4, 8, "https://images.unsplash.com/photo-1518604666860-9ed391f76460?w=150&auto=format&fit=crop&q=80"),
                ]
                for r, pname, club, g, a, mp, av in scorers_seed:
                    TopScorer.objects.create(
                        competition=c_ucl,
                        rank=r,
                        player_name=pname,
                        club_name=club,
                        goals=g,
                        assists=a,
                        matches_played=mp,
                        avatar_url=av,
                    )

        # 15. Studio Web TV Questions (Q&A Plateau)
        if StudioQuestion.objects.count() == 0:
            sq_seed = [
                ("Yasmine K.", "@yasmine_ia", "Zely Live 24/7", "Comment les universités africaines et européennes vont-elles se répartir le temps de calcul des nouveaux supercalculateurs ?", 47, True, "Un quota de 40% est garanti par traité aux laboratoires universitaires et projets open-source."),
                ("Romain_Foot", "@romain_psg", "L'Arène Sport & eSport", "Avec son doublé décisif et ses statistiques xG ce soir, Ousmane Dembélé est-il le favori numéro un du Ballon d'Or ?", 39, True, "Il est clairement dans le Top 3 européen sur les 6 derniers mois selon notre baromètre Zely Sport."),
                ("Chloé M.", "@chloe_eco", "La Matinale Hybride", "Quand les nouveaux trains de nuit capsules seront-ils disponibles sur l'axe Paris - Madrid - Casablanca ?", 28, False, ""),
                ("Nabil_Tech", "@nabil_dev", "Zely Tech & Labo", "Les startups pourront-elles soumettre leurs candidatures directement en ligne dès ce trimestre ?", 19, False, ""),
            ]
            for uname, uhandle, sname, qtxt, upv, ans, reply in sq_seed:
                StudioQuestion.objects.create(
                    user_name=uname,
                    user_handle=uhandle,
                    show_name=sname,
                    question_text=qtxt,
                    upvotes=upv,
                    is_answered_on_air=ans,
                    host_reply=reply,
                )

        # 16. Live 24/7 News Wires ("En Continu")
        if LiveNewsWire.objects.count() == 0:
            wires_seed = [
                ("Sommet IA Souveraine : signature officielle du traité d'interconnexion des 6 supercalculateurs", cat_map["tech-science-innovation"], "AFP / Zely Tech", True),
                ("Ligue des Champions : le PSG prend l'avantage face au Real Madrid au Parc des Princes (2-1)", cat_map["sport-esport"], "Zely Score en direct", True),
                ("ZeMercato : Viktor Gyökeres se rapproche d'un accord total avec le Paris Saint-Germain", cat_map["sport-esport"], "ZeMercato", True),
                ("Banques Centrales : baisse de 65% des coûts de transaction pour les PME exportatrices", cat_map["politique-economie-monde"], "Reuters / Zely Éco", False),
                ("Festival Ciné-Pulse : une nouvelle séance interactive ajoutée samedi soir face à la demande", cat_map["culture-musique-cinema"], "Zely Culture", False),
                ("Trains de nuit nouvelle génération : plus de 92% de taux de réservation pour l'automne", cat_map["politique-economie-monde"], "Zely Mobilités", False),
            ]
            for wtitle, wcat, wsrc, wurg in wires_seed:
                LiveNewsWire.objects.create(
                    title=wtitle,
                    category=wcat,
                    source_name=wsrc,
                    is_urgent=wurg,
                )

        # 17. Real-Time User Notifications
        if UserNotification.objects.count() == 0:
            notifs_seed = [
                ("BREAKING", "🚨 FLASH : L'Europe et l'Afrique lancent le réseau de supercalculateurs ouverts", "/article/sommet-mondial-ia-souveraine-reseau-supercalculateurs/"),
                ("GOAL", "⚽ BUUUUT ! Ousmane Dembélé (68') donne l'avantage au PSG face au Real Madrid (2-1)", "/sport/"),
                ("MERCATO", "🔥 EXCLU MERCATO : Accord de principe entre Viktor Gyökeres et le PSG (92% fiabilité)", "/sport/?mercato=ADVANCED"),
                ("TV", "📺 EN DIRECT : Rejoignez le Grand Direct Web TV et posez vos questions au plateau", "/webtv/"),
            ]
            for ntype, ntitle, nurl in notifs_seed:
                UserNotification.objects.create(
                    notif_type=ntype,
                    title=ntitle,
                    link_url=nurl,
                    is_read=False,
                )

        self.stdout.write(self.style.SUCCESS("Données Zely News initialisées avec succès !"))
