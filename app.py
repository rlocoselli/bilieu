from flask import Flask, render_template, request

app = Flask(__name__)

SUPPORTED_LANGS = ["fr", "en", "it"]

CONTACT = {
    "whatsapp_phone": "33600000000",
    "email": "votre-email@example.com",
}

CAROUSEL_IMAGES = [
    {"src": "images/hero/image.png", "alt": "Vue sur le lac"},
    {"src": "images/hero/image2.png", "alt": "Vue sur le lac"},
    {"src": "images/hero/image3.png", "alt": "Vue sur le lac"},
]

GUIDE_CONTENT = {
    "title": "Bienvenue à Bilieu",
    "description": "Découvrez notre logement spacieux et confortable",
    "amenities": [
        "Salon/hall : 1 canapé convertible confortable pour 2 personnes.",
        "1er étage : 2 pièces (1 bureau + 1 chambre avec 1 lit simple).",
        "2e étage : 1 chambre avec 1 lit simple + 1 fauteuil-lit",
        "2e étage : 1 chambre avec 1 lit double (couple).",
        "climatisation": "La climatisation est uniquement au dernier étage, actuellement en maintenance, retour prévu en septembre."
    ]
}

@app.route('/health')
def health_check():
    return "OK", 200

@app.route('/')
def index():
    lang = request.args.get('lang', 'fr')
    if lang not in SUPPORTED_LANGS:
        lang = 'fr'
    return render_template('index.html', lang=lang, supported_langs=SUPPORTED_LANGS, contact=CONTACT, carousel_images=CAROUSEL_IMAGES)

if __name__ == '__main__':
    app.run(debug=True)
