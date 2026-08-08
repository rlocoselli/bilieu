from pathlib import Path
import shutil, zipfile, textwrap, os, json

root = Path("/mnt/data/bilieu_improved")
templates_dir = root / "templates"
static_css = root / "static" / "css"
static_js = root / "static" / "js"
templates_dir.mkdir(parents=True, exist_ok=True)
static_css.mkdir(parents=True, exist_ok=True)
static_js.mkdir(parents=True, exist_ok=True)

# Copy the templates the user uploaded.
template_names = [
    "index.html",
    "house_photos.html",
    "history.html",
    "bus.html",
    "environment.html",
    "guide.html",
    "privacy.html",
]
for name in template_names:
    src = Path("/mnt/data") / name
    if src.exists():
        shutil.copy2(src, templates_dir / name)
    else:
        raise FileNotFoundError(src)

app_py = r'''import logging
import os

from flask import Flask, jsonify, render_template, request
from werkzeug.exceptions import HTTPException


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
app.logger.setLevel(logging.INFO)

SUPPORTED_LANGS = ["fr", "en", "it"]

AIRBNB_URL = os.getenv(
    "AIRBNB_URL",
    "https://www.airbnb.fr/rooms/1402915287163928554",
)
CONTACT_EMAIL = os.getenv("CONTACT_EMAIL", "")
WHATSAPP_PHONE = (
    os.getenv("WHATSAPP_PHONE", "")
    .replace("+", "")
    .replace(" ", "")
    .replace("-", "")
)

CAROUSEL_IMAGES = [
    {
        "src": "images/carroussel/image.png",
        "alt": "Vue extérieure de la maison",
    },
    {
        "src": "images/carroussel/image copy.png",
        "alt": "Jardin et environnement",
    },
    {
        "src": "images/carroussel/image copy 2.png",
        "alt": "Vue du lac et alentours",
    },
    {
        "src": "images/carroussel/image copy 3.png",
        "alt": "Ambiance du séjour à Bilieu",
    },
]

HOUSE_IMAGES = CAROUSEL_IMAGES


def get_lang():
    lang = request.args.get("lang", "fr").lower()
    return lang if lang in SUPPORTED_LANGS else "fr"


CONTENT = {
    "fr": {
        "meta_title": "Domus Biliacum · Bilieu & lac de Paladru",
        "nav": {
            "house": "Maison Airbnb",
            "house_photos": "Photos maison",
            "history": "Histoire de Bilieu",
            "bus": "Lignes de bus",
            "environment": "Environnement",
            "services": "Services & commerces",
            "beauties": "Lac de Paladru",
            "contact": "Contact",
        },
        "hero": {
            "subtitle": (
                "Votre guide pratique pour profiter sereinement de la maison, "
                "du village de Bilieu et du lac de Paladru."
            )
        },
        "house": {
            "title": "La maison à Bilieu",
            "text": (
                "Une maison familiale à proximité du lac de Paladru, pensée pour "
                "un séjour simple et confortable. Vous trouverez ici les informations "
                "essentielles avant l'arrivée : accès, stationnement, couchages, "
                "équipements et règles de voisinage."
            ),
            "airbnb_url": AIRBNB_URL,
            "airbnb_label": "Voir l'annonce Airbnb",
        },
        "house_gallery": {"title": "Photos de la maison"},
        "stay_details": {
            "title": "Capacité, chambres & couchages",
            "stats": [
                {"label": "Capacité", "value": "Jusqu'à 7 personnes"},
                {"label": "Chambres", "value": "3 chambres + 1 bureau"},
                {"label": "Couchages", "value": "5 couchages répartis dans la maison"},
                {"label": "Salon", "value": "Canapé convertible 2 places"},
            ],
            "cards": [
                {
                    "title": "Répartition des couchages",
                    "items": [
                        "Hall / salon : 1 canapé convertible confortable pour 2 personnes.",
                        "1er étage : 2 pièces, dont 1 bureau et 1 chambre avec 1 lit simple.",
                        "2e étage : 1 chambre avec 1 lit simple + 1 fauteuil-lit.",
                        "2e étage : 1 chambre avec 1 lit double pour un couple.",
                    ],
                },
                {
                    "title": "À prévoir avant votre arrivée",
                    "items": [
                        "Draps, couvertures et serviettes ne sont pas fournis.",
                        "Prévoyez votre linge de lit et de toilette en fonction des couchages utilisés.",
                        "Des barrières de sécurité pour les escaliers sont disponibles dans la maison.",
                    ],
                },
            ],
        },
        "services": {
            "title": "Services & équipements utiles",
            "home_services_title": "Équipements de la maison",
            "home_services": [
                "Wi-Fi Bbox–1202F156, Smart TV, poêle à granulés pilotable avec l'application MCZ, lave-linge au dernier étage et espace bureau avec écran, clavier et souris."
            ],
            "markets_title": "Commerces à proximité",
            "markets": [
                "Casino Charavines – 25 Avenue du Lac, 38850 Charavines. Pensez à vérifier les horaires selon la saison."
            ],
        },
        "beauties": {
            "title": "Le lac de Paladru",
            "text": (
                "Bilieu offre un accès privilégié au cadre naturel du lac de Paladru : "
                "balades, paysages, plages et activités de plein air dans une ambiance "
                "paisible. Merci de respecter les riverains et les espaces naturels."
            ),
        },
        "history": {
            "title": "L'histoire de Bilieu",
            "text": (
                "Village du Pays voironnais au bord du lac de Paladru, Bilieu conserve "
                "une identité rurale forte, liée à l'agriculture, aux hameaux et à la "
                "relation historique du territoire avec le lac."
            ),
        },
        "pdf_info": {
            "title": "Informations essentielles avant votre séjour",
            "cards": [
                {
                    "title": "Arrivée & départ",
                    "items": [
                        "Check-in : à partir de 15h00.",
                        "Check-out : au plus tard à 10h00.",
                        "Stationnement public gratuit dans la rue.",
                    ],
                },
                {
                    "title": "Accès à la maison",
                    "items": [
                        "Après avoir stationné, empruntez le chemin en herbe/gravier.",
                        "Suivez la clôture en bois.",
                        "Repérez la maison avec la grande baie vitrée et la porte en bois à carrés vitrés.",
                    ],
                },
                {
                    "title": "Règles importantes",
                    "items": [
                        "Maison strictement non-fumeurs.",
                        "Silence demandé de 22h00 à 08h00.",
                        "La zone devant la maison est une servitude d'accès : gardez-la libre et ne laissez aucun objet sur le terrain du voisin.",
                        "La recharge d'un véhicule électrique sur les prises de la maison n'est pas autorisée.",
                    ],
                },
                {
                    "title": "Confort & équipements",
                    "items": [
                        "Wi-Fi, Smart TV, poêle à granulés MCZ, lave-linge et espace bureau équipé.",
                        "Climatisation uniquement au dernier étage ; actuellement en maintenance jusqu'en septembre.",
                        "Animaux bienvenus, à condition de nettoyer après leur passage.",
                        "Draps, couvertures et serviettes non fournis.",
                    ],
                },
            ],
        },
        "contact": {
            "title": "Besoin d'aide pendant le séjour ?",
            "text": (
                "Pour une question sur l'arrivée, l'accès à la maison, un équipement "
                "ou une difficulté pendant le séjour, contactez-nous directement."
            ),
            "whatsapp_label": "Écrire sur WhatsApp",
            "email_label": "Envoyer un e-mail",
        },
    },

    "en": {
        "meta_title": "Domus Biliacum · Bilieu & Lake Paladru",
        "nav": {
            "house": "Airbnb house",
            "house_photos": "House photos",
            "history": "History of Bilieu",
            "bus": "Bus lines",
            "environment": "Environment",
            "services": "Services & shops",
            "beauties": "Lake Paladru",
            "contact": "Contact",
        },
        "hero": {
            "subtitle": (
                "Your practical guide to enjoy the house, Bilieu village and "
                "Lake Paladru with everything you need before arrival."
            )
        },
        "house": {
            "title": "The house in Bilieu",
            "text": (
                "A family house close to Lake Paladru, designed for a simple and "
                "comfortable stay. This site brings together the key information "
                "about access, parking, sleeping arrangements, equipment and neighbour rules."
            ),
            "airbnb_url": AIRBNB_URL,
            "airbnb_label": "Open Airbnb listing",
        },
        "house_gallery": {"title": "House photos"},
        "stay_details": {
            "title": "Capacity, rooms & sleeping",
            "stats": [
                {"label": "Capacity", "value": "Up to 7 guests"},
                {"label": "Bedrooms", "value": "3 bedrooms + 1 office"},
                {"label": "Sleeping spots", "value": "5 sleeping spots across floors"},
                {"label": "Living room", "value": "Double sofa bed"},
            ],
            "cards": [
                {
                    "title": "Sleeping layout",
                    "items": [
                        "Hall / living room: 1 comfortable convertible sofa for 2 people.",
                        "1st floor: 2 rooms, including 1 office and 1 bedroom with a single bed.",
                        "2nd floor: 1 bedroom with a single bed + 1 armchair bed.",
                        "2nd floor: 1 bedroom with a double bed for a couple.",
                    ],
                },
                {
                    "title": "Bring with you",
                    "items": [
                        "Sheets, blankets and towels are not provided.",
                        "Please bring the appropriate bed linen and towels for the sleeping places you will use.",
                        "Safety gates for the stairs are available in the house.",
                    ],
                },
            ],
        },
        "services": {
            "title": "Useful services & equipment",
            "home_services_title": "House equipment",
            "home_services": [
                "Wi-Fi Bbox–1202F156, Smart TV, pellet stove controlled through the MCZ app, washing machine on the top floor and office area with monitor, keyboard and mouse."
            ],
            "markets_title": "Nearby shops",
            "markets": [
                "Casino Charavines – 25 Avenue du Lac, 38850 Charavines. Check opening hours, especially during seasonal periods."
            ],
        },
        "beauties": {
            "title": "Lake Paladru",
            "text": (
                "Bilieu offers easy access to the natural setting of Lake Paladru, "
                "with walks, views, beaches and outdoor activities. Please respect "
                "neighbours and natural areas."
            ),
        },
        "history": {
            "title": "The history of Bilieu",
            "text": (
                "Bilieu is a village in the Pays Voironnais area beside Lake Paladru, "
                "with a strong rural identity shaped by farming, hamlets and its "
                "long-standing relationship with the lake."
            ),
        },
        "pdf_info": {
            "title": "Essential information before your stay",
            "cards": [
                {
                    "title": "Arrival & departure",
                    "items": [
                        "Check-in: from 3:00 PM.",
                        "Check-out: by 10:00 AM.",
                        "Free public parking in the street.",
                    ],
                },
                {
                    "title": "Finding the house",
                    "items": [
                        "After parking, take the grass/gravel path.",
                        "Follow the wooden fence.",
                        "Look for the house with the large bay window and wooden door with square glass panes.",
                    ],
                },
                {
                    "title": "Important rules",
                    "items": [
                        "Strictly non-smoking property.",
                        "Quiet hours from 10:00 PM to 8:00 AM.",
                        "The area in front of the house is an access easement: keep it clear and do not leave anything on the neighbour's land.",
                        "Charging an electric vehicle from the house outlets is not permitted.",
                    ],
                },
                {
                    "title": "Comfort & equipment",
                    "items": [
                        "Wi-Fi, Smart TV, MCZ pellet stove, washing machine and equipped office area.",
                        "Air conditioning is available only on the top floor and is currently under maintenance until September.",
                        "Pets are welcome; please clean after them.",
                        "Sheets, blankets and towels are not provided.",
                    ],
                },
            ],
        },
        "contact": {
            "title": "Need help during your stay?",
            "text": (
                "For questions about arrival, access, house equipment or any difficulty "
                "during your stay, contact us directly."
            ),
            "whatsapp_label": "Message on WhatsApp",
            "email_label": "Send an email",
        },
    },

    "it": {
        "meta_title": "Domus Biliacum · Bilieu & lago di Paladru",
        "nav": {
            "house": "Casa Airbnb",
            "house_photos": "Foto casa",
            "history": "Storia di Bilieu",
            "bus": "Linee autobus",
            "environment": "Ambiente",
            "services": "Servizi & negozi",
            "beauties": "Lago di Paladru",
            "contact": "Contatto",
        },
        "hero": {
            "subtitle": (
                "La guida pratica per vivere serenamente la casa, Bilieu e il lago "
                "di Paladru, con tutte le informazioni utili prima dell'arrivo."
            )
        },
        "house": {
            "title": "La casa a Bilieu",
            "text": (
                "Una casa familiare vicino al lago di Paladru, pensata per un soggiorno "
                "semplice e confortevole. Qui trovate le informazioni essenziali su "
                "accesso, parcheggio, posti letto, dotazioni e regole di vicinato."
            ),
            "airbnb_url": AIRBNB_URL,
            "airbnb_label": "Apri annuncio Airbnb",
        },
        "house_gallery": {"title": "Foto della casa"},
        "stay_details": {
            "title": "Capienza, camere e posti letto",
            "stats": [
                {"label": "Capienza", "value": "Fino a 7 ospiti"},
                {"label": "Camere", "value": "3 camere + 1 ufficio"},
                {"label": "Posti letto", "value": "5 posti letto distribuiti sui piani"},
                {"label": "Soggiorno", "value": "Divano letto matrimoniale"},
            ],
            "cards": [
                {
                    "title": "Distribuzione dei posti letto",
                    "items": [
                        "Ingresso / soggiorno: 1 divano letto comodo per 2 persone.",
                        "1° piano: 2 stanze, di cui 1 ufficio e 1 camera con letto singolo.",
                        "2° piano: 1 camera con letto singolo + 1 poltrona-letto.",
                        "2° piano: 1 camera con letto matrimoniale.",
                    ],
                },
                {
                    "title": "Da portare",
                    "items": [
                        "Lenzuola, coperte e asciugamani non sono forniti.",
                        "Portate la biancheria necessaria in base ai posti letto utilizzati.",
                        "Sono disponibili barriere di sicurezza per le scale.",
                    ],
                },
            ],
        },
        "services": {
            "title": "Servizi e dotazioni utili",
            "home_services_title": "Dotazioni della casa",
            "home_services": [
                "Wi-Fi Bbox–1202F156, Smart TV, stufa a pellet tramite app MCZ, lavatrice all'ultimo piano e zona ufficio con monitor, tastiera e mouse."
            ],
            "markets_title": "Negozi nelle vicinanze",
            "markets": [
                "Casino Charavines – 25 Avenue du Lac, 38850 Charavines. Verificate gli orari, soprattutto nei periodi stagionali."
            ],
        },
        "beauties": {
            "title": "Il lago di Paladru",
            "text": (
                "Bilieu permette di godere facilmente del lago di Paladru, delle "
                "passeggiate, dei paesaggi, delle spiagge e delle attività all'aperto. "
                "Rispettate i vicini e gli spazi naturali."
            ),
        },
        "history": {
            "title": "La storia di Bilieu",
            "text": (
                "Bilieu è un paese del Pays Voironnais sulle rive del lago di Paladru, "
                "con una forte identità rurale legata all'agricoltura, ai piccoli "
                "nuclei abitati e al rapporto storico con il lago."
            ),
        },
        "pdf_info": {
            "title": "Informazioni essenziali prima del soggiorno",
            "cards": [
                {
                    "title": "Arrivo & partenza",
                    "items": [
                        "Check-in: dalle 15:00.",
                        "Check-out: entro le 10:00.",
                        "Parcheggio pubblico gratuito in strada.",
                    ],
                },
                {
                    "title": "Accesso alla casa",
                    "items": [
                        "Dopo aver parcheggiato, prendete il sentiero in erba/ghiaia.",
                        "Seguite la recinzione in legno.",
                        "Cercate la casa con la grande vetrata e la porta in legno con riquadri vetrati.",
                    ],
                },
                {
                    "title": "Regole importanti",
                    "items": [
                        "Casa rigorosamente non fumatori.",
                        "Silenzio dalle 22:00 alle 08:00.",
                        "La zona davanti alla casa è una servitù di accesso: lasciatela libera e non depositate nulla sul terreno del vicino.",
                        "Non è consentito ricaricare un veicolo elettrico tramite le prese della casa.",
                    ],
                },
                {
                    "title": "Comfort & dotazioni",
                    "items": [
                        "Wi-Fi, Smart TV, stufa a pellet MCZ, lavatrice e zona ufficio attrezzata.",
                        "Aria condizionata solo all'ultimo piano, attualmente in manutenzione fino a settembre.",
                        "Animali benvenuti; pulire dopo il loro soggiorno.",
                        "Lenzuola, coperte e asciugamani non sono forniti.",
                    ],
                },
            ],
        },
        "contact": {
            "title": "Serve aiuto durante il soggiorno?",
            "text": (
                "Per domande sull'arrivo, sull'accesso, sulle dotazioni della casa "
                "o per qualsiasi difficoltà durante il soggiorno, contattateci."
            ),
            "whatsapp_label": "Scrivi su WhatsApp",
            "email_label": "Invia un'e-mail",
        },
    },
}


HISTORY = {
    "fr": {
        "title": "L'histoire de Bilieu",
        "intro": (
            "Bilieu est une commune du nord Isère au bord du lac de Paladru. "
            "Son histoire est liée à la vie rurale, aux voies de passage locales "
            "et à l'évolution touristique du lac."
        ),
        "kpis": [
            {"label": "Région", "value": "Auvergne-Rhône-Alpes"},
            {"label": "Territoire", "value": "Pays voironnais"},
            {"label": "Repère local", "value": "Lac de Paladru"},
            {"label": "Identité", "value": "Village nature & patrimoine"},
        ],
        "sections": [
            {
                "title": "Étymologie du nom Bilieu",
                "items": [
                    "Selon des interprétations toponymiques locales, le nom Bilieu pourrait dériver d'une forme ancienne liée à un domaine rural gallo-romain.",
                    "Comme pour de nombreux noms anciens, l'origine exacte n'est pas absolument certaine et peut varier selon les sources historiques.",
                ],
            },
            {
                "title": "Origines rurales",
                "items": [
                    "Le développement du village s'est appuyé sur l'agriculture, l'élevage et la gestion des terres autour du lac.",
                    "L'habitat traditionnel s'organise historiquement en hameaux et maisons familiales liés aux activités locales.",
                ],
            },
            {
                "title": "Lien avec le lac de Paladru",
                "items": [
                    "Le lac a structuré la vie quotidienne : pêche, circulation locale, loisirs puis attractivité touristique.",
                    "Aujourd'hui encore, le lac reste au cœur de l'identité paysagère et culturelle de Bilieu.",
                ],
            },
            {
                "title": "Patrimoine & vie locale",
                "items": [
                    "Le territoire conserve un caractère résidentiel paisible, mêlant mémoire rurale et usages contemporains.",
                    "Le rythme local reste fortement marqué par les saisons et les activités de plein air.",
                ],
            },
        ],
    },
    "en": {
        "title": "The history of Bilieu",
        "intro": (
            "Bilieu is a municipality in northern Isère on the shore of Lake Paladru. "
            "Its history is linked to rural life, local routes and the lake's growing tourism role."
        ),
        "kpis": [
            {"label": "Region", "value": "Auvergne-Rhône-Alpes"},
            {"label": "Area", "value": "Pays Voironnais"},
            {"label": "Local landmark", "value": "Lake Paladru"},
            {"label": "Identity", "value": "Nature & heritage village"},
        ],
        "sections": [
            {
                "title": "Etymology of the name Bilieu",
                "items": [
                    "Local toponymic interpretations suggest that Bilieu may derive from an older form linked to a rural Gallo-Roman estate.",
                    "As with many old place names, the exact origin is not completely certain and may vary across historical sources.",
                ],
            },
            {
                "title": "Rural roots",
                "items": [
                    "The village developed through agriculture, livestock activity and land use around the lake.",
                    "Traditional settlement patterns historically relied on hamlets and family homes connected to local work.",
                ],
            },
            {
                "title": "Connection with Lake Paladru",
                "items": [
                    "The lake shaped daily life through fishing, local movement, leisure and later visitor attraction.",
                    "It remains central to Bilieu's landscape and cultural identity.",
                ],
            },
            {
                "title": "Heritage & local life",
                "items": [
                    "The area keeps a calm residential character, combining rural memory with contemporary uses.",
                    "Local life remains strongly influenced by seasons and outdoor activities.",
                ],
            },
        ],
    },
    "it": {
        "title": "La storia di Bilieu",
        "intro": (
            "Bilieu è un comune del nord Isère sulle rive del lago di Paladru. "
            "La sua storia è legata alla vita rurale, alle vie locali e allo sviluppo turistico del lago."
        ),
        "kpis": [
            {"label": "Regione", "value": "Auvergne-Rhône-Alpes"},
            {"label": "Territorio", "value": "Pays Voironnais"},
            {"label": "Punto di riferimento", "value": "Lago di Paladru"},
            {"label": "Identità", "value": "Paese natura & patrimonio"},
        ],
        "sections": [
            {
                "title": "Etimologia del nome Bilieu",
                "items": [
                    "Secondo interpretazioni toponomastiche locali, il nome Bilieu potrebbe derivare da una forma antica legata a un dominio rurale gallo-romano.",
                    "Come per molti nomi antichi, l'origine esatta non è completamente certa e può variare secondo le fonti storiche.",
                ],
            },
            {
                "title": "Origini rurali",
                "items": [
                    "Lo sviluppo del paese si è basato su agricoltura, allevamento e gestione delle terre intorno al lago.",
                    "Gli insediamenti tradizionali erano organizzati in piccoli nuclei e case familiari legate alle attività locali.",
                ],
            },
            {
                "title": "Legame con il lago di Paladru",
                "items": [
                    "Il lago ha influenzato la vita quotidiana: pesca, spostamenti, svago e poi attrattiva turistica.",
                    "Ancora oggi è al centro dell'identità paesaggistica e culturale di Bilieu.",
                ],
            },
            {
                "title": "Patrimonio & vita locale",
                "items": [
                    "Il territorio conserva un carattere residenziale tranquillo, tra memoria rurale e usi contemporanei.",
                    "La vita locale è ancora fortemente segnata dalle stagioni e dalle attività all'aperto.",
                ],
            },
        ],
    },
}


BUS = {
    "fr": {
        "title": "Lignes de bus",
        "intro": (
            "Informations pratiques pour organiser vos trajets autour de Bilieu et du lac de Paladru. "
            "Les horaires peuvent évoluer selon la saison : vérifiez toujours les horaires officiels avant le départ."
        ),
        "links": [
            {
                "label": "Itinéraire en transport (Google Maps)",
                "url": "https://www.google.com/maps/dir/?api=1&destination=Bilieu%2C%20France&travelmode=transit",
            }
        ],
        "kpis": [
            {"label": "Départ conseillé", "value": "Arrêt Bilieu centre"},
            {"label": "Correspondance", "value": "Voiron gare"},
            {"label": "Vers le lac", "value": "Bilieu / Charavines"},
            {"label": "Conseil", "value": "Arriver 5 min avant"},
        ],
        "sections": [
            {
                "title": "Horaires types (indicatifs)",
                "items": [
                    "Lundi-vendredi : passages renforcés le matin et en fin d'après-midi.",
                    "Samedi : fréquence réduite ; vérifiez les retours en soirée.",
                    "Dimanche et jours fériés : service limité selon la période.",
                ],
            },
            {
                "title": "Itinéraires utiles",
                "items": [
                    "Bilieu → Charavines : accès aux commerces et aux zones du lac.",
                    "Bilieu → Voiron : correspondance train et services urbains.",
                    "Bilieu → Le Pin / Paladru : déplacements locaux et balades.",
                ],
            },
            {
                "title": "Conseils voyageurs",
                "items": [
                    "Prévoyez un titre de transport valide avant la montée.",
                    "En période touristique, anticipez les départs les plus demandés.",
                    "Pour les retours tardifs, prévoyez une solution alternative si nécessaire.",
                ],
            },
        ],
    },
    "en": {
        "title": "Bus lines",
        "intro": (
            "Practical information for travelling around Bilieu and Lake Paladru. "
            "Schedules may change seasonally, so always check official timetables before leaving."
        ),
        "links": [
            {
                "label": "Public transport route (Google Maps)",
                "url": "https://www.google.com/maps/dir/?api=1&destination=Bilieu%2C%20France&travelmode=transit",
            }
        ],
        "kpis": [
            {"label": "Suggested stop", "value": "Bilieu centre"},
            {"label": "Connection", "value": "Voiron station"},
            {"label": "Lake access", "value": "Bilieu / Charavines"},
            {"label": "Tip", "value": "Arrive 5 min early"},
        ],
        "sections": [
            {
                "title": "Typical service (indicative)",
                "items": [
                    "Monday-Friday: more services in the morning and late afternoon.",
                    "Saturday: reduced frequency; check evening return options.",
                    "Sunday and public holidays: limited service depending on the period.",
                ],
            },
            {
                "title": "Useful routes",
                "items": [
                    "Bilieu → Charavines: access to shops and lake areas.",
                    "Bilieu → Voiron: rail connections and urban services.",
                    "Bilieu → Le Pin / Paladru: local travel and walks.",
                ],
            },
            {
                "title": "Traveller tips",
                "items": [
                    "Have a valid ticket ready before boarding.",
                    "During busy tourism periods, plan ahead for popular departures.",
                    "For late returns, keep an alternative transport option in mind.",
                ],
            },
        ],
    },
    "it": {
        "title": "Linee autobus",
        "intro": (
            "Informazioni pratiche per spostarsi tra Bilieu e il lago di Paladru. "
            "Gli orari possono cambiare secondo la stagione: controllate sempre gli orari ufficiali prima di partire."
        ),
        "links": [
            {
                "label": "Percorso con trasporto pubblico (Google Maps)",
                "url": "https://www.google.com/maps/dir/?api=1&destination=Bilieu%2C%20France&travelmode=transit",
            }
        ],
        "kpis": [
            {"label": "Fermata consigliata", "value": "Bilieu centre"},
            {"label": "Coincidenza", "value": "Stazione di Voiron"},
            {"label": "Verso il lago", "value": "Bilieu / Charavines"},
            {"label": "Consiglio", "value": "Arrivare 5 min prima"},
        ],
        "sections": [
            {
                "title": "Orari tipici (indicativi)",
                "items": [
                    "Lunedì-venerdì: più passaggi al mattino e nel tardo pomeriggio.",
                    "Sabato: frequenza ridotta; verificare i rientri serali.",
                    "Domenica e festivi: servizio limitato secondo il periodo.",
                ],
            },
            {
                "title": "Percorsi utili",
                "items": [
                    "Bilieu → Charavines: accesso a negozi e zone del lago.",
                    "Bilieu → Voiron: coincidenze ferroviarie e servizi urbani.",
                    "Bilieu → Le Pin / Paladru: spostamenti locali e passeggiate.",
                ],
            },
            {
                "title": "Consigli",
                "items": [
                    "Tenere pronto un titolo di viaggio valido.",
                    "Nei periodi turistici, pianificare in anticipo le partenze più richieste.",
                    "Per i rientri tardivi, prevedere un'alternativa se necessario.",
                ],
            },
        ],
    },
}


ENVIRONMENT = {
    "fr": {
        "title": "Astuces environnement",
        "intro": (
            "Quelques gestes simples pour préserver la tranquillité de Bilieu, "
            "le voisinage et le cadre naturel du lac de Paladru."
        ),
        "kpis": [
            {"label": "Cadre", "value": "Lac & nature"},
            {"label": "Priorité", "value": "Respect du voisinage"},
            {"label": "Déchets", "value": "Trier & limiter"},
            {"label": "Déplacements", "value": "Marche & transports"},
        ],
        "sections": [
            {
                "title": "Eau & énergie",
                "items": [
                    "Évitez de laisser couler l'eau inutilement.",
                    "Éteignez les lumières et équipements inutilisés.",
                    "N'utilisez pas les prises de la maison pour recharger un véhicule électrique.",
                ],
            },
            {
                "title": "Déchets",
                "items": [
                    "Triez les déchets selon les consignes locales.",
                    "Ne laissez aucun déchet dans les espaces naturels ni sur le terrain voisin.",
                ],
            },
            {
                "title": "Déplacements",
                "items": [
                    "Pour les courts trajets autour du lac, privilégiez la marche lorsque c'est possible.",
                    "Consultez les horaires de bus avant le départ, particulièrement le week-end.",
                ],
            },
            {
                "title": "Nature & voisinage",
                "items": [
                    "Respectez les zones naturelles et les propriétés privées.",
                    "Gardez le passage devant la maison libre : il s'agit d'une servitude d'accès.",
                    "Respectez le silence entre 22h00 et 08h00.",
                ],
            },
        ],
    },
    "en": {
        "title": "Environmental tips",
        "intro": (
            "Simple actions to protect Bilieu's quiet setting, neighbours and "
            "the natural environment around Lake Paladru."
        ),
        "kpis": [
            {"label": "Setting", "value": "Lake & nature"},
            {"label": "Priority", "value": "Respect neighbours"},
            {"label": "Waste", "value": "Sort & reduce"},
            {"label": "Travel", "value": "Walk & public transport"},
        ],
        "sections": [
            {
                "title": "Water & energy",
                "items": [
                    "Avoid wasting water.",
                    "Switch off lights and equipment when not needed.",
                    "Do not use the house outlets to charge an electric vehicle.",
                ],
            },
            {
                "title": "Waste",
                "items": [
                    "Sort waste according to local instructions.",
                    "Do not leave waste in natural areas or on neighbouring property.",
                ],
            },
            {
                "title": "Getting around",
                "items": [
                    "For short trips around the lake, walk when practical.",
                    "Check bus timetables before leaving, especially at weekends.",
                ],
            },
            {
                "title": "Nature & neighbours",
                "items": [
                    "Respect natural areas and private property.",
                    "Keep the area in front of the house clear because it is an access easement.",
                    "Respect quiet hours from 10 PM to 8 AM.",
                ],
            },
        ],
    },
    "it": {
        "title": "Consigli ambientali",
        "intro": (
            "Piccoli gesti per preservare la tranquillità di Bilieu, il vicinato "
            "e l'ambiente naturale del lago di Paladru."
        ),
        "kpis": [
            {"label": "Contesto", "value": "Lago & natura"},
            {"label": "Priorità", "value": "Rispetto del vicinato"},
            {"label": "Rifiuti", "value": "Differenziare & ridurre"},
            {"label": "Spostamenti", "value": "A piedi & trasporti"},
        ],
        "sections": [
            {
                "title": "Acqua & energia",
                "items": [
                    "Evitare sprechi d'acqua.",
                    "Spegnere luci e apparecchi non utilizzati.",
                    "Non usare le prese della casa per ricaricare un veicolo elettrico.",
                ],
            },
            {
                "title": "Rifiuti",
                "items": [
                    "Differenziare i rifiuti secondo le indicazioni locali.",
                    "Non lasciare rifiuti negli spazi naturali o sul terreno del vicino.",
                ],
            },
            {
                "title": "Spostamenti",
                "items": [
                    "Per i tragitti brevi intorno al lago, preferire la camminata quando possibile.",
                    "Controllare gli orari degli autobus, soprattutto nel fine settimana.",
                ],
            },
            {
                "title": "Natura & vicinato",
                "items": [
                    "Rispettare gli spazi naturali e le proprietà private.",
                    "Lasciare libera la zona davanti alla casa: è una servitù di accesso.",
                    "Rispettare il silenzio dalle 22:00 alle 08:00.",
                ],
            },
        ],
    },
}


GUIDE = {
    "fr": {
        "title": "Guide du séjour",
        "intro": (
            "Tout ce qu'il faut savoir avant et pendant votre séjour : arrivée, "
            "stationnement, accès, couchages, équipements et règles importantes."
        ),
        "kpis": [
            {"label": "Check-in", "value": "15h00"},
            {"label": "Check-out", "value": "10h00"},
            {"label": "Silence", "value": "22h00–08h00"},
            {"label": "Parking", "value": "Public gratuit"},
        ],
        "sections": [
            {
                "title": "Arrivée & accès à la maison",
                "items": [
                    "Check-in à partir de 15h00.",
                    "Le stationnement public est gratuit dans la rue.",
                    "Après avoir stationné, prenez le chemin en herbe/gravier.",
                    "Suivez la clôture en bois jusqu'à la maison.",
                    "Repérez la grande baie vitrée et la porte en bois à carrés vitrés.",
                ],
            },
            {
                "title": "Stationnement, voisinage & servitude",
                "items": [
                    "Ne bloquez jamais le passage devant la maison : cette zone est une servitude d'accès.",
                    "Ne garez pas de véhicule et ne laissez aucun objet sur le terrain du voisin.",
                    "Respectez la tranquillité du voisinage, en particulier entre 22h00 et 08h00.",
                    "La recharge de voiture électrique sur les prises de la maison n'est pas autorisée.",
                ],
            },
            {
                "title": "Couchages & linge",
                "items": [
                    "Capacité maximale indiquée : jusqu'à 7 personnes.",
                    "Hall / salon : canapé convertible confortable pour 2 personnes.",
                    "1er étage : bureau + chambre avec 1 lit simple.",
                    "2e étage : chambre avec 1 lit simple + 1 fauteuil-lit.",
                    "2e étage : chambre avec 1 lit double.",
                    "Draps, couvertures et serviettes ne sont pas fournis : merci de les apporter.",
                ],
            },
            {
                "title": "Équipements de la maison",
                "items": [
                    "Wi-Fi : réseau Bbox–1202F156.",
                    "Smart TV disponible.",
                    "Poêle à granulés pilotable avec l'application MCZ.",
                    "Lave-linge au dernier étage, dans la salle de bains.",
                    "Espace bureau avec écran, clavier et souris.",
                    "Barrières de sécurité pour les escaliers disponibles.",
                ],
            },
            {
                "title": "Wi-Fi & médias",
                "items": [
                    "Réseau Wi-Fi : Bbox–1202F156.",
                    "La Smart TV est disponible pour vos usages habituels.",
                    "Le site ne charge les médias externes qu'à votre demande afin de limiter les chargements tiers.",
                ],
            },
            {
                "title": "Chauffage & climatisation",
                "items": [
                    "Le poêle à granulés peut être piloté avec l'application MCZ.",
                    "La climatisation est disponible uniquement au dernier étage.",
                    "La climatisation est actuellement en maintenance et son retour est prévu en septembre.",
                ],
            },
            {
                "title": "Animaux",
                "items": [
                    "Les animaux sont les bienvenus.",
                    "Merci de nettoyer après eux, à l'intérieur comme autour de la maison.",
                    "Veillez à ne pas gêner les voisins ni les zones de passage.",
                ],
            },
            {
                "title": "Sécurité & règles de la maison",
                "items": [
                    "Maison strictement non-fumeurs.",
                    "Silence demandé de 22h00 à 08h00.",
                    "Gardez les zones de passage et escaliers dégagés.",
                    "Des barrières de sécurité pour les escaliers sont disponibles si nécessaire.",
                    "N'utilisez pas les prises domestiques pour recharger une voiture électrique.",
                ],
            },
            {
                "title": "Environnement & vie locale",
                "items": [
                    "Respectez le lac, les espaces naturels et les propriétés privées.",
                    "Limitez les déchets et suivez les consignes locales de tri.",
                    "Pour les commerces, Casino Charavines se trouve au 25 Avenue du Lac, 38850 Charavines.",
                    "Pour les transports, vérifiez les horaires officiels avant chaque déplacement.",
                ],
            },
            {
                "title": "Avant le départ",
                "items": [
                    "Check-out au plus tard à 10h00.",
                    "Vérifiez que vos effets personnels ont été récupérés.",
                    "Laissez les espaces utilisés propres et rangés.",
                    "Si vous voyagez avec un animal, vérifiez que les zones utilisées ont été nettoyées.",
                    "Assurez-vous de ne rien laisser dans la zone de servitude ou sur le terrain du voisin.",
                ],
            },
        ],
    },
    "en": {
        "title": "Guest guide",
        "intro": (
            "Everything you need before and during your stay: arrival, parking, access, "
            "sleeping arrangements, equipment and important house rules."
        ),
        "kpis": [
            {"label": "Check-in", "value": "3:00 PM"},
            {"label": "Check-out", "value": "10:00 AM"},
            {"label": "Quiet hours", "value": "10 PM–8 AM"},
            {"label": "Parking", "value": "Free public"},
        ],
        "sections": [
            {
                "title": "Arrival & finding the house",
                "items": [
                    "Check-in from 3:00 PM.",
                    "Free public parking is available in the street.",
                    "After parking, take the grass/gravel path.",
                    "Follow the wooden fence to the house.",
                    "Look for the large bay window and wooden door with square glass panes.",
                ],
            },
            {
                "title": "Parking, neighbours & access easement",
                "items": [
                    "Never block the area in front of the house; it is an access easement.",
                    "Do not park or leave objects on the neighbour's land.",
                    "Respect the neighbourhood, especially during quiet hours from 10 PM to 8 AM.",
                    "Charging an electric vehicle from the house outlets is not permitted.",
                ],
            },
            {
                "title": "Sleeping arrangements & linen",
                "items": [
                    "Maximum indicated capacity: up to 7 guests.",
                    "Hall / living room: comfortable sofa bed for 2 people.",
                    "1st floor: office + bedroom with 1 single bed.",
                    "2nd floor: bedroom with 1 single bed + 1 armchair bed.",
                    "2nd floor: bedroom with 1 double bed.",
                    "Sheets, blankets and towels are not provided; please bring your own.",
                ],
            },
            {
                "title": "House equipment",
                "items": [
                    "Wi-Fi network: Bbox–1202F156.",
                    "Smart TV available.",
                    "Pellet stove controlled through the MCZ app.",
                    "Washing machine on the top floor in the bathroom.",
                    "Office area with monitor, keyboard and mouse.",
                    "Safety gates for stairs are available.",
                ],
            },
            {
                "title": "Wi-Fi & media",
                "items": [
                    "Wi-Fi network: Bbox–1202F156.",
                    "Smart TV is available for normal guest use.",
                    "External media on the website is loaded only on request to reduce third-party loading.",
                ],
            },
            {
                "title": "Heating & air conditioning",
                "items": [
                    "The pellet stove can be controlled through the MCZ app.",
                    "Air conditioning is available only on the top floor.",
                    "The air conditioning is currently under maintenance and is expected back in September.",
                ],
            },
            {
                "title": "Pets",
                "items": [
                    "Pets are welcome.",
                    "Please clean after them inside and around the house.",
                    "Make sure they do not disturb neighbours or access areas.",
                ],
            },
            {
                "title": "Safety & house rules",
                "items": [
                    "Strictly non-smoking property.",
                    "Quiet hours from 10 PM to 8 AM.",
                    "Keep passageways and stairs clear.",
                    "Safety gates for stairs are available if needed.",
                    "Do not charge an electric vehicle from domestic outlets.",
                ],
            },
            {
                "title": "Environment & local life",
                "items": [
                    "Respect the lake, natural areas and private property.",
                    "Reduce waste and follow local sorting instructions.",
                    "For shopping, Casino Charavines is at 25 Avenue du Lac, 38850 Charavines.",
                    "For public transport, check official timetables before each journey.",
                ],
            },
            {
                "title": "Before departure",
                "items": [
                    "Check-out by 10:00 AM.",
                    "Make sure you have collected all personal belongings.",
                    "Leave used areas clean and tidy.",
                    "If travelling with a pet, make sure used areas have been cleaned.",
                    "Do not leave anything in the access easement or on the neighbour's land.",
                ],
            },
        ],
    },
    "it": {
        "title": "Guida del soggiorno",
        "intro": (
            "Tutto ciò che serve prima e durante il soggiorno: arrivo, parcheggio, "
            "accesso, posti letto, dotazioni e regole importanti."
        ),
        "kpis": [
            {"label": "Check-in", "value": "15:00"},
            {"label": "Check-out", "value": "10:00"},
            {"label": "Silenzio", "value": "22:00–08:00"},
            {"label": "Parcheggio", "value": "Pubblico gratuito"},
        ],
        "sections": [
            {
                "title": "Arrivo & accesso alla casa",
                "items": [
                    "Check-in dalle 15:00.",
                    "Parcheggio pubblico gratuito in strada.",
                    "Dopo aver parcheggiato, prendere il sentiero in erba/ghiaia.",
                    "Seguire la recinzione in legno fino alla casa.",
                    "Cercare la grande vetrata e la porta in legno con riquadri vetrati.",
                ],
            },
            {
                "title": "Parcheggio, vicinato & servitù",
                "items": [
                    "Non bloccare la zona davanti alla casa: è una servitù di accesso.",
                    "Non parcheggiare e non lasciare oggetti sul terreno del vicino.",
                    "Rispettare il vicinato, soprattutto dalle 22:00 alle 08:00.",
                    "Non è consentito ricaricare un'auto elettrica tramite le prese della casa.",
                ],
            },
            {
                "title": "Posti letto & biancheria",
                "items": [
                    "Capienza massima indicata: fino a 7 ospiti.",
                    "Ingresso / soggiorno: divano letto comodo per 2 persone.",
                    "1° piano: ufficio + camera con 1 letto singolo.",
                    "2° piano: camera con 1 letto singolo + 1 poltrona-letto.",
                    "2° piano: camera con 1 letto matrimoniale.",
                    "Lenzuola, coperte e asciugamani non sono forniti: portarli con sé.",
                ],
            },
            {
                "title": "Dotazioni della casa",
                "items": [
                    "Rete Wi-Fi: Bbox–1202F156.",
                    "Smart TV disponibile.",
                    "Stufa a pellet controllabile tramite app MCZ.",
                    "Lavatrice all'ultimo piano, nel bagno.",
                    "Zona ufficio con monitor, tastiera e mouse.",
                    "Barriere di sicurezza per le scale disponibili.",
                ],
            },
            {
                "title": "Wi-Fi & media",
                "items": [
                    "Rete Wi-Fi: Bbox–1202F156.",
                    "Smart TV disponibile per l'uso normale degli ospiti.",
                    "I media esterni del sito vengono caricati solo su richiesta per limitare i contenuti di terze parti.",
                ],
            },
            {
                "title": "Riscaldamento & aria condizionata",
                "items": [
                    "La stufa a pellet può essere controllata tramite l'app MCZ.",
                    "L'aria condizionata è disponibile solo all'ultimo piano.",
                    "L'aria condizionata è attualmente in manutenzione e il ritorno è previsto a settembre.",
                ],
            },
            {
                "title": "Animali",
                "items": [
                    "Gli animali sono benvenuti.",
                    "Pulire dopo di loro dentro e intorno alla casa.",
                    "Fare attenzione a non disturbare i vicini e le zone di passaggio.",
                ],
            },
            {
                "title": "Sicurezza & regole della casa",
                "items": [
                    "Casa rigorosamente non fumatori.",
                    "Silenzio dalle 22:00 alle 08:00.",
                    "Tenere liberi passaggi e scale.",
                    "Sono disponibili barriere di sicurezza per le scale.",
                    "Non ricaricare veicoli elettrici dalle prese domestiche.",
                ],
            },
            {
                "title": "Ambiente & vita locale",
                "items": [
                    "Rispettare il lago, gli spazi naturali e le proprietà private.",
                    "Ridurre i rifiuti e seguire le regole locali di raccolta differenziata.",
                    "Per la spesa, Casino Charavines si trova al 25 Avenue du Lac, 38850 Charavines.",
                    "Per i trasporti, controllare gli orari ufficiali prima di ogni spostamento.",
                ],
            },
            {
                "title": "Prima della partenza",
                "items": [
                    "Check-out entro le 10:00.",
                    "Controllare di aver preso tutti gli effetti personali.",
                    "Lasciare puliti e ordinati gli spazi utilizzati.",
                    "Se viaggiate con un animale, verificare che le zone utilizzate siano state pulite.",
                    "Non lasciare nulla nella servitù di accesso o sul terreno del vicino.",
                ],
            },
        ],
    },
}


LEGAL = {
    "fr": {
        "title": "Confidentialité & cookies",
        "intro": "Informations simples sur le fonctionnement du site et les contenus externes.",
        "sections": [
            {
                "title": "Cookies",
                "items": [
                    "Le site utilise uniquement les éléments nécessaires à son fonctionnement et à la mémorisation de votre choix de consentement.",
                    "Votre choix est enregistré localement dans votre navigateur.",
                ],
            },
            {
                "title": "Contenus externes",
                "items": [
                    "Les médias tiers, comme la vidéo, ne sont chargés qu'après une action de votre part.",
                    "Les liens externes (Airbnb, YouTube, cartes ou transports) ouvrent les services concernés dans une nouvelle page.",
                ],
            },
            {
                "title": "Contact",
                "items": [
                    "Les coordonnées affichées servent uniquement aux échanges liés à la maison et au séjour.",
                ],
            },
        ],
    },
    "en": {
        "title": "Privacy & cookies",
        "intro": "Simple information about how the website works and how external content is handled.",
        "sections": [
            {
                "title": "Cookies",
                "items": [
                    "The site uses only elements needed for operation and to remember your consent choice.",
                    "Your choice is stored locally in your browser.",
                ],
            },
            {
                "title": "External content",
                "items": [
                    "Third-party media, such as video, is loaded only after an action from you.",
                    "External links (Airbnb, YouTube, maps or transport) open the relevant services separately.",
                ],
            },
            {
                "title": "Contact",
                "items": [
                    "Displayed contact details are intended only for communication related to the house and stay.",
                ],
            },
        ],
    },
    "it": {
        "title": "Privacy e cookie",
        "intro": "Informazioni semplici sul funzionamento del sito e sui contenuti esterni.",
        "sections": [
            {
                "title": "Cookie",
                "items": [
                    "Il sito utilizza solo gli elementi necessari al funzionamento e alla memorizzazione della scelta di consenso.",
                    "La scelta viene salvata localmente nel browser.",
                ],
            },
            {
                "title": "Contenuti esterni",
                "items": [
                    "I media di terze parti, come i video, vengono caricati solo dopo una vostra azione.",
                    "I link esterni (Airbnb, YouTube, mappe o trasporti) aprono i rispettivi servizi separatamente.",
                ],
            },
            {
                "title": "Contatto",
                "items": [
                    "I recapiti mostrati servono solo alle comunicazioni relative alla casa e al soggiorno.",
                ],
            },
        ],
    },
}


def common_context(lang):
    return {
        "content": CONTENT[lang],
        "lang": lang,
        "supported_langs": SUPPORTED_LANGS,
    }


@app.route("/")
def index():
    lang = get_lang()
    context = common_context(lang)
    context.update(
        carousel_images=CAROUSEL_IMAGES,
        whatsapp_link=f"https://wa.me/{WHATSAPP_PHONE}" if WHATSAPP_PHONE else "#contact",
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
    context["history"] = HISTORY[lang]
    return render_template("history.html", **context)


@app.route("/bus")
def bus():
    lang = get_lang()
    context = common_context(lang)
    context["bus"] = BUS[lang]
    return render_template("bus.html", **context)


@app.route("/environment")
def environment():
    lang = get_lang()
    context = common_context(lang)
    context["environment"] = ENVIRONMENT[lang]
    return render_template("environment.html", **context)


@app.route("/guide")
def guide():
    lang = get_lang()
    context = common_context(lang)
    context["guide"] = GUIDE[lang]
    return render_template("guide.html", **context)


@app.route("/privacy")
def privacy():
    lang = get_lang()
    context = common_context(lang)
    context["legal"] = LEGAL[lang]
    return render_template("privacy.html", **context)


@app.route("/health")
def health_check():
    return jsonify(status="healthy"), 200


@app.errorhandler(Exception)
def handle_unexpected_exception(error):
    if isinstance(error, HTTPException):
        return error

    app.logger.error(
        "Unhandled Flask exception",
        exc_info=(type(error), error, error.__traceback__),
    )
    return "Internal Server Error", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082, debug=False)
'''

