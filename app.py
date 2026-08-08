import logging
import os

from flask import Flask, jsonify, render_template, request
from werkzeug.exceptions import HTTPException


app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
app.logger.setLevel(logging.INFO)

SUPPORTED_LANGS = ["fr", "en", "it"]

AIRBNB_URL = os.getenv("AIRBNB_URL", "https://www.airbnb.fr/")
CONTACT_EMAIL = os.getenv("CONTACT_EMAIL", "")
WHATSAPP_PHONE = (
    os.getenv("WHATSAPP_PHONE", "")
    .replace("+", "")
    .replace(" ", "")
    .replace("-", "")
)

CAROUSEL_IMAGES = [
    {"src": "images/hero/image.png", "alt": "Vue générale de la maison"},
    {"src": "images/hero/image2.png", "alt": "Vue du lac de Paladru"},
]

# Ajoute ici d'autres photos si elles existent dans static/.
HOUSE_IMAGES = [
    {"src": "images/hero/image.png", "alt": "Vue générale de la maison"},
    {"src": "images/hero/image2.png", "alt": "Vue du lac de Paladru"},
]


def tr(lang, fr, en, it):
    return {"fr": fr, "en": en, "it": it}[lang]


def get_lang():
    lang = request.args.get("lang", "fr").lower()
    return lang if lang in SUPPORTED_LANGS else "fr"


