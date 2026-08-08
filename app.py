import os

from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)


app = Flask(__name__)

SUPPORTED_LANGS = ["fr", "en", "it"]


CONTACT = {
    "whatsapp_phone": os.getenv("WHATSAPP_PHONE", "33600000000"),
    "email": os.getenv("CONTACT_EMAIL", "votre-email@example.com"),
}


CAROUSEL_IMAGES = [
    {
        "src": "images/hero/image.png",
        "alt": "Vue générale de la maison",
    },
    {
        "src": "images/hero/image2.png",
        "alt": "Vue du lac de Paladru",
    },
]


GUIDE_CONTENT = {
    "fr": {
        "meta_title": "Bilieu - Lac de Paladru",

        "nav": {
            "house": "La maison",
            "house_photos": "Photos",
            "history": "Histoire",
            "bus": "Transports",
            "environment": "Environnement",
            "services": "Services",
            "beauties": "Découvrir",
            "contact": "Contact",
        },

        "hero": {
            "subtitle": "Une maison au cœur de Bilieu, près du lac de Paladru.",
        },

        "house": {
            "title": "La maison",
            "text": (
                "Découvrez notre logement spacieux et confortable à Bilieu, "
                "à proximité du lac de Paladru."
            ),
            "airbnb_url": "https://www.airbnb.fr/",
            "airbnb_label": "Voir sur Airbnb",
        },

        "stay_details": {
            "title": "Le logement",
            "stats": [
                {"label": "Localisation", "value": "Bilieu"},
                {"label": "Lac", "value": "Paladru"},
                {"label": "Type", "value": "Maison"},
            ],
            "cards": [
                {
                    "title": "Couchages",
                    "items": [
                        "Salon : canapé convertible pour 2 personnes.",
                        "1er étage : bureau et chambre avec lit simple.",
                        "2e étage : chambre avec lit simple et fauteuil-lit.",
                        "2e étage : chambre avec lit double.",
                    ],
                },
                {
                    "title": "Climatisation",
                    "items": [
                        "Climatisation uniquement au dernier étage.",
                        "Actuellement en maintenance jusqu'en septembre.",
                    ],
                },
            ],
        },

        "services": {
            "title": "Services",
            "home_services_title": "Dans la maison",
            "home_services": [
                "Un logement confortable pour profiter de votre séjour."
            ],
            "markets_title": "Commerces",
            "markets": [
                "Commerces et services disponibles dans les environs."
            ],
        },

        "pdf_info": {
            "title": "Informations pratiques",
            "cards": [
                {
                    "title": "Stationnement",
                    "items": [
                        "Merci de respecter les emplacements indiqués."
                    ],
                },
                {
                    "title": "Voisinage",
                    "items": [
                        "Merci de respecter le droit de passage du voisinage."
                    ],
                },
                {
                    "title": "Électricité",
                    "items": [
                        "La recharge des voitures électriques sur les prises "
                        "de la maison n'est pas autorisée."
                    ],
                },
                {
                    "title": "Salle de bain",
                    "items": [
                        "Salle de bain et équipements à disposition."
                    ],
                },
            ],
        },

        "beauties": {
            "title": "Le lac de Paladru",
            "text": (
                "Profitez du lac, des paysages et des promenades autour de Bilieu."
            ),
        },

        "history": {
            "title": "Bilieu et son histoire",
            "text": (
                "Découvrez l'histoire et le patrimoine de Bilieu "
                "et du lac de Paladru."
            ),
        },

        "contact": {
            "title": "Contact",
            "text": "Une question pendant votre séjour ? Contactez-nous.",
            "whatsapp_label": "WhatsApp",
            "email_label": "E-mail",
        },
    },

    "en": {
        "meta_title": "Bilieu - Lake Paladru",

        "nav": {
            "house": "The house",
            "house_photos": "Photos",
            "history": "History",
            "bus": "Transport",
            "environment": "Environment",
            "services": "Services",
            "beauties": "Discover",
            "contact": "Contact",
        },

        "hero": {
            "subtitle": "A home in Bilieu, close to Lake Paladru.",
        },

        "house": {
            "title": "The house",
            "text": (
                "Discover our spacious and comfortable accommodation "
                "in Bilieu, near Lake Paladru."
            ),
            "airbnb_url": "https://www.airbnb.com/",
            "airbnb_label": "View on Airbnb",
        },

        "stay_details": {
            "title": "Accommodation",
            "stats": [
                {"label": "Location", "value": "Bilieu"},
                {"label": "Lake", "value": "Paladru"},
                {"label": "Type", "value": "House"},
            ],
            "cards": [
                {
                    "title": "Sleeping arrangements",
                    "items": [
                        "Living room: convertible sofa for 2 people.",
                        "First floor: office and bedroom with single bed.",
                        "Second floor: room with single bed and chair bed.",
                        "Second floor: bedroom with double bed.",
                    ],
                },
                {
                    "title": "Air conditioning",
                    "items": [
                        "Air conditioning is available only on the top floor.",
                        "Currently under maintenance until September.",
                    ],
                },
            ],
        },

        "services": {
            "title": "Services",
            "home_services_title": "At home",
            "home_services": [
                "Comfortable accommodation for your stay."
            ],
            "markets_title": "Shops",
            "markets": [
                "Local shops and services are available nearby."
            ],
        },

        "pdf_info": {
            "title": "Practical information",
            "cards": [
                {
                    "title": "Parking",
                    "items": ["Please use the designated parking areas."],
                },
                {
                    "title": "Neighbours",
                    "items": ["Please respect the neighbour's right of way."],
                },
                {
                    "title": "Electricity",
                    "items": [
                        "EV charging using the house outlets is not permitted."
                    ],
                },
                {
                    "title": "Bathroom",
                    "items": ["Bathroom facilities are available."],
                },
            ],
        },

        "beauties": {
            "title": "Lake Paladru",
            "text": "Enjoy the lake, landscapes and walks around Bilieu.",
        },

        "history": {
            "title": "History of Bilieu",
            "text": "Discover the heritage of Bilieu and Lake Paladru.",
        },

        "contact": {
            "title": "Contact",
            "text": "Have a question during your stay? Contact us.",
            "whatsapp_label": "WhatsApp",
            "email_label": "Email",
        },
    },

    "it": {
        "meta_title": "Bilieu - Lago di Paladru",

        "nav": {
            "house": "La casa",
            "house_photos": "Foto",
            "history": "Storia",
            "bus": "Trasporti",
            "environment": "Ambiente",
            "services": "Servizi",
            "beauties": "Scoprire",
            "contact": "Contatti",
        },

        "hero": {
            "subtitle": "Una casa a Bilieu, vicino al lago di Paladru.",
        },

        "house": {
            "title": "La casa",
            "text": (
                "Scopri la nostra abitazione spaziosa e confortevole "
                "a Bilieu, vicino al lago di Paladru."
            ),
            "airbnb_url": "https://www.airbnb.it/",
            "airbnb_label": "Vedi su Airbnb",
        },

        "stay_details": {
            "title": "Alloggio",
            "stats": [
                {"label": "Località", "value": "Bilieu"},
                {"label": "Lago", "value": "Paladru"},
                {"label": "Tipo", "value": "Casa"},
            ],
            "cards": [
                {
                    "title": "Posti letto",
                    "items": [
                        "Salone: divano convertibile per 2 persone.",
                        "Primo piano: ufficio e camera con letto singolo.",
                        "Secondo piano: camera con letto singolo e poltrona-letto.",
                        "Secondo piano: camera con letto matrimoniale.",
                    ],
                },
                {
                    "title": "Aria condizionata",
                    "items": [
                        "Aria condizionata solo all'ultimo piano.",
                        "Attualmente in manutenzione fino a settembre.",
                    ],
                },
            ],
        },

        "services": {
            "title": "Servizi",
            "home_services_title": "Nella casa",
            "home_services": [
                "Un alloggio confortevole per il vostro soggiorno."
            ],
            "markets_title": "Negozi",
            "markets": [
                "Negozi e servizi disponibili nelle vicinanze."
            ],
        },

        "pdf_info": {
            "title": "Informazioni pratiche",
            "cards": [
                {
                    "title": "Parcheggio",
                    "items": ["Utilizzare gli spazi indicati."],
                },
                {
                    "title": "Vicini",
                    "items": ["Rispettare il diritto di passaggio del vicino."],
                },
                {
                    "title": "Elettricità",
                    "items": [
                        "Non è consentita la ricarica di auto elettriche "
                        "tramite le prese della casa."
                    ],
                },
                {
                    "title": "Bagno",
                    "items": ["Bagno e servizi disponibili."],
                },
            ],
        },

        "beauties": {
            "title": "Lago di Paladru",
            "text": (
                "Godetevi il lago, i paesaggi e le passeggiate intorno a Bilieu."
            ),
        },

        "history": {
            "title": "La storia di Bilieu",
            "text": "Scopri la storia di Bilieu e del lago di Paladru.",
        },

        "contact": {
            "title": "Contatti",
            "text": "Una domanda durante il soggiorno? Contattaci.",
            "whatsapp_label": "WhatsApp",
            "email_label": "E-mail",
        },
    },
}