style_css = r'''/* Domus Biliacum - responsive lake-house design
   Drop-in replacement for static/css/style.css */

:root {
  --ink: #183035;
  --muted: #607177;
  --lake: #176f87;
  --lake-dark: #0d5267;
  --lake-soft: #e6f4f6;
  --pine: #2f6a55;
  --sand: #f4efe6;
  --paper: #fffdfa;
  --white: #ffffff;
  --line: rgba(24, 48, 53, 0.12);
  --shadow-sm: 0 8px 24px rgba(24, 48, 53, 0.08);
  --shadow: 0 18px 55px rgba(24, 48, 53, 0.14);
  --radius: 22px;
  --radius-sm: 14px;
  --container: 1180px;
}

* {
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
  scroll-padding-top: 96px;
}

body {
  margin: 0;
  color: var(--ink);
  background:
    radial-gradient(circle at 85% 5%, rgba(23, 111, 135, 0.08), transparent 28rem),
    var(--paper);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  line-height: 1.65;
  -webkit-font-smoothing: antialiased;
}

img {
  display: block;
  max-width: 100%;
}

a {
  color: inherit;
}

button,
a {
  -webkit-tap-highlight-color: transparent;
}

button,
input,
select,
textarea {
  font: inherit;
}

.container {
  width: min(calc(100% - 36px), var(--container));
  margin-inline: auto;
}

.site-header {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: rgba(255, 253, 250, 0.92);
  border-bottom: 1px solid rgba(24, 48, 53, 0.08);
  backdrop-filter: blur(18px);
}

.nav-wrap {
  min-height: 78px;
  display: flex;
  align-items: center;
  gap: 18px;
}

.brand {
  margin: 0;
  flex: 0 0 auto;
}

.brand a {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
}

.brand img {
  width: 40px;
  height: 40px;
  object-fit: contain;
}

.brand-name {
  font-size: 1rem;
  font-weight: 900;
  letter-spacing: 0.14em;
  color: var(--lake-dark);
}

.main-nav {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 4px;
}

.main-nav a {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-height: 42px;
  padding: 8px 10px;
  border-radius: 999px;
  color: var(--ink);
  text-decoration: none;
  font-size: 0.86rem;
  font-weight: 700;
  white-space: nowrap;
  transition: background 160ms ease, color 160ms ease, transform 160ms ease;
}

.main-nav a:hover {
  background: var(--lake-soft);
  color: var(--lake-dark);
  transform: translateY(-1px);
}

.nav-ico {
  font-size: 0.98rem;
}

.lang-switch {
  display: flex;
  align-items: center;
  gap: 4px;
  flex: 0 0 auto;
}

.lang-btn {
  display: grid;
  place-items: center;
  min-width: 34px;
  height: 34px;
  padding: 0 7px;
  border: 1px solid var(--line);
  border-radius: 999px;
  color: var(--muted);
  text-decoration: none;
  font-size: 0.76rem;
  font-weight: 900;
}

.lang-btn:hover,
.lang-btn.active {
  color: var(--white);
  background: var(--lake);
  border-color: var(--lake);
}

.nav-toggle {
  display: none;
  margin-left: auto;
  border: 1px solid var(--line);
  background: var(--white);
  border-radius: 999px;
  padding: 9px 14px;
  color: var(--ink);
  font-weight: 800;
  cursor: pointer;
}

.hero {
  position: relative;
  min-height: 68vh;
  display: grid;
  align-items: end;
  overflow: hidden;
  color: var(--white);
  background:
    linear-gradient(180deg, rgba(7, 31, 38, 0.17) 10%, rgba(7, 31, 38, 0.80) 100%),
    url("../images/carroussel/image%20copy%202.png") center 46% / cover no-repeat;
}

.hero-small {
  min-height: 390px;
  align-items: end;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(90deg, rgba(8, 37, 44, 0.45), transparent 62%),
    radial-gradient(circle at 70% 20%, rgba(255, 255, 255, 0.13), transparent 22rem);
  pointer-events: none;
}

.hero-content {
  position: relative;
  z-index: 1;
  padding-top: clamp(80px, 12vw, 150px);
  padding-bottom: clamp(54px, 8vw, 92px);
}

.hero-kicker,
.eyebrow {
  margin: 0 0 8px;
  color: rgba(255, 255, 255, 0.82);
  font-size: 0.78rem;
  font-weight: 900;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.eyebrow {
  color: var(--lake);
}

.hero h2 {
  margin: 0;
  font-family: Georgia, "Times New Roman", serif;
  font-size: clamp(3.3rem, 8vw, 7rem);
  line-height: 0.95;
  letter-spacing: -0.045em;
}

.hero-small h2 {
  max-width: 900px;
  font-size: clamp(2.3rem, 6vw, 4.6rem);
}

.hero-subtitle {
  max-width: 760px;
  margin: 20px 0 0;
  font-size: clamp(1.05rem, 2vw, 1.35rem);
  color: rgba(255, 255, 255, 0.91);
}

.poet-quote {
  max-width: 720px;
  margin: 18px 0 0;
  font-family: Georgia, "Times New Roman", serif;
  font-style: italic;
  color: rgba(255, 255, 255, 0.75);
}

.hero-actions,
.spotlight-actions,
.contact-actions {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 28px;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 9px;
  min-height: 46px;
  padding: 11px 18px;
  border: 1px solid transparent;
  border-radius: 999px;
  text-decoration: none;
  font-weight: 850;
  cursor: pointer;
  transition:
    transform 160ms ease,
    box-shadow 160ms ease,
    background 160ms ease,
    border-color 160ms ease;
}

.btn:hover {
  transform: translateY(-2px);
}

.btn-primary {
  color: var(--white);
  background: linear-gradient(135deg, var(--lake), var(--lake-dark));
  box-shadow: 0 10px 26px rgba(13, 82, 103, 0.26);
}

.btn-primary:hover {
  box-shadow: 0 15px 34px rgba(13, 82, 103, 0.33);
}

.btn-ghost {
  border-color: rgba(24, 48, 53, 0.17);
  color: var(--ink);
  background: rgba(255, 255, 255, 0.82);
}

.hero .btn-ghost {
  color: var(--white);
  border-color: rgba(255, 255, 255, 0.32);
  background: rgba(255, 255, 255, 0.10);
  backdrop-filter: blur(10px);
}

.btn-light {
  color: var(--lake-dark);
  background: var(--white);
  box-shadow: var(--shadow-sm);
}

.airbnb-logo,
.contact-icon {
  width: 22px;
  height: 22px;
  object-fit: contain;
}

.section {
  padding: clamp(64px, 8vw, 108px) 0;
}

.paper {
  background: linear-gradient(180deg, var(--sand), #f8f4ed);
  border-block: 1px solid rgba(24, 48, 53, 0.07);
}

.section-blue {
  color: var(--white);
  background:
    linear-gradient(135deg, rgba(13, 82, 103, 0.98), rgba(47, 106, 85, 0.96));
}

.section-blue .section-title,
.section-blue h3,
.section-blue h4 {
  color: var(--white);
}

.section-blue p {
  color: rgba(255, 255, 255, 0.82);
}

.section-title {
  margin: 0 0 24px;
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--ink);
  font-family: Georgia, "Times New Roman", serif;
  font-size: clamp(1.7rem, 3vw, 2.5rem);
  line-height: 1.12;
  letter-spacing: -0.025em;
}

.section-ico {
  font-family: system-ui, sans-serif;
  font-size: 0.82em;
}

.section-spotlight {
  padding-top: 0;
  position: relative;
  z-index: 2;
}

.spotlight-grid {
  margin-top: -46px;
  display: grid;
  grid-template-columns: 1.25fr 0.75fr;
  gap: 18px;
}

.spotlight-card {
  position: relative;
  padding: clamp(24px, 4vw, 38px);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: rgba(255, 253, 250, 0.96);
  box-shadow: var(--shadow);
  overflow: hidden;
}

.spotlight-card--primary::after {
  content: "";
  position: absolute;
  width: 220px;
  height: 220px;
  right: -90px;
  top: -100px;
  border-radius: 50%;
  background: rgba(23, 111, 135, 0.09);
}

.spotlight-card h3 {
  margin: 0 0 18px;
  font-family: Georgia, "Times New Roman", serif;
  font-size: clamp(1.5rem, 3vw, 2rem);
}

.check-list,
.card ul {
  margin: 0;
  padding: 0;
  list-style: none;
}

.check-list li,
.card li,
.guide-card li {
  position: relative;
  padding-left: 28px;
  margin: 10px 0;
}

.check-list li::before,
.card li::before,
.guide-card li::before {
  content: "✓";
  position: absolute;
  left: 0;
  top: 0;
  color: var(--pine);
  font-weight: 950;
}

.split {
  display: grid;
  grid-template-columns: minmax(280px, 0.72fr) minmax(0, 1.28fr);
  align-items: center;
  gap: clamp(30px, 6vw, 76px);
}

.house-media-row {
  min-width: 0;
  display: grid;
  grid-template-columns: 1fr 0.78fr;
  gap: 18px;
}

.framed {
  overflow: hidden;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--white);
  box-shadow: var(--shadow-sm);
}

.carousel {
  position: relative;
  min-width: 0;
}

.carousel-track-wrapper {
  overflow: hidden;
}

.carousel-track {
  position: relative;
  min-height: 420px;
}

.carousel-slide {
  position: absolute;
  inset: 0;
  margin: 0;
  opacity: 0;
  transform: scale(1.02);
  pointer-events: none;
  transition: opacity 350ms ease, transform 500ms ease;
}

.carousel-slide.active {
  opacity: 1;
  transform: scale(1);
  pointer-events: auto;
}

.carousel-slide img {
  width: 100%;
  height: 100%;
  min-height: 420px;
  object-fit: cover;
}

.carousel-btn {
  position: absolute;
  z-index: 3;
  top: 50%;
  transform: translateY(-50%);
  width: 44px;
  height: 44px;
  border: 0;
  border-radius: 50%;
  display: grid;
  place-items: center;
  color: var(--white);
  background: rgba(8, 37, 44, 0.65);
  backdrop-filter: blur(8px);
  cursor: pointer;
}

.carousel-btn:hover {
  background: rgba(8, 37, 44, 0.86);
}

.carousel-btn.prev {
  left: 14px;
}

.carousel-btn.next {
  right: 14px;
}

.carousel-dots {
  position: absolute;
  z-index: 3;
  left: 50%;
  bottom: 16px;
  transform: translateX(-50%);
  display: flex;
  gap: 7px;
  padding: 8px 10px;
  border-radius: 999px;
  background: rgba(8, 37, 44, 0.42);
  backdrop-filter: blur(8px);
}

.dot {
  width: 8px;
  height: 8px;
  padding: 0;
  border: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.55);
  cursor: pointer;
}

.dot.active {
  width: 22px;
  border-radius: 999px;
  background: var(--white);
}

.house-inline-video {
  min-height: 420px;
}

.video-placeholder {
  height: 100%;
  min-height: 420px;
  padding: 28px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  gap: 18px;
  color: var(--white);
  background:
    linear-gradient(180deg, rgba(8, 37, 44, 0.08), rgba(8, 37, 44, 0.86)),
    url("../images/carroussel/image%20copy%203.png") center / cover no-repeat;
}

.video-placeholder__media {
  display: grid;
  place-items: center;
  width: 70px;
  height: 70px;
  margin: auto;
  border: 1px solid rgba(255, 255, 255, 0.35);
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.14);
  backdrop-filter: blur(10px);
  font-size: 1.5rem;
}

.video-copy .eyebrow {
  color: rgba(255, 255, 255, 0.72);
}

.video-copy h4 {
  margin: 0;
  font-size: 1.25rem;
}

.video-copy p {
  color: rgba(255, 255, 255, 0.82);
}

.house-inline-video iframe {
  display: block;
  width: 100%;
  min-height: 420px;
  height: 100%;
  border: 0;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
}

.feature-card,
.card,
.scenic-card {
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: rgba(255, 255, 255, 0.86);
  box-shadow: var(--shadow-sm);
}

.feature-card {
  padding: 24px;
}

.feature-card h4,
.card h4,
.scenic-card h4 {
  margin: 0 0 10px;
  color: var(--ink);
  font-size: 1.05rem;
}

.feature-icon {
  display: grid;
  place-items: center;
  width: 46px;
  height: 46px;
  margin-bottom: 16px;
  border-radius: 14px;
  background: var(--lake-soft);
  font-size: 1.35rem;
}

.stat-label {
  margin: 0 0 8px;
  color: var(--muted);
  font-size: 0.78rem;
  font-weight: 850;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.stat-value {
  margin: 0;
  color: var(--ink);
  font-size: clamp(1.2rem, 2vw, 1.55rem);
  font-weight: 900;
  line-height: 1.2;
}

.grid-two {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}

.stay-cards {
  margin-top: 18px;
}

.card {
  padding: clamp(22px, 4vw, 32px);
}

.card h4 {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.35rem;
}

.scenic-grid {
  margin-top: 24px;
}

.scenic-card {
  overflow: hidden;
}

.scenic-card img {
  width: 100%;
  height: 310px;
  object-fit: cover;
}

.scenic-content {
  padding: 22px;
}

.contact-band {
  padding-top: 70px;
  padding-bottom: 70px;
}

.contact-grid {
  display: grid;
  grid-template-columns: 1.1fr auto;
  align-items: center;
  gap: 28px;
}

.site-footer {
  padding: 28px 0;
  border-top: 1px solid var(--line);
  background: #0d2e37;
  color: rgba(255, 255, 255, 0.76);
}

.footer-legal-wrap {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
}

.footer-links {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 14px;
}

.footer-links a,
.cookie-settings-btn {
  color: rgba(255, 255, 255, 0.82);
  text-decoration: none;
  font-size: 0.9rem;
}

.cookie-settings-btn {
  border: 0;
  padding: 0;
  background: none;
  cursor: pointer;
}

.footer-links a:hover,
.cookie-settings-btn:hover {
  color: var(--white);
}

.hidden-guide-link {
  opacity: 0.12;
  font-size: 0.7rem;
  text-decoration: none;
}

/* Guide / content pages */
.guide-page {
  min-height: 70vh;
}

.guide-actions {
  margin-top: 24px;
}

.guide-kpis {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.guide-sections {
  display: grid;
  gap: 18px;
}

.guide-sections--tabs .guide-tabs {
  display: grid;
  grid-template-columns: minmax(230px, 0.32fr) minmax(0, 0.68fr);
  align-items: start;
  gap: 24px;
}

.guide-tab-list {
  position: sticky;
  top: 102px;
  display: grid;
  gap: 8px;
}

.guide-tab-btn {
  width: 100%;
  display: grid;
  grid-template-columns: 30px 32px 1fr;
  align-items: center;
  gap: 8px;
  padding: 12px 14px;
  border: 1px solid var(--line);
  border-radius: 14px;
  color: var(--ink);
  text-align: left;
  background: rgba(255, 255, 255, 0.76);
  cursor: pointer;
  transition: transform 150ms ease, background 150ms ease, color 150ms ease;
}

.guide-tab-btn:hover {
  transform: translateX(3px);
  background: var(--lake-soft);
}

.guide-tab-btn.active {
  color: var(--white);
  border-color: var(--lake);
  background: linear-gradient(135deg, var(--lake), var(--lake-dark));
  box-shadow: 0 10px 26px rgba(13, 82, 103, 0.20);
}

.guide-tab-index {
  font-size: 0.78rem;
  font-weight: 900;
  opacity: 0.72;
}

.guide-tab-icon {
  font-size: 1.15rem;
}

.guide-tab-panel {
  min-height: 270px;
}

.guide-tab-panel[hidden] {
  display: none !important;
}

.house-gallery {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}

.house-photo {
  margin: 0;
  overflow: hidden;
  border-radius: var(--radius);
  box-shadow: var(--shadow-sm);
}

.house-photo img {
  width: 100%;
  height: 420px;
  object-fit: cover;
  transition: transform 500ms ease;
}

.house-photo:hover img {
  transform: scale(1.025);
}

.cookie-banner {
  position: fixed;
  z-index: 2000;
  left: 50%;
  bottom: 18px;
  width: min(calc(100% - 28px), 760px);
  transform: translateX(-50%);
  padding: 18px;
  border: 1px solid var(--line);
  border-radius: 18px;
  background: rgba(255, 253, 250, 0.97);
  box-shadow: 0 25px 70px rgba(8, 37, 44, 0.25);
  backdrop-filter: blur(18px);
}

.cookie-banner[hidden] {
  display: none !important;
}

.cookie-banner p {
  margin: 0;
  color: var(--muted);
}

.cookie-actions {
  display: flex;
  gap: 10px;
  margin-top: 14px;
}

.cookie-decline {
  background: var(--white);
}

/* Keyboard accessibility */
a:focus-visible,
button:focus-visible {
  outline: 3px solid rgba(23, 111, 135, 0.32);
  outline-offset: 3px;
}

/* Tablets */
@media (max-width: 1120px) {
  .nav-toggle {
    display: inline-flex;
  }

  .main-nav {
    position: absolute;
    top: calc(100% + 1px);
    left: 18px;
    right: 18px;
    display: none;
    max-height: min(72vh, 620px);
    overflow: auto;
    padding: 12px;
    border: 1px solid var(--line);
    border-radius: 18px;
    background: rgba(255, 253, 250, 0.98);
    box-shadow: var(--shadow);
  }

  .main-nav.open {
    display: grid;
  }

  .main-nav a {
    width: 100%;
    border-radius: 12px;
    padding: 10px 12px;
  }

  .lang-switch {
    margin-left: 0;
  }

  .split {
    grid-template-columns: 1fr;
  }

  .house-media-row {
    grid-template-columns: 1fr 1fr;
  }

  .feature-grid,
  .guide-kpis {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

/* Mobile */
@media (max-width: 760px) {
  .container {
    width: min(calc(100% - 24px), var(--container));
  }

  .nav-wrap {
    min-height: 68px;
    gap: 10px;
  }

  .brand-name {
    display: none;
  }

  .brand img {
    width: 36px;
    height: 36px;
  }

  .lang-btn {
    min-width: 31px;
    height: 31px;
    font-size: 0.71rem;
  }

  .nav-toggle {
    padding: 8px 12px;
  }

  .hero {
    min-height: 600px;
  }

  .hero-small {
    min-height: 340px;
  }

  .hero-content {
    padding-top: 95px;
    padding-bottom: 54px;
  }

  .hero h2 {
    font-size: clamp(3rem, 17vw, 5rem);
  }

  .hero-small h2 {
    font-size: clamp(2.2rem, 11vw, 3.8rem);
  }

  .section {
    padding: 58px 0;
  }

  .section-spotlight {
    padding-top: 0;
  }

  .spotlight-grid {
    margin-top: -28px;
    grid-template-columns: 1fr;
  }

  .house-media-row,
  .grid-two,
  .feature-grid,
  .guide-kpis,
  .contact-grid,
  .house-gallery {
    grid-template-columns: 1fr;
  }

  .carousel-track,
  .carousel-slide img,
  .house-inline-video,
  .video-placeholder,
  .house-inline-video iframe {
    min-height: 330px;
  }

  .scenic-card img,
  .house-photo img {
    height: 300px;
  }

  .guide-sections--tabs .guide-tabs {
    grid-template-columns: 1fr;
  }

  .guide-tab-list {
    position: static;
    display: flex;
    overflow-x: auto;
    padding-bottom: 6px;
    scrollbar-width: thin;
  }

  .guide-tab-btn {
    min-width: 245px;
  }

  .footer-legal-wrap {
    align-items: flex-start;
    flex-direction: column;
  }

  .contact-actions,
  .hero-actions {
    align-items: stretch;
  }

  .contact-actions .btn,
  .hero-actions .btn {
    width: 100%;
  }

  .cookie-actions {
    flex-direction: column;
  }

  .cookie-actions .btn {
    width: 100%;
  }
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    scroll-behavior: auto !important;
    transition-duration: 0.001ms !important;
    animation-duration: 0.001ms !important;
    animation-iteration-count: 1 !important;
  }
}
'''