def make_content(lang):
    """Données communes utilisées par index.html et les autres templates."""

    return {
        "meta_title": tr(
            lang,
            "Bilieu · Lac de Paladru",
            "Bilieu · Lake Paladru",
            "Bilieu · Lago di Paladru",
        ),
        "nav": {
            "house": tr(lang, "La maison", "The house", "La casa"),
            "house_photos": tr(lang, "Photos", "Photos", "Foto"),
            "history": tr(lang, "Histoire", "History", "Storia"),
            "bus": "Bus",
            "environment": tr(lang, "Environnement", "Environment", "Ambiente"),
            "services": tr(lang, "Services", "Services", "Servizi"),
            "beauties": tr(lang, "Découvrir", "Discover", "Scoprire"),
            "contact": tr(lang, "Contact", "Contact", "Contatti"),
        },
        "hero": {
            "subtitle": tr(
                lang,
                "Un séjour paisible à Bilieu, à proximité du lac de Paladru.",
                "A peaceful stay in Bilieu, close to Lake Paladru.",
                "Un soggiorno tranquillo a Bilieu, vicino al lago di Paladru.",
            )
        },
        "house": {
            "title": tr(lang, "La maison", "The house", "La casa"),
            "text": tr(
                lang,
                "Découvrez notre logement spacieux et confortable à Bilieu, à proximité du lac de Paladru.",
                "Discover our spacious and comfortable accommodation in Bilieu, close to Lake Paladru.",
                "Scopri la nostra abitazione spaziosa e confortevole a Bilieu, vicino al lago di Paladru.",
            ),
            "airbnb_url": AIRBNB_URL,
            "airbnb_label": tr(
                lang,
                "Voir sur Airbnb",
                "View on Airbnb",
                "Vedi su Airbnb",
            ),
        },
        "house_gallery": {
            "title": tr(
                lang,
                "Photos de la maison",
                "House photos",
                "Foto della casa",
            )
        },
        "stay_details": {
            "title": tr(lang, "Le logement", "Accommodation", "Alloggio"),
            "stats": [
                {
                    "label": tr(lang, "Localisation", "Location", "Località"),
                    "value": "Bilieu",
                },
                {"label": tr(lang, "Lac", "Lake", "Lago"), "value": "Paladru"},
                {
                    "label": tr(lang, "Type", "Type", "Tipo"),
                    "value": tr(lang, "Maison", "House", "Casa"),
                },
            ],
            "cards": [
                {
                    "title": tr(lang, "Salon / hall", "Living room / hall", "Salone / sala"),
                    "items": [
                        tr(
                            lang,
                            "1 canapé convertible confortable pour 2 personnes.",
                            "1 comfortable convertible sofa for 2 people.",
                            "1 divano convertibile comodo per 2 persone.",
                        )
                    ],
                },
                {
                    "title": tr(lang, "1er étage", "1st floor", "1° piano"),
                    "items": [
                        tr(
                            lang,
                            "2 pièces : 1 bureau + 1 chambre avec 1 lit simple.",
                            "2 rooms: 1 office + 1 bedroom with 1 single bed.",
                            "2 stanze: 1 ufficio + 1 camera con 1 letto singolo.",
                        )
                    ],
                },
                {
                    "title": tr(lang, "2e étage", "2nd floor", "2° piano"),
                    "items": [
                        tr(
                            lang,
                            "1 chambre avec 1 lit simple + 1 fauteuil-lit.",
                            "1 room with 1 single bed + 1 chair-bed.",
                            "1 camera con 1 letto singolo + 1 poltrona-letto.",
                        ),
                        tr(
                            lang,
                            "1 chambre avec 1 lit double.",
                            "1 room with 1 double bed.",
                            "1 camera con 1 letto matrimoniale.",
                        ),
                    ],
                },
                {
                    "title": tr(
                        lang,
                        "Climatisation",
                        "Air conditioning",
                        "Aria condizionata",
                    ),
                    "items": [
                        tr(
                            lang,
                            "Uniquement au dernier étage, en maintenance jusqu'en septembre.",
                            "Only on the top floor, under maintenance until September.",
                            "Solo all'ultimo piano, in manutenzione fino a settembre.",
                        )
                    ],
                },
            ],
        },
        "services": {
            "title": tr(lang, "Services", "Services", "Servizi"),
            "home_services_title": tr(
                lang,
                "Dans la maison",
                "At the house",
                "Nella casa",
            ),
            "home_services": [
                tr(
                    lang,
                    "Des équipements pratiques pour un séjour confortable.",
                    "Practical equipment for a comfortable stay.",
                    "Dotazioni pratiche per un soggiorno confortevole.",
                )
            ],
            "markets_title": tr(
                lang,
                "Services à proximité",
                "Nearby services",
                "Servizi nelle vicinanze",
            ),
            "markets": [
                tr(
                    lang,
                    "Commerces et services sont disponibles autour de Bilieu et du lac.",
                    "Shops and services are available around Bilieu and the lake.",
                    "Negozi e servizi sono disponibili nei dintorni di Bilieu e del lago.",
                )
            ],
        },
        "beauties": {
            "title": tr(
                lang,
                "Lac de Paladru",
                "Lake Paladru",
                "Lago di Paladru",
            ),
            "text": tr(
                lang,
                "Profitez du lac, de la nature et des promenades autour de Bilieu.",
                "Enjoy the lake, nature and walks around Bilieu.",
                "Godetevi il lago, la natura e le passeggiate intorno a Bilieu.",
            ),
        },
        "history": {
            "title": tr(
                lang,
                "Bilieu et son histoire",
                "Bilieu and its history",
                "Bilieu e la sua storia",
            ),
            "text": tr(
                lang,
                "Découvrez le patrimoine et l'histoire locale de Bilieu et du lac de Paladru.",
                "Discover the local heritage and history of Bilieu and Lake Paladru.",
                "Scopri il patrimonio e la storia locale di Bilieu e del lago di Paladru.",
            ),
        },
        # index.html utilise explicitement cards[3], donc conserver au moins 4 cartes.
        "pdf_info": {
            "title": tr(
                lang,
                "Informations pratiques",
                "Practical information",
                "Informazioni pratiche",
            ),
            "cards": [
                {
                    "title": tr(lang, "Stationnement", "Parking", "Parcheggio"),
                    "items": [
                        tr(
                            lang,
                            "Merci d'utiliser uniquement les emplacements indiqués.",
                            "Please use only the indicated parking areas.",
                            "Utilizzare esclusivamente gli spazi di parcheggio indicati.",
                        )
                    ],
                },
                {
                    "title": tr(lang, "Voisinage", "Neighbourhood", "Vicinato"),
                    "items": [
                        tr(
                            lang,
                            "Respectez le droit de passage du voisin et ne déposez rien sur son terrain.",
                            "Respect the neighbour's right of way and do not leave anything on neighbouring land.",
                            "Rispettare il diritto di passaggio del vicino e non lasciare oggetti sul suo terreno.",
                        )
                    ],
                },
                {
                    "title": tr(lang, "Électricité", "Electricity", "Elettricità"),
                    "items": [
                        tr(
                            lang,
                            "La recharge de voiture électrique sur les prises de la maison n'est pas autorisée.",
                            "EV charging from the house outlets is not permitted.",
                            "Non è consentito ricaricare auto elettriche dalle prese della casa.",
                        )
                    ],
                },
                {
                    "title": tr(lang, "Salle de bain", "Bathroom", "Bagno"),
                    "items": [
                        tr(
                            lang,
                            "Les équipements de salle de bain sont à disposition des voyageurs.",
                            "Bathroom facilities are available for guests.",
                            "Il bagno è a disposizione degli ospiti.",
                        )
                    ],
                },
            ],
        },
        "contact": {
            "title": tr(lang, "Contact", "Contact", "Contatti"),
            "text": tr(
                lang,
                "Pour toute question pendant votre séjour, contactez-nous.",
                "If you need help during your stay, please contact us.",
                "Per qualsiasi necessità durante il soggiorno, contattateci.",
            ),
            "whatsapp_label": "WhatsApp",
            "email_label": tr(lang, "E-mail", "Email", "E-mail"),
        },
    }


