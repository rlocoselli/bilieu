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

## Personnalisation rapide

- Mettre votre lien Airbnb dans `app.py` (`airbnb_url` pour `fr`, `en`, `it`).
- Ajouter des photos dans `static/images/` et les référencer dans `CAROUSEL_IMAGES` dans `app.py`.