main_js = r'''(() => {
  "use strict";

  /* Mobile navigation */
  const navToggle = document.querySelector(".nav-toggle");
  const mainNav = document.querySelector(".main-nav");

  if (navToggle && mainNav) {
    navToggle.addEventListener("click", () => {
      const open = mainNav.classList.toggle("open");
      navToggle.setAttribute("aria-expanded", String(open));
    });

    mainNav.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        mainNav.classList.remove("open");
        navToggle.setAttribute("aria-expanded", "false");
      });
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        mainNav.classList.remove("open");
        navToggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* Carousels */
  document.querySelectorAll("[data-carousel]").forEach((carousel) => {
    const slides = [...carousel.querySelectorAll(".carousel-slide")];
    const dots = [...carousel.querySelectorAll(".dot")];
    const prev = carousel.querySelector(".prev");
    const next = carousel.querySelector(".next");

    if (!slides.length) return;

    let index = Math.max(0, slides.findIndex((slide) => slide.classList.contains("active")));

    const render = () => {
      slides.forEach((slide, i) => slide.classList.toggle("active", i === index));
      dots.forEach((dot, i) => {
        dot.classList.toggle("active", i === index);
        dot.setAttribute("aria-current", i === index ? "true" : "false");
      });
    };

    const move = (delta) => {
      index = (index + delta + slides.length) % slides.length;
      render();
    };

    prev?.addEventListener("click", () => move(-1));
    next?.addEventListener("click", () => move(1));

    dots.forEach((dot, i) => {
      dot.addEventListener("click", () => {
        index = i;
        render();
      });
    });

    render();
  });

  /* Tabs used by guide, bus and environment */
  document.querySelectorAll("[data-tabs]").forEach((tabs) => {
    const buttons = [...tabs.querySelectorAll("[data-tab-btn]")];
    const panels = [...tabs.querySelectorAll("[data-tab-panel]")];

    const activate = (index, focus = false) => {
      buttons.forEach((button, i) => {
        const active = i === index;
        button.classList.toggle("active", active);
        button.setAttribute("aria-selected", String(active));
        button.tabIndex = active ? 0 : -1;
        if (active && focus) button.focus();
      });

      panels.forEach((panel, i) => {
        panel.hidden = i !== index;
      });
    };

    buttons.forEach((button, index) => {
      button.addEventListener("click", () => activate(index));

      button.addEventListener("keydown", (event) => {
        if (!["ArrowRight", "ArrowDown", "ArrowLeft", "ArrowUp", "Home", "End"].includes(event.key)) {
          return;
        }

        event.preventDefault();

        let nextIndex = index;
        if (event.key === "ArrowRight" || event.key === "ArrowDown") {
          nextIndex = (index + 1) % buttons.length;
        } else if (event.key === "ArrowLeft" || event.key === "ArrowUp") {
          nextIndex = (index - 1 + buttons.length) % buttons.length;
        } else if (event.key === "Home") {
          nextIndex = 0;
        } else if (event.key === "End") {
          nextIndex = buttons.length - 1;
        }

        activate(nextIndex, true);
      });
    });

    activate(Math.max(0, buttons.findIndex((button) => button.classList.contains("active"))));
  });

  /* Privacy-friendly YouTube loader */
  document.querySelectorAll("[data-video-placeholder]").forEach((placeholder) => {
    const button = placeholder.querySelector("[data-load-video]");
    if (!button) return;

    button.addEventListener("click", () => {
      const videoId = button.dataset.videoId;
      if (!videoId) return;

      const iframe = document.createElement("iframe");
      iframe.src =
        `https://www.youtube-nocookie.com/embed/${encodeURIComponent(videoId)}` +
        "?autoplay=1&modestbranding=1&rel=0";
      iframe.title = "Video";
      iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
      iframe.allowFullscreen = true;

      const wrapper = placeholder.closest(".house-inline-video") || placeholder.parentElement;
      wrapper.replaceChildren(iframe);
    });
  });

  /* Minimal consent memory. No analytics are loaded here. */
  const CONSENT_KEY = "bilieu-cookie-choice";
  const banner = document.querySelector("[data-cookie-banner]");
  const accept = document.querySelector("[data-cookie-accept]");
  const decline = document.querySelector("[data-cookie-decline]");
  const settingsButtons = document.querySelectorAll(".cookie-settings-btn");

  const showBanner = () => {
    if (banner) banner.hidden = false;
  };

  const hideBanner = () => {
    if (banner) banner.hidden = true;
  };

  if (banner && !localStorage.getItem(CONSENT_KEY)) {
    showBanner();
  }

  accept?.addEventListener("click", () => {
    localStorage.setItem(CONSENT_KEY, "accepted");
    hideBanner();
  });

  decline?.addEventListener("click", () => {
    localStorage.setItem(CONSENT_KEY, "declined");
    hideBanner();
  });

  settingsButtons.forEach((button) => {
    button.addEventListener("click", () => {
      localStorage.removeItem(CONSENT_KEY);
      showBanner();
    });
  });
})();
'''