def make_history(lang):
    return {
        "title": tr(lang, "Histoire de Bilieu", "History of Bilieu", "Storia di Bilieu"),
        "intro": tr(
            lang,
            "Quelques repères pour découvrir Bilieu et le lac de Paladru.",
            "A few points to discover Bilieu and Lake Paladru.",
            "Alcuni riferimenti per scoprire Bilieu e il lago di Paladru.",
        ),
        "kpis": [
            {"label": tr(lang, "Village", "Village", "Paese"), "value": "Bilieu"},
            {
                "label": tr(lang, "Territoire", "Area", "Territorio"),
                "value": tr(lang, "Lac de Paladru", "Lake Paladru", "Lago di Paladru"),
            },
            {"label": tr(lang, "Département", "Department", "Dipartimento"), "value": "Isère"},
        ],
        "sections": [
            {
                "title": "Bilieu",
                "items": [
                    tr(
                        lang,
                        "Bilieu se trouve sur les hauteurs du lac de Paladru.",
                        "Bilieu lies on the heights above Lake Paladru.",
                        "Bilieu si trova sulle alture del lago di Paladru.",
                    )
                ],
            },
            {
                "title": tr(lang, "Le lac", "The lake", "Il lago"),
                "items": [
                    tr(
                        lang,
                        "Le lac et les paysages environnants occupent une place centrale dans la vie locale.",
                        "The lake and surrounding landscapes are central to local life.",
                        "Il lago e i paesaggi circostanti sono centrali nella vita locale.",
                    )
                ],
            },
        ],
    }