def get_lang():
    lang = request.args.get("lang", "fr")

    if lang not in SUPPORTED_LANGS:
        return "fr"

    return lang


@app.route("/")
def index():
    lang = get_lang()

    whatsapp_link = (
        f"https://wa.me/{CONTACT['whatsapp_phone']}"
    )

    email_link = (
        f"mailto:{CONTACT['email']}"
    )

    return render_template(
        "index.html",
        content=GUIDE_CONTENT[lang],
        lang=lang,
        supported_langs=SUPPORTED_LANGS,
        contact=CONTACT,
        carousel_images=CAROUSEL_IMAGES,
        whatsapp_link=whatsapp_link,
        email_link=email_link,
    )


# Ces endpoints sont nécessaires car index.html les utilise avec url_for().
# Pour l'instant ils redirigent vers la homepage.


@app.route("/photos")
def house_photos():
    lang = get_lang()
    return redirect(url_for("index", lang=lang) + "#house")


@app.route("/history")
def history():
    lang = get_lang()
    return redirect(url_for("index", lang=lang) + "#history")


@app.route("/bus")
def bus():
    lang = get_lang()
    return redirect(url_for("index", lang=lang))


@app.route("/environment")
def environment():
    lang = get_lang()
    return redirect(url_for("index", lang=lang) + "#beauties")


@app.route("/guide")
def guide():
    lang = get_lang()
    return redirect(url_for("index", lang=lang) + "#pdf-info")


@app.route("/privacy")
def privacy():
    lang = get_lang()
    return redirect(url_for("index", lang=lang))


@app.route("/health")
def health_check():
    return jsonify(status="healthy"), 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8082,
        debug=False,
    )