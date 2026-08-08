import os
from flask import Flask, render_template, request
from flask import jsonify

app = Flask(__name__)

SUPPORTED_LANGS = ["fr", "en", "it"]

CONTACT = {
    "whatsapp_phone": "33600000000",
    "email": "votre-email@example.com",
}

CAROUSEL_IMAGES = [
    {"src": "images/hero/image.png", "alt": "Vue générale de la maison"},
    {"src": "images/hero/image2.png", "alt": "Vue du lac"}
]

GUIDE_CONTENT = {
    "fr": {
        "description": "Découvrez notre logement spacieux et confortable",
        "amenities": [
            "Salon/hall : 1 canapé convertible confortable pour 2 personnes.",
            "1er étage : 2 pièces (1 bureau + 1 chambre avec 1 lit simple).",
            "2e étage : 1 chambre avec 1 lit simple + 1 fauteuil-lit",
            "2e étage : 1 chambre avec 1 lit double (couple).",
            "Climatisation": "Uniquement au dernier étage, en maintenance jusqu'en septembre."
        ]
    },
    "en": {
        "description": "Discover our spacious and comfortable accommodation",
        "amenities": [
            "Living room/hall: 1 convertible sofa comfortable for 2 people.",
            "1st floor: 2 rooms (1 office + 1 room with 1 single bed).",
            "2nd floor: 1 room with 1 single bed + 1 armchair-bed",
            "2nd floor: 1 room with 1 double bed (couple).",
            "Air conditioning": "Only on the top floor, currently under maintenance, and expected back in September."
        ]
    },
    "it": {
        "description": "Scopri la nostra abitazione spaziosa e confortevole",
        "amenities": [
            "Salone/sala: 1 divano convertibile comodo per 2 persone.",
            "1° piano: 2 stanze (1 ufficio + 1 stanza con 1 letto singolo).",
            "2° piano: 1 stanza con 1 letto singolo + 1 poltrona-letto",
            "2° piano: 1 stanza con 1 letto doppio (coppia).",
            "Aria condizionata": "Solo al piano superiore, attualmente in manutenzione e prevista di ritorno a settembre."
        ]
    }
}

@app.route('/')
def home():
    lang = request.args.get('lang', 'fr')
    if lang not in SUPPORTED_LANGS:
        lang = 'fr'
    return render_template('index.html',
                         content=GUIDE_CONTENT[lang],
                         lang=lang,
                         supported_langs=SUPPORTED_LANGS,
                         contact=CONTACT,
                        carousel_images=CAROUSEL_IMAGES)

@app.route('/health')
def health_check():
    return jsonify(status="healthy"), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)
