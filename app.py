import logging
import os
from copy import deepcopy

from flask import Flask, Response, jsonify, render_template, request
from werkzeug.exceptions import HTTPException


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
app.logger.setLevel(logging.INFO)

SUPPORTED_LANGS = ["fr", "en", "it", "es"]
ADSENSE_CLIENT = os.getenv("ADSENSE_CLIENT", "ca-pub-6158185990205930").strip()
AD_PAGES = {"index": "home", "house_photos": "content", "history": "content", "environment": "content"}
AD_COPY = {
    "fr": {"label": "Publicité"},
    "en": {"label": "Advertisement"},
    "it": {"label": "Pubblicità"},
    "es": {"label": "Publicidad"},
}

AIRBNB_URL = os.getenv(
    "AIRBNB_URL",
    "https://www.airbnb.fr/rooms/1402915287163928554",
)
CONTACT_EMAIL = os.getenv("CONTACT_EMAIL", "admin@audeladedonnees.fr")
WHATSAPP_PHONE = (
    os.getenv("WHATSAPP_PHONE", "+33 7 64 14 20 31")
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

AIRBNB_IMAGES = [
    {"src": "images/airbnb/airbnb-01.jpeg", "alt": "Vue de la maison et du lac"},
    {"src": "images/airbnb/airbnb-02.jpeg", "alt": "Salon de la maison"},
    {"src": "images/airbnb/airbnb-03.jpeg", "alt": "Chambre de la maison"},
    {"src": "images/airbnb/airbnb-04.jpeg", "alt": "Cuisine équipée"},
    {"src": "images/airbnb/airbnb-05.jpeg", "alt": "Vue sur le lac de Paladru"},
    {"src": "images/airbnb/airbnb-06.jpeg", "alt": "Espace extérieur de la maison"},
    {"src": "images/airbnb/airbnb-07.jpeg", "alt": "Détail de l'intérieur"},
]


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
            "internet_title": "Internet & télévision",
            "wifi_name_label": "Nom du Wi-Fi",
            "wifi_password_label": "Mot de passe",
            "wifi_name": "Bbox–1202F156",
            "wifi_password": "R1cLfqRR14heKTwCV9",
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
                        "Climatisation uniquement au dernier étage ; contactez-nous pour confirmer sa disponibilité.",
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
            "internet_title": "Internet & television",
            "wifi_name_label": "Wi-Fi name",
            "wifi_password_label": "Password",
            "wifi_name": "Bbox–1202F156",
            "wifi_password": "R1cLfqRR14heKTwCV9",
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
                        "Air conditioning is only on the top floor; please contact us to confirm availability.",
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
            "internet_title": "Internet e televisione",
            "wifi_name_label": "Nome Wi-Fi",
            "wifi_password_label": "Password",
            "wifi_name": "Bbox–1202F156",
            "wifi_password": "R1cLfqRR14heKTwCV9",
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
                        "Aria condizionata solo all'ultimo piano; contattateci per confermarne la disponibilità.",
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
                    "Mot de passe Wi-Fi : R1cLfqRR14heKTwCV9.",
                    "La Smart TV est disponible pour vos usages habituels.",
                    "Le site ne charge les médias externes qu'à votre demande afin de limiter les chargements tiers.",
                ],
            },
            {
                "title": "Chauffage & climatisation",
                "items": [
                    "Le poêle à granulés peut être piloté avec l'application MCZ.",
                    "La climatisation est disponible uniquement au dernier étage.",
                    "Contactez-nous pour confirmer la disponibilité de la climatisation avant votre séjour.",
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
                    "La maison est également habitée par ses propriétaires : merci de respecter leurs effets personnels et de ne pas les déplacer.",
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
                    "La propreté est fondamentale : laissez chaque espace propre et rangé afin de présenter la maison dans un bon état aux prochains visiteurs.",
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
                    "Wi-Fi password: R1cLfqRR14heKTwCV9.",
                    "Smart TV is available for normal guest use.",
                    "External media on the website is loaded only on request to reduce third-party loading.",
                ],
            },
            {
                "title": "Heating & air conditioning",
                "items": [
                    "The pellet stove can be controlled through the MCZ app.",
                    "Air conditioning is available only on the top floor.",
                    "Please contact us to confirm air conditioning availability before your stay.",
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
                    "The house is also inhabited by its owners; please respect their personal belongings and do not move them.",
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
                    "Keeping the house clean is essential: leave every used area clean and tidy so it is in good condition for the next visitors.",
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
                    "Password Wi-Fi: R1cLfqRR14heKTwCV9.",
                    "Smart TV disponibile per l'uso normale degli ospiti.",
                    "I media esterni del sito vengono caricati solo su richiesta per limitare i contenuti di terze parti.",
                ],
            },
            {
                "title": "Riscaldamento & aria condizionata",
                "items": [
                    "La stufa a pellet può essere controllata tramite l'app MCZ.",
                    "L'aria condizionata è disponibile solo all'ultimo piano.",
                    "Contattateci per confermare la disponibilità dell'aria condizionata prima del soggiorno.",
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
                    "La casa è abitata anche dai proprietari: rispettate i loro effetti personali e non spostateli.",
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
                    "La pulizia è fondamentale: lasciare ogni spazio utilizzato pulito e ordinato, così la casa sarà in buone condizioni per i prossimi ospiti.",
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
    ad_page = AD_PAGES.get(request.endpoint)
    return {
        "content": CONTENT[lang],
        "lang": lang,
        "supported_langs": SUPPORTED_LANGS,
        "ad_client": ADSENSE_CLIENT if ad_page else "",
        "ad_slot": os.getenv(f"ADSENSE_SLOT_{ad_page.upper()}", "").strip() if ad_page else "",
        "ad_copy": AD_COPY[lang],
    }


SUPPORT = {
    "fr": {
        "title": "Soutenir les enfants atteints de cancer",
        "intro": "Un geste choisi librement peut aider la recherche, les soins et l'accompagnement des enfants et de leurs familles.",
        "kicker": "Une attention qui compte",
        "cta": "Découvrir les instituts",
        "note": "Les dons sont réalisés directement sur les sites officiels des instituts. Bilieu ne collecte aucun paiement.",
        "institutes": [
            {"name": "Centre Léon Bérard", "place": "Lyon", "text": "Soutenir la recherche contre le cancer et les équipes qui accompagnent les jeunes patients.", "url": "https://soutenir.centreleonberard.fr/", "label": "Donner au Centre Léon Bérard"},
            {"name": "Gustave Roussy", "place": "Villejuif", "text": "Contribuer directement aux programmes de recherche et de soins contre les cancers de l'enfant.", "url": "https://www.gustaveroussy.fr/fr/faire-un-don-contre-les-cancers-enfants", "label": "Donner à Gustave Roussy"},
        ],
    },
    "en": {
        "title": "Support children with cancer",
        "intro": "A freely chosen gift can help research, care and support for children and their families.",
        "kicker": "A little care can matter",
        "cta": "Discover the institutes",
        "note": "Donations are made directly on each institute's official website. Bilieu does not collect payments.",
        "institutes": [
            {"name": "Centre Léon Bérard", "place": "Lyon", "text": "Support cancer research and the teams caring for young patients.", "url": "https://soutenir.centreleonberard.fr/", "label": "Donate to Centre Léon Bérard"},
            {"name": "Gustave Roussy", "place": "Villejuif", "text": "Support research and care programmes dedicated to childhood cancer.", "url": "https://www.gustaveroussy.fr/fr/faire-un-don-contre-les-cancers-enfants", "label": "Donate to Gustave Roussy"},
        ],
    },
    "it": {
        "title": "Sostenere i bambini malati di cancro",
        "intro": "Un gesto scelto liberamente può aiutare la ricerca, le cure e il sostegno ai bambini e alle loro famiglie.",
        "kicker": "Un gesto che conta",
        "cta": "Scopri gli istituti",
        "note": "Le donazioni vengono effettuate direttamente sui siti ufficiali degli istituti. Bilieu non raccoglie pagamenti.",
        "institutes": [
            {"name": "Centre Léon Bérard", "place": "Lione", "text": "Sostenere la ricerca contro il cancro e le équipe che accompagnano i giovani pazienti.", "url": "https://soutenir.centreleonberard.fr/", "label": "Dona al Centre Léon Bérard"},
            {"name": "Gustave Roussy", "place": "Villejuif", "text": "Contribuire ai programmi di ricerca e cura contro i tumori infantili.", "url": "https://www.gustaveroussy.fr/fr/faire-un-don-contre-les-cancers-enfants", "label": "Dona a Gustave Roussy"},
        ],
    },
}

# Spanish keeps the complete existing guide structure while translating the most visible and house-specific content.
CONTENT["es"] = deepcopy(CONTENT["en"])
CONTENT["es"].update(
    meta_title="Domus Biliacum · Bilieu y lago de Paladru",
    nav={
        "house": "Casa Airbnb", "house_photos": "Fotos de la casa", "history": "Historia de Bilieu",
        "bus": "Líneas de autobús", "environment": "Medio ambiente", "services": "Servicios y comercios",
        "beauties": "Lago de Paladru", "contact": "Contacto",
    },
)
SUPPORT["es"] = {
    "title": "Apoyar a los niños con cáncer",
    "intro": "Un donativo elegido libremente puede ayudar a la investigación, los cuidados y el apoyo a los niños y sus familias.",
    "kicker": "Un gesto que cuenta", "cta": "Descubrir los institutos",
    "note": "Las donaciones se realizan directamente en los sitios oficiales de cada instituto. Bilieu no recibe ningún pago.",
    "institutes": [
        {"name": "Centre Léon Bérard", "place": "Lyon", "text": "Apoya la investigación contra el cáncer y a los equipos que acompañan a los pacientes jóvenes.", "url": "https://soutenir.centreleonberard.fr/", "label": "Donar al Centre Léon Bérard"},
        {"name": "Gustave Roussy", "place": "Villejuif", "text": "Contribuye a los programas de investigación y cuidados contra el cáncer infantil.", "url": "https://www.gustaveroussy.fr/fr/faire-un-don-contre-les-cancers-enfants", "label": "Donar a Gustave Roussy"},
    ],
}
for localized_data in (HISTORY, BUS, ENVIRONMENT, GUIDE, LEGAL):
    localized_data["es"] = deepcopy(localized_data["en"])
for language, cookie_text, choice_text, title, ad_text in (
    ("fr", "Les choix relatifs aux annonces sont gérés par la plateforme de consentement de Google sur les pages de découverte.", "La plateforme conserve votre choix dans votre navigateur.", "Publicité", "Les pages de découverte peuvent charger des annonces Google AdSense. Google et ses partenaires peuvent utiliser des cookies ou identifiants pour afficher et mesurer ces annonces selon votre choix. Vous pouvez modifier ce choix via le lien de gestion des cookies."),
    ("en", "Advertising choices are managed by Google's consent platform on discovery pages.", "The platform stores your choice in your browser.", "Advertising", "Discovery pages may load Google AdSense ads. Google and its partners may use cookies or identifiers to display and measure those ads according to your choice. You can change it using the cookie settings link."),
    ("it", "Le scelte relative agli annunci sono gestite dalla piattaforma di consenso di Google nelle pagine da esplorare.", "La piattaforma conserva la scelta nel browser.", "Pubblicità", "Le pagine da esplorare possono caricare annunci Google AdSense. Google e i suoi partner possono usare cookie o identificatori per mostrarli e misurarli in base alla tua scelta. Puoi modificarla dal link per la gestione dei cookie."),
    ("es", "Las opciones sobre anuncios se gestionan mediante la plataforma de consentimiento de Google en las páginas de descubrimiento.", "La plataforma guarda tu elección en el navegador.", "Publicidad", "Las páginas de descubrimiento pueden cargar anuncios de Google AdSense. Google y sus socios pueden usar cookies o identificadores para mostrarlos y medirlos según tu elección. Puedes cambiarla en el enlace de configuración de cookies."),
):
    LEGAL[language]["sections"][0]["items"][0] = cookie_text
    LEGAL[language]["sections"][0]["items"][1] = choice_text
    LEGAL[language]["sections"].append({"title": title, "items": [ad_text]})
GUIDE["es"].update(
    title="Guía de la estancia",
    intro="Todo lo necesario antes y durante la estancia: llegada, aparcamiento, acceso, habitaciones, equipamiento y normas importantes de la casa.",
)
GUIDE["es"]["sections"][7]["items"][1] = "La casa también está habitada por sus propietarios: respete sus objetos personales y no los mueva."
GUIDE["es"]["sections"][-1]["items"][2] = "La limpieza es fundamental: deje cada espacio utilizado limpio y ordenado para que la casa esté en buen estado para los próximos visitantes."
GUIDE["es"]["kpis"] = [
    {"label": "Entrada", "value": "15:00"},
    {"label": "Salida", "value": "10:00"},
    {"label": "Silencio", "value": "22:00–08:00"},
    {"label": "Aparcamiento", "value": "Público gratuito"},
]
GUIDE["es"]["sections"] = [
    {"title": "Llegada y acceso a la casa", "items": [
        "Entrada a partir de las 15:00.", "Hay aparcamiento público gratuito en la calle.",
        "Después de aparcar, tome el camino de hierba y grava.",
        "Siga la valla de madera hasta la casa.",
        "Busque el gran ventanal y la puerta de madera con cristales cuadrados.",
    ]},
    {"title": "Aparcamiento, vecinos y derecho de paso", "items": [
        "No bloquee la zona frente a la casa: es un derecho de paso.",
        "No aparque ni deje objetos en el terreno del vecino.",
        "Respete la tranquilidad del vecindario, especialmente entre las 22:00 y las 08:00.",
        "No está permitido cargar vehículos eléctricos en los enchufes de la casa.",
    ]},
    {"title": "Camas y ropa de cama", "items": [
        "Capacidad máxima indicada: 7 personas.",
        "Entrada y salón: sofá cama cómodo para 2 personas.",
        "Primera planta: despacho y habitación con 1 cama individual.",
        "Segunda planta: habitación con 1 cama individual y 1 sillón cama.",
        "Segunda planta: otra habitación con 1 cama doble.",
        "No se proporcionan sábanas, mantas ni toallas; tráigalas consigo.",
    ]},
    {"title": "Equipamiento de la casa", "items": [
        "Red Wi-Fi: Bbox–1202F156.", "Hay una Smart TV.",
        "Estufa de pellets controlable mediante la aplicación MCZ.",
        "Lavadora en el baño de la última planta.",
        "Despacho con pantalla, teclado y ratón.",
        "Hay barreras de seguridad para las escaleras.",
    ]},
    {"title": "Wi-Fi y televisión", "items": [
        "Red Wi-Fi: Bbox–1202F156.", "Contraseña Wi-Fi: R1cLfqRR14heKTwCV9.",
        "La Smart TV está disponible para el uso habitual de los huéspedes.",
        "Los contenidos externos del sitio web solo se cargan cuando usted los solicita.",
    ]},
    {"title": "Calefacción y aire acondicionado", "items": [
        "La estufa de pellets se controla con la aplicación MCZ.",
        "El aire acondicionado solo está en la última planta.",
        "Contáctenos para confirmar su disponibilidad antes de la estancia.",
    ]},
    {"title": "Mascotas", "items": [
        "Las mascotas son bienvenidas.",
        "Limpie después de ellas dentro y alrededor de la casa.",
        "Evite que molesten a los vecinos u obstaculicen las zonas de paso.",
    ]},
    {"title": "Seguridad y normas de la casa", "items": [
        "Está estrictamente prohibido fumar en la casa.",
        "Los propietarios también viven en la casa: respete sus objetos personales y no los mueva.",
        "Se pide silencio de 22:00 a 08:00.",
        "Mantenga libres los pasillos y las escaleras.",
        "Hay barreras de seguridad para las escaleras si las necesita.",
        "No cargue vehículos eléctricos en los enchufes domésticos.",
    ]},
    {"title": "Entorno y vida local", "items": [
        "Respete el lago, los espacios naturales y las propiedades privadas.",
        "Reduzca los residuos y siga las instrucciones locales de reciclaje.",
        "Para comprar, Casino Charavines está en 25 Avenue du Lac, 38850 Charavines.",
        "Consulte los horarios oficiales antes de usar el transporte público.",
    ]},
    {"title": "Antes de salir", "items": [
        "Salida a más tardar a las 10:00.",
        "Compruebe que ha recogido todos sus objetos personales.",
        "Deje limpios y ordenados todos los espacios utilizados para los próximos huéspedes.",
        "Si viaja con una mascota, limpie las zonas que haya utilizado.",
        "No deje nada en el derecho de paso ni en el terreno del vecino.",
    ]},
]

# Keep the arrival reminders and the full web guide in one localized source.
GUIDE_UPDATES = {
    "fr": {
        "parking": [
            "Merci de stationner uniquement sur les places publiques de la rue, près de la haie. Il n'y a pas de parking privé.",
            "Le terrain devant la maison appartient au voisin. Le droit de passage permet de rejoindre la maison à pied, sans s'y arrêter ni y déposer d'affaires.",
            "Pour préserver l'accès de chacun, merci de ne pas garer de voiture, même brièvement, sur ce terrain ou dans le passage.",
            "Gardez vos animaux avec vous et ramassez leurs déjections, y compris aux abords du passage.",
            "En cas de doute sur une place ou une limite de propriété, contactez-nous avant de vous garer.",
        ],
        "stove": [
            "Un téléphone mis à disposition dans la maison permet d'allumer et de régler le poêle à granulés avec l'application MCZ.",
            "Ouvrez l'application MCZ sur ce téléphone et ajustez la température selon votre confort. Si le poêle ne répond pas, contactez-nous plutôt que de modifier ses réglages techniques.",
            "Quelques granulés sont stockés dans le petit placard extérieur. Merci de nous prévenir si le stock est presque épuisé.",
        ],
        "extras": {
            3: ["Des jouets, des livres et un appareil à raclette sont à votre disposition ; merci de les ranger après usage."],
            7: ["Le tableau électrique se trouve au rez-de-chaussée ; merci de ne pas toucher aux disjoncteurs et de nous contacter en cas de problème.", "Merci de respecter les affiches et espaces personnels décorés par les enfants."],
            8: [
                "Si besoin, la poubelle grise pour les déchets organiques se trouve à gauche, à l'entrée du chemin.",
                "La poubelle jaune se trouve à l'entrée de la maison.",
                "À proximité : plage du camping à environ 2 minutes à pied et plage municipale de Paladru à environ 5 minutes en voiture.",
            ],
            9: ["Éteignez les lumières en quittant une pièce et débranchez les câbles USB inutilisés.", "Un aspirateur est à votre disposition pour laisser la maison propre."],
        },
        "highlights": {
            "parking_title": "Stationnement & droit de passage",
            "parking_text": "Garez votre voiture sur les places publiques de la rue, près de la haie. Le terrain devant la maison appartient au voisin : empruntez-le seulement pour rejoindre la maison à pied, sans stationner ni déposer d'affaires. Merci de préserver sa tranquillité et de nous contacter en cas de doute.",
            "stove_title": "Régler le poêle à granulés",
            "stove_text": "Utilisez le téléphone mis à disposition dans la maison : ouvrez l'application MCZ pour allumer le poêle et ajuster la température. Des granulés sont dans le petit placard extérieur ; contactez-nous si vous avez besoin d'aide.",
            "guide_title": "Guide complet du séjour",
            "guide_intro": "Retrouvez ici toutes les informations pratiques de la maison. Le PDF illustré reste disponible pour les photos d'arrivée.",
            "pdf_label": "Voir le guide PDF illustré",
            "parking_photo": "Places publiques le long de la haie : stationnez uniquement là où le stationnement est autorisé.",
            "path_photo": "Chemin en herbe et gravier à suivre à pied le long de la clôture en bois.",
        },
    },
    "en": {
        "parking": [
            "Please park only in the public street spaces beside the hedge. There is no private parking.",
            "The land in front of the house belongs to the neighbour. The right of way is for walking to the house, without stopping or leaving belongings there.",
            "To keep access clear for everyone, please do not park a car there, even briefly, or block the path.",
            "Please keep pets with you and clean up after them, including near the path.",
            "If you are unsure about a parking space or property boundary, please contact us before parking.",
        ],
        "stove": [
            "A phone provided in the house lets you switch on and adjust the pellet stove through the MCZ app.",
            "Open the MCZ app on that phone and adjust the temperature to your comfort. If the stove does not respond, contact us instead of changing technical settings.",
            "Some pellets are stored in the small outdoor cupboard. Please let us know when the supply is running low.",
        ],
        "extras": {
            3: ["Toys, books and a raclette machine are available; please put them away after use."],
            7: ["The electrical panel is on the ground floor; please leave the breakers as they are and contact us if there is a problem.", "Please respect the children's decorated posters and personal spaces."],
            8: [
                "If needed, the grey bin for organic waste is on the left at the entrance to the path.",
                "The yellow bin is at the entrance to the house.",
                "Nearby: the campsite beach is about a 2-minute walk away, and Paladru municipal beach is about a 5-minute drive away.",
            ],
            9: ["Turn off lights when leaving a room and unplug unused USB cables.", "A vacuum cleaner is available to help leave the house clean."],
        },
        "highlights": {
            "parking_title": "Parking & right of way",
            "parking_text": "Park in the public street spaces beside the hedge. The land in front of the house belongs to the neighbour: please cross it only on foot to reach the house, without parking or leaving belongings. Thank you for respecting their space; contact us if you are unsure.",
            "stove_title": "Adjusting the pellet stove",
            "stove_text": "Use the phone provided in the house. Open the MCZ app to switch on the stove and adjust the temperature. Pellets are in the small outdoor cupboard; contact us if you need help.",
            "guide_title": "Complete guest guide",
            "guide_intro": "All practical house information is here. The illustrated PDF is also available for arrival photos.",
            "pdf_label": "View the illustrated PDF guide",
            "parking_photo": "Public spaces beside the hedge: park only where parking is permitted.",
            "path_photo": "Follow the grass and gravel path on foot beside the wooden fence.",
        },
    },
    "it": {
        "parking": [
            "Vi preghiamo di parcheggiare solo nei posti pubblici lungo la strada, accanto alla siepe. Non c'è un parcheggio privato.",
            "Il terreno davanti alla casa appartiene al vicino. La servitù di passaggio consente di raggiungere la casa a piedi, senza fermarsi o lasciare oggetti.",
            "Per mantenere libero l'accesso, vi chiediamo di non parcheggiare lì, nemmeno per poco tempo, e di non bloccare il passaggio.",
            "Tenete con voi gli animali e raccogliete le loro deiezioni, anche vicino al passaggio.",
            "Se avete dubbi su un posto auto o sui confini della proprietà, contattateci prima di parcheggiare.",
        ],
        "stove": [
            "Un telefono disponibile in casa permette di accendere e regolare la stufa a pellet tramite l'app MCZ.",
            "Aprite l'app MCZ su quel telefono e regolate la temperatura secondo le vostre esigenze. Se la stufa non risponde, contattateci senza modificare le impostazioni tecniche.",
            "Alcuni pellet si trovano nel piccolo armadietto esterno. Avvisateci se la scorta sta finendo.",
        ],
        "extras": {
            3: ["Sono disponibili giocattoli, libri e una macchina per raclette; riponeteli dopo l'uso."],
            7: ["Il quadro elettrico è al piano terra; non toccate gli interruttori e contattateci in caso di problemi.", "Vi preghiamo di rispettare i poster e gli spazi personali decorati dai bambini."],
            8: [
                "Se necessario, il bidone grigio per i rifiuti organici si trova a sinistra all'ingresso del sentiero.",
                "Il bidone giallo si trova all'ingresso della casa.",
                "Nelle vicinanze: spiaggia del campeggio a circa 2 minuti a piedi e spiaggia comunale di Paladru a circa 5 minuti in auto.",
            ],
            9: ["Spegnete le luci quando uscite da una stanza e scollegate i cavi USB inutilizzati.", "È disponibile un aspirapolvere per lasciare la casa pulita."],
        },
        "highlights": {
            "parking_title": "Parcheggio e diritto di passaggio",
            "parking_text": "Parcheggiate nei posti pubblici lungo la strada, accanto alla siepe. Il terreno davanti alla casa appartiene al vicino: attraversatelo solo a piedi per raggiungere la casa, senza sostare o lasciare oggetti. Grazie per il rispetto; contattateci in caso di dubbi.",
            "stove_title": "Regolare la stufa a pellet",
            "stove_text": "Usate il telefono disponibile in casa. Aprite l'app MCZ per accendere la stufa e regolare la temperatura. I pellet sono nel piccolo armadietto esterno; contattateci se serve aiuto.",
            "guide_title": "Guida completa del soggiorno",
            "guide_intro": "Qui trovate tutte le informazioni pratiche sulla casa. Il PDF illustrato è disponibile anche per le foto dell'arrivo.",
            "pdf_label": "Vedi la guida PDF illustrata",
            "parking_photo": "Posti pubblici accanto alla siepe: parcheggiate solo dove è consentito.",
            "path_photo": "Seguite a piedi il sentiero in erba e ghiaia lungo la recinzione in legno.",
        },
    },
    "es": {
        "parking": [
            "Por favor, aparque solo en las plazas públicas de la calle, junto al seto. No hay aparcamiento privado.",
            "El terreno frente a la casa pertenece al vecino. El derecho de paso permite llegar a la casa a pie, sin detenerse ni dejar objetos allí.",
            "Para mantener libre el acceso, no aparque allí, ni siquiera brevemente, ni bloquee el paso.",
            "Mantenga a sus mascotas con usted y recoja sus excrementos, también junto al camino.",
            "Si tiene dudas sobre una plaza o los límites de la propiedad, consúltenos antes de aparcar.",
        ],
        "stove": [
            "Hay un teléfono disponible en la casa para encender y ajustar la estufa de pellets mediante la aplicación MCZ.",
            "Abra la aplicación MCZ en ese teléfono y ajuste la temperatura a su gusto. Si la estufa no responde, contáctenos en lugar de cambiar los ajustes técnicos.",
            "Hay algunos pellets en el pequeño armario exterior. Avísenos si quedan pocos.",
        ],
        "extras": {
            3: ["Hay juguetes, libros y una máquina de raclette disponibles; guárdelos después de usarlos."],
            7: ["El cuadro eléctrico está en la planta baja; no toque los interruptores y contáctenos si surge algún problema.", "Respete los carteles y espacios personales decorados por los niños."],
            8: [
                "Si lo necesita, el contenedor gris para residuos orgánicos está a la izquierda, a la entrada del camino.",
                "El contenedor amarillo está a la entrada de la casa.",
                "Cerca: la playa del camping está a unos 2 minutos a pie y la playa municipal de Paladru, a unos 5 minutos en coche.",
            ],
            9: ["Apague las luces al salir de una habitación y desconecte los cables USB que no utilice.", "Hay una aspiradora disponible para dejar la casa limpia."],
        },
        "highlights": {
            "parking_title": "Aparcamiento y derecho de paso",
            "parking_text": "Aparque en las plazas públicas de la calle, junto al seto. El terreno frente a la casa pertenece al vecino: crúcelo solo a pie para llegar a la casa, sin aparcar ni dejar objetos. Gracias por respetar su espacio; consúltenos si tiene dudas.",
            "stove_title": "Ajustar la estufa de pellets",
            "stove_text": "Use el teléfono disponible en la casa. Abra la aplicación MCZ para encender la estufa y ajustar la temperatura. Hay pellets en el pequeño armario exterior; contáctenos si necesita ayuda.",
            "guide_title": "Guía completa de la estancia",
            "guide_intro": "Aquí encontrará toda la información práctica de la casa. El PDF ilustrado también muestra fotos de la llegada.",
            "pdf_label": "Ver la guía PDF ilustrada",
            "parking_photo": "Plazas públicas junto al seto: aparque solo donde esté permitido.",
            "path_photo": "Siga a pie el camino de hierba y grava junto a la valla de madera.",
        },
    },
}

for guide_lang, update in GUIDE_UPDATES.items():
    guide_data = GUIDE[guide_lang]
    guide_data["highlights"] = update["highlights"]
    guide_data["sections"][0]["items"][1] = update["parking"][0]
    guide_data["sections"][1]["items"] = update["parking"] + guide_data["sections"][1]["items"][2:]
    guide_data["sections"][5]["items"][0:1] = update["stove"]
    for section_index, extra_items in update["extras"].items():
        guide_data["sections"][section_index]["items"].extend(extra_items)


@app.route("/")
def index():
    lang = get_lang()
    context = common_context(lang)
    context.update(
        carousel_images=CAROUSEL_IMAGES,
        guide=GUIDE[lang],
        support=SUPPORT[lang],
        whatsapp_link=f"https://wa.me/{WHATSAPP_PHONE}" if WHATSAPP_PHONE else "#contact",
        email_link=f"mailto:{CONTACT_EMAIL}" if CONTACT_EMAIL else "#contact",
    )
    return render_template("index.html", **context)


@app.route("/support")
def support_page():
    lang = get_lang()
    context = common_context(lang)
    context["support"] = SUPPORT[lang]
    return render_template("support.html", **context)


@app.route("/photos")
def house_photos():
    lang = get_lang()
    context = common_context(lang)
    context["house_images"] = AIRBNB_IMAGES
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


@app.route("/ads.txt")
def ads_txt():
    return Response("google.com, pub-6158185990205930, DIRECT, f08c47fec0942fa0\n", mimetype="text/plain")


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