readme = r'''DOMUS BILIACUM - improved version

Files:
- app.py                         richer FR/EN/IT content + all Flask routes
- templates/*.html               your existing templates
- static/css/style.css           new responsive design
- static/js/main.js              menu, carousel, tabs, video and cookie behavior

Deploy:
1. Replace app.py
2. Replace static/css/style.css
3. Replace static/js/main.js
4. Keep/copy the templates in templates/
5. Ensure these existing images are present:
   static/images/carroussel/image.png
   static/images/carroussel/image copy.png
   static/images/carroussel/image copy 2.png
   static/images/carroussel/image copy 3.png

Optional environment variables in docker-compose.yml:
  AIRBNB_URL=https://www.airbnb.fr/rooms/1402915287163928554
  CONTACT_EMAIL=your-email@example.com
  WHATSAPP_PHONE=336XXXXXXXX

Then:
  docker compose down
  docker compose up -d --build

Health check:
  curl -i http://127.0.0.1:8082/health
'''

(root / "app.py").write_text(app_py, encoding="utf-8")
(static_css / "style.css").write_text(style_css, encoding="utf-8")
(static_js / "main.js").write_text(main_js, encoding="utf-8")
(root / "README.txt").write_text(readme, encoding="utf-8")

# Validate the Python file syntax.
import py_compile
py_compile.compile(str(root / "app.py"), doraise=True)

# Validate route rendering with Flask's test client.
# Temporarily add package root to import path and import app.py by path.
import importlib.util, sys
spec = importlib.util.spec_from_file_location("bilieu_test_app", root / "app.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.app.template_folder = str(templates_dir)

results = {}
with mod.app.test_client() as client:
    for route in ["/", "/photos", "/history", "/bus", "/environment", "/guide", "/privacy", "/health"]:
        resp = client.get(route)
        results[route] = resp.status_code

# Package ZIP.
zip_path = Path("/mnt/data/bilieu_improved.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for p in root.rglob("*"):
        if p.is_file():
            z.write(p, p.relative_to(root))

print("Created:")
print(root / "app.py")
print(static_css / "style.css")
print(static_js / "main.js")
print(zip_path)
print("Route tests:", results)
