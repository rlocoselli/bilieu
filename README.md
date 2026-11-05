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

Les annonces automatiques utilisent le compte `ca-pub-6158185990205930` sur l'accueil, les photos, l'histoire et l'environnement. Le script AdSense est installé dans ces pages pour permettre à la plateforme de consentement certifiée de Google de présenter son message et de gérer les choix publicitaires. Le site ne présente plus sa propre bannière de consentement. Les pages de guide, transport, soutien et confidentialité ne chargent pas le script AdSense. Le lien « Gérer les cookies » ouvre à nouveau le message Google depuis une page avec annonces.

Pour afficher aussi une annonce dans l'emplacement prévu entre les sections, définir `ADSENSE_SLOT_HOME` et/ou `ADSENSE_SLOT_CONTENT` avec les identifiants numériques des blocs d'annonces créés dans AdSense. Sans ces variables, seules les annonces automatiques sont possibles. `ADSENSE_CLIENT` permet de changer le compte éditeur.

Le domaine public est `domusbiliacum.fr`. Son fichier `/ads.txt` autorise ce compte éditeur. Ajouter `domusbiliacum.fr` dans **AdSense → Sites** et attendre son approbation pour diffuser les annonces. Publier un message de réglementations européennes pour ce site dans **AdSense → Confidentialité et messages** ; choisir `https://domusbiliacum.fr/privacy` comme politique de confidentialité. Activer les annonces automatiques pour le site dans **AdSense → Annonces**.

## Personnalisation rapide

- Mettre votre lien Airbnb dans `app.py` (`airbnb_url` pour `fr`, `en`, `it`).
- Ajouter des photos dans `static/images/` et les référencer dans `CAROUSEL_IMAGES` dans `app.py`.
