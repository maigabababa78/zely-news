# Zely News — Plateforme d'Actualités Multi-Domaines, Web TV 24/7, Score en direct & ZeMercato

Application web complète développée avec **Django** combinant :
- **Actualités Multi-Domaines & Fil 24/7** : Synchronisation automatique de dépêches et articles depuis les flux RSS francophones.
- **Foot • Score en direct & ZeMercato** :
  - Synchronisation 100 % réelle via l'API publique **ESPN Soccer** (et connecteurs **Football-Data.org** / **API-Football** / **TheSportsDB**) sur 8 compétitions majeures (*Ligue 1, UEFA Champions League, Europa League, Conference League, Premier League, LaLiga, Serie A, Bundesliga*).
  - **Page dédiée par match** (`/sport/match/<id>/`) affichant le fil chronologique des événements (buteurs, passeurs, cartons), les statistiques comparatives, et les compositions d'équipes sur terrain tactique 2D.
  - **Classements officiels** et **Tableau des transferts ZeMercato** avec indice de fiabilité.
- **Studio Web TV 24/7 & Shorts** : Direct continu avec lecteur Picture-in-Picture (PiP), grille TV, replays VOD et questions interactives au plateau.
- **Le Pouls Citoyen** : Débats contradictoires argumentés, sondages en direct et signalements citoyens géolocalisés.
- **Espace Utilisateur Connecté** (`/mon-espace/`) : Menu déroulant rapide et pages dédiées (*Mon Flux, Mon Club & Matchs, Mes Favoris, Mes Contributions, Paramètres*).

## Installation & Lancement rapide

```powershell
# 1. Créer et activer l'environnement virtuel
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Appliquer les migrations
python manage.py migrate

# 4. Lancer le serveur de développement
python manage.py runserver 8000
```

Accédez ensuite à `http://127.0.0.1:8000/`.
