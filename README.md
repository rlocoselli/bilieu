# Site Flask multilingue — Bilieu / Lac de Paladru

## Lancer le projet

```bash
cd /home/testuser/bilieu
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app run --debug
```

Puis ouvrir: `http://127.0.0.1:5000/`

## Docker container

```bash
cd /home/testuser/bilieu
docker compose up -d --build
```

Puis ouvrir: `http://127.0.0.1:8082/`

Pour arrêter:

```bash
docker compose down
```

## Langues

- Français (par défaut)
- Anglais (`/?lang=en`)
- Italien (`/?lang=it`)
- Espagnol (`/?lang=es`)

## Annonces AdSense

Les annonces automatiques utilisent le compte `ca-pub-6158185990205930` sur l'accueil, les photos, l'histoire et l'environnement. Le script Google est chargé uniquement après l'acceptation des annonces dans la bannière de consentement. Les pages de guide, transport, soutien et confidentialité ne chargent pas ce script.

Pour afficher aussi une annonce dans l'emplacement prévu entre les sections, définir `ADSENSE_SLOT_HOME` et/ou `ADSENSE_SLOT_CONTENT` avec les identifiants numériques des blocs d'annonces créés dans AdSense. Sans ces variables, seules les annonces automatiques sont possibles. `ADSENSE_CLIENT` permet de changer le compte éditeur.

Le domaine public est `domusbiliacum.fr`. Son fichier `/ads.txt` autorise ce compte éditeur. Ajouter `domusbiliacum.fr` dans **AdSense → Sites** et attendre son approbation pour diffuser les annonces. Pour les visiteurs de l'EEE, du Royaume-Uni et de Suisse, configurer aussi une plateforme de gestion du consentement certifiée par Google dans **AdSense → Confidentialité et messages** avant d'activer la diffusion.

## Personnalisation rapide

- Mettre votre lien Airbnb dans `app.py` (`airbnb_url` pour `fr`, `en`, `it`).
- Ajouter des photos dans `static/images/` et les référencer dans `CAROUSEL_IMAGES` dans `app.py`.