def make_guide(lang):
    sections = [
        (
            tr(lang, "Arrivée et stationnement", "Arrival and parking", "Arrivo e parcheggio"),
            [
                tr(
                    lang,
                    "Garez les véhicules uniquement aux emplacements indiqués.",
                    "Park vehicles only in the indicated areas.",
                    "Parcheggiare i veicoli solo negli spazi indicati.",
                ),
                tr(
                    lang,
                    "Laissez libre le droit de passage du voisin.",
                    "Keep the neighbour's right of way clear.",
                    "Lasciare libero il diritto di passaggio del vicino.",
                ),
            ],
        ),
        (
            tr(lang, "Voisinage", "Neighbourhood", "Vicinato"),
            [
                tr(
                    lang,
                    "Respectez le calme entre 22h00 et 08h00.",
                    "Respect quiet hours from 10 PM to 8 AM.",
                    "Rispettare il silenzio dalle 22:00 alle 08:00.",
                ),
                tr(
                    lang,
                    "Ne déposez aucun objet sur le terrain du voisin.",
                    "Do not leave objects on neighbouring land.",
                    "Non lasciare oggetti sul terreno del vicino.",
                ),
            ],
        ),
        (
            tr(lang, "Couchages", "Sleeping arrangements", "Posti letto"),
            [
                tr(
                    lang,
                    "Salon : canapé convertible pour 2 personnes.",
                    "Living room: convertible sofa for 2 people.",
                    "Salone: divano convertibile per 2 persone.",
                ),
                tr(
                    lang,
                    "1er étage : bureau et chambre avec lit simple.",
                    "1st floor: office and bedroom with a single bed.",
                    "1° piano: ufficio e camera con letto singolo.",
                ),
                tr(
                    lang,
                    "2e étage : deux chambres, dont une avec lit double.",
                    "2nd floor: two bedrooms, including one with a double bed.",
                    "2° piano: due camere, una con letto matrimoniale.",
                ),
            ],
        ),
        (
            tr(lang, "Linge et propreté", "Linen and cleanliness", "Biancheria e pulizia"),
            [
                tr(
                    lang,
                    "Laissez les espaces communs propres.",
                    "Leave shared spaces clean.",
                    "Lasciare puliti gli spazi comuni.",
                )
            ],
        ),
        (
            "Wi-Fi",
            [
                tr(
                    lang,
                    "Utilisez le réseau Wi-Fi de manière raisonnable.",
                    "Use the Wi-Fi network reasonably.",
                    "Utilizzare la rete Wi-Fi in modo ragionevole.",
                )
            ],
        ),
        (
            tr(lang, "Sécurité et énergie", "Safety and energy", "Sicurezza ed energia"),
            [
                tr(lang, "Maison non-fumeur.", "Non-smoking home.", "Casa non fumatori."),
                tr(
                    lang,
                    "La recharge de voiture électrique sur les prises de la maison n'est pas autorisée.",
                    "EV charging from the house outlets is not permitted.",
                    "Non è consentito ricaricare auto elettriche dalle prese della casa.",
                ),
            ],
        ),
        (
            tr(lang, "Animaux", "Pets", "Animali"),
            [
                tr(
                    lang,
                    "Les animaux sont les bienvenus, avec nettoyage après le séjour.",
                    "Pets are welcome, with cleanup after the stay.",
                    "Gli animali sono benvenuti, con pulizia dopo il soggiorno.",
                )
            ],
        ),
        (
            tr(lang, "Climatisation", "Air conditioning", "Aria condizionata"),
            [
                tr(
                    lang,
                    "Uniquement au dernier étage, en maintenance jusqu'en septembre.",
                    "Only on the top floor, under maintenance until September.",
                    "Solo all'ultimo piano, in manutenzione fino a settembre.",
                )
            ],
        ),
        (
            tr(lang, "Environnement", "Environment", "Ambiente"),
            [
                tr(
                    lang,
                    "Respectez la tranquillité des lieux et limitez les déchets.",
                    "Respect the area and reduce waste.",
                    "Rispettare la tranquillità del luogo e limitare i rifiuti.",
                )
            ],
        ),
        (
            tr(lang, "Avant le départ", "Before departure", "Prima della partenza"),
            [
                tr(
                    lang,
                    "Vérifiez que les fenêtres et les portes sont fermées.",
                    "Check that windows and doors are closed.",
                    "Controllare che porte e finestre siano chiuse.",
                )
            ],
        ),
    ]

    return {
        "title": tr(lang, "Guide du séjour", "Guest guide", "Guida del soggiorno"),
        "intro": tr(
            lang,
            "Les informations essentielles pour profiter de la maison dans de bonnes conditions.",
            "Essential information for a comfortable stay at the house.",
            "Le informazioni essenziali per un soggiorno confortevole nella casa.",
        ),
        "kpis": [
            {"label": tr(lang, "Silence", "Quiet hours", "Silenzio"), "value": "22h–08h"},
            {
                "label": tr(lang, "Maison", "Home", "Casa"),
                "value": tr(lang, "Non-fumeur", "Non-smoking", "Non fumatori"),
            },
            {
                "label": tr(lang, "Animaux", "Pets", "Animali"),
                "value": tr(lang, "Bienvenus", "Welcome", "Benvenuti"),
            },
        ],
        "sections": [{"title": title, "items": items} for title, items in sections],
    }


def make_bus(lang):
    return {
        "title": tr(lang, "Bus et transports", "Bus and transport", "Bus e trasporti"),
        "intro": tr(
            lang,
            "Informations pratiques pour se déplacer depuis Bilieu.",
            "Practical information for travelling from Bilieu.",
            "Informazioni pratiche per spostarsi da Bilieu.",
        ),
        "links": [
            {
                "label": "Pays Voironnais",
                "url": "https://www.paysvoironnais.com/",
            }
        ],
        "kpis": [
            {"label": tr(lang, "Réseau", "Network", "Rete"), "value": "Pays Voironnais"},
            {"label": tr(lang, "Commune", "Town", "Comune"), "value": "Bilieu"},
            {
                "label": "Info",
                "value": tr(lang, "Horaires en ligne", "Online timetables", "Orari online"),
            },
        ],
        "sections": [
            {
                "title": tr(lang, "Horaires", "Timetables", "Orari"),
                "items": [
                    tr(
                        lang,
                        "Consultez les horaires officiels avant votre déplacement.",
                        "Check official timetables before travelling.",
                        "Consultare gli orari ufficiali prima di partire.",
                    )
                ],
            },
            {
                "title": tr(lang, "Arrêts", "Stops", "Fermate"),
                "items": [
                    tr(
                        lang,
                        "Vérifiez l'arrêt et le sens de circulation avant le départ.",
                        "Check the stop and direction before departure.",
                        "Controllare la fermata e la direzione prima della partenza.",
                    )
                ],
            },
            {
                "title": tr(lang, "Conseils", "Tips", "Consigli"),
                "items": [
                    tr(
                        lang,
                        "Prévoyez quelques minutes d'avance.",
                        "Allow a few extra minutes.",
                        "Arrivare con qualche minuto di anticipo.",
                    )
                ],
            },
        ],
    }


def make_environment(lang):
    return {
        "title": tr(lang, "Environnement", "Environment", "Ambiente"),
        "intro": tr(
            lang,
            "Quelques gestes simples pour préserver Bilieu et le lac de Paladru.",
            "Simple actions to help protect Bilieu and Lake Paladru.",
            "Piccoli gesti per preservare Bilieu e il lago di Paladru.",
        ),
        "kpis": [
            {
                "label": tr(lang, "Cadre", "Setting", "Contesto"),
                "value": tr(lang, "Lac & nature", "Lake & nature", "Lago & natura"),
            },
            {
                "label": tr(lang, "Priorité", "Priority", "Priorità"),
                "value": tr(lang, "Respect", "Respect", "Rispetto"),
            },
            {
                "label": tr(lang, "Déchets", "Waste", "Rifiuti"),
                "value": tr(lang, "À trier", "Sort it", "Differenziare"),
            },
        ],
        "sections": [
            {
                "title": tr(lang, "Eau", "Water", "Acqua"),
                "items": [
                    tr(
                        lang,
                        "Évitez le gaspillage d'eau pendant votre séjour.",
                        "Avoid wasting water during your stay.",
                        "Evitare sprechi d'acqua durante il soggiorno.",
                    )
                ],
            },
            {
                "title": tr(lang, "Déchets", "Waste", "Rifiuti"),
                "items": [
                    tr(
                        lang,
                        "Triez les déchets selon les consignes locales.",
                        "Sort waste according to local instructions.",
                        "Differenziare i rifiuti secondo le indicazioni locali.",
                    )
                ],
            },
            {
                "title": tr(lang, "Déplacements", "Getting around", "Spostamenti"),
                "items": [
                    tr(
                        lang,
                        "Privilégiez la marche pour les trajets courts lorsque c'est possible.",
                        "Walk for short journeys when practical.",
                        "Preferire gli spostamenti a piedi per i tragitti brevi quando possibile.",
                    )
                ],
            },
            {
                "title": tr(lang, "Nature", "Nature", "Natura"),
                "items": [
                    tr(
                        lang,
                        "Respectez les espaces naturels, les riverains et la tranquillité du lac.",
                        "Respect natural areas, neighbours and the quiet surroundings of the lake.",
                        "Rispettare gli spazi naturali, i vicini e la tranquillità del lago.",
                    )
                ],
            },
        ],
    }


def make_legal(lang):
    return {
        "title": tr(
            lang,
            "Confidentialité & cookies",
            "Privacy & cookies",
            "Privacy e cookie",
        ),
        "intro": tr(
            lang,
            "Informations sur la confidentialité et le fonctionnement du site.",
            "Information about privacy and how this website operates.",
            "Informazioni sulla privacy e sul funzionamento del sito.",
        ),
        "sections": [
            {
                "title": tr(lang, "Cookies", "Cookies", "Cookie"),
                "items": [
                    tr(
                        lang,
                        "Le site utilise uniquement les éléments nécessaires à son fonctionnement et à la mémorisation du choix de consentement.",
                        "The site uses only items required for operation and to remember your consent choice.",
                        "Il sito utilizza solo gli elementi necessari al funzionamento e alla memorizzazione della scelta di consenso.",
                    )
                ],
            },
            {
                "title": tr(
                    lang,
                    "Contenus externes",
                    "External content",
                    "Contenuti esterni",
                ),
                "items": [
                    tr(
                        lang,
                        "Les médias tiers ne sont chargés qu'à la demande.",
                        "Third-party media is loaded only on request.",
                        "I media di terze parti vengono caricati solo su richiesta.",
                    )
                ],
            },
            {
                "title": tr(lang, "Contact", "Contact", "Contatti"),
                "items": [
                    tr(
                        lang,
                        "Les coordonnées affichées servent aux échanges liés au séjour.",
                        "Displayed contact details are intended for communication related to the stay.",
                        "I recapiti mostrati servono alle comunicazioni relative al soggiorno.",
                    )
                ],
            },
        ],
    }


def common_context(lang):
    return {
        "content": make_content(lang),
        "lang": lang,
        "supported_langs": SUPPORTED_LANGS,
    }


@app.route("/")
def index():
    lang = get_lang()
    context = common_context(lang)

    context.update(
        carousel_images=CAROUSEL_IMAGES,
        whatsapp_link=(
            f"https://wa.me/{WHATSAPP_PHONE}" if WHATSAPP_PHONE else "#contact"
        ),
        email_link=f"mailto:{CONTACT_EMAIL}" if CONTACT_EMAIL else "#contact",
    )

    return render_template("index.html", **context)


@app.route("/photos")
def house_photos():
    lang = get_lang()
    context = common_context(lang)
    context["house_images"] = HOUSE_IMAGES
    return render_template("house_photos.html", **context)


@app.route("/history")
def history():
    lang = get_lang()
    context = common_context(lang)
    context["history"] = make_history(lang)
    return render_template("history.html", **context)


@app.route("/bus")
def bus():
    lang = get_lang()
    context = common_context(lang)
    context["bus"] = make_bus(lang)
    return render_template("bus.html", **context)


@app.route("/environment")
def environment():
    lang = get_lang()
    context = common_context(lang)
    context["environment"] = make_environment(lang)
    return render_template("environment.html", **context)


@app.route("/guide")
def guide():
    lang = get_lang()
    context = common_context(lang)
    context["guide"] = make_guide(lang)
    return render_template("guide.html", **context)


@app.route("/privacy")
def privacy():
    lang = get_lang()
    context = common_context(lang)
    context["legal"] = make_legal(lang)
    return render_template("privacy.html", **context)


@app.route("/health")
def health_check():
    return jsonify(status="healthy"), 200


@app.errorhandler(Exception)
def handle_unexpected_exception(error):
    # Préserve les erreurs HTTP normales (404, 405, etc.).
    if isinstance(error, HTTPException):
        return error

    app.logger.error(
        "Unhandled Flask exception",
        exc_info=(type(error), error, error.__traceback__),
    )
    return "Internal Server Error", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082, debug=False)
