from flask import Flask, render_template, request

app = Flask(__name__)

SUPPORTED_LANGS = ["fr", "en", "it"]

CONTACT = {
	"whatsapp_phone": "33600000000",
	"email": "votre-email@example.com",
}

CAROUSEL_IMAGES = [
	{"src": "images/carroussel/image.png", "alt": "Vue extérieure de la maison"},
	{"src": "images/carroussel/image copy.png", "alt": "Jardin et environnement"},
	{"src": "images/carroussel/image copy 2.png", "alt": "Vue du lac et alentours"},
	{"src": "images/carroussel/image copy 3.png", "alt": "Ambiance du séjour à Bilieu"},
]

HOUSE_IMAGES = [
	{"src": "images/casa/image.png", "alt": "Photo maison 1"},
	{"src": "images/casa/image copy.png", "alt": "Photo maison 2"},
	{"src": "images/casa/image copy 2.png", "alt": "Photo maison 3"},
	{"src": "images/casa/image copy 3.png", "alt": "Photo maison 4"},
]

GUIDE_CONTENT = {
	"fr": {
		"title": "Guide complet du séjour",
		"intro": "Toutes les informations utiles du document de bienvenue sont regroupées ici pour faciliter votre arrivée et votre séjour.",
		"kpis": [
			{"label": "Check-in", "value": "15h00"},
			{"label": "Check-out", "value": "10h00"},
			{"label": "Capacité", "value": "Jusqu'à 7 personnes"},
			{"label": "Distance", "value": "À 2 min à pied du lac"},
		],
		"sections": [
			{
				"title": "Arrivée & accès à la maison",
				"items": [
					"Stationnez dans les places publiques de la rue (à côté de la haie).",
					"Prenez ensuite le chemin herbe/gravier qui longe la clôture en bois.",
					"Repérez la maison avec grande baie vitrée et porte bois à trois carrés vitrés.",
				],
			},
			{
				"title": "Règles essentielles",
				"items": [
					"Maison strictement non-fumeurs (sanctions en cas d'odeur de cigarette).",
					"Silence de 22h00 à 08h00 (pas de fêtes, musique forte ou regroupements).",
					"Le terrain devant la maison appartient à un tiers : passage rapide uniquement (servitude).",
				],
			},
			{
				"title": "Couchages & pièces",
				"items": [
					"Salon/hall : 1 canapé convertible confortable pour 2 personnes.",
					"1er étage : 2 pièces (1 bureau + 1 chambre avec 1 lit simple).",
					"2e étage : 1 chambre avec 1 lit simple + 1 fauteuil-lit.",
					"2e étage : 1 chambre avec 1 lit double (couple).",
				],
			},
			{
				"title": "Confort & équipements",
				"items": [
					"Wi-Fi : Bbox–1202F156.",
					"Smart TV connectée (Netflix, YouTube, etc.).",
					"Poêle à granulés pilotable via application MCZ (téléphone dédié disponible).",
					"Granulés disponibles dans le petit placard extérieur.",
					"Lave-linge au dernier étage, dans la salle de bains.",
					"Bureau avec écran, clavier et souris.",
				],
			},
			{
				"title": "Linge, propreté, animaux",
				"items": [
					"Draps, couvertures et serviettes ne sont pas fournis.",
					"La maison est livrée propre et doit être rendue propre.",
					"Aspirateur et équipements de nettoyage à disposition.",
					"Chiens et chats bienvenus, merci de nettoyer après eux.",
				],
			},
			{
				"title": "Sécurité & conseils pratiques",
				"items": [
					"Barrières de sécurité pour escaliers disponibles.",
					"Panneau électrique avec disjoncteurs : ne pas manipuler.",
					"Ne pas laisser de câbles USB branchés sans appareil connecté.",
					"Merci de respecter les affiches et espaces personnels décorés par les enfants.",
				],
			},
			{
				"title": "Autour de la maison",
				"items": [
					"Plage du camping : environ 2 min à pied.",
					"Plage municipale de Paladru : environ 5 min en voiture.",
					"Commerces utiles : Casino Charavines, Proxy Le Pin, Carrefour Voiron.",
				],
			},
		],
	},
	"en": {
		"title": "Complete stay guide",
		"intro": "All useful information from the welcome document is gathered here to make your arrival and stay smooth.",
		"kpis": [
			{"label": "Check-in", "value": "3:00 PM"},
			{"label": "Check-out", "value": "10:00 AM"},
			{"label": "Capacity", "value": "Up to 7 guests"},
			{"label": "Distance", "value": "2-min walk from the lake"},
		],
		"sections": [
			{
				"title": "Arrival & access to the house",
				"items": [
					"Park your car in the public street spaces (next to the hedge).",
					"Then take the grass/gravel path along the wooden fence.",
					"Look for the house with a large bay window and wooden door with three glass squares.",
				],
			},
			{
				"title": "Essential rules",
				"items": [
					"Strictly non-smoking property (penalties if cigarette odor is detected).",
					"Quiet hours from 10:00 PM to 8:00 AM (no loud music, parties, gatherings).",
					"The area in front of the house belongs to a third party: brief access passage only (easement).",
				],
			},
			{
				"title": "Sleeping layout & rooms",
				"items": [
					"Hall/living room: 1 comfortable sofa bed for 2 people.",
					"1st floor: 2 rooms (1 office + 1 bedroom with 1 single bed).",
					"2nd floor: 1 bedroom with 1 single bed + 1 armchair bed.",
					"2nd floor: 1 bedroom with 1 double bed (couple).",
				],
			},
			{
				"title": "Comfort & amenities",
				"items": [
					"Wi-Fi: Bbox–1202F156.",
					"Smart TV with Internet access (Netflix, YouTube, etc.).",
					"Pellet stove controllable with MCZ app (dedicated phone available).",
					"Pellets available in the small outdoor cupboard.",
					"Washing machine on the top floor (bathroom).",
					"Office setup with monitor, keyboard and mouse.",
				],
			},
			{
				"title": "Linen, cleanliness, pets",
				"items": [
					"Sheets, blankets and towels are not provided.",
					"The house is delivered clean and must be returned clean.",
					"Vacuum cleaner and cleaning tools are available.",
					"Dogs and cats are welcome; please clean after them.",
				],
			},
			{
				"title": "Safety & practical tips",
				"items": [
					"Stair safety gates are available.",
					"Electrical panel and breakers: please do not handle.",
					"Do not leave USB cables plugged in without a connected device.",
					"Please respect posters and personal spaces decorated by our children.",
				],
			},
			{
				"title": "Around the house",
				"items": [
					"Camping beach: about 2 minutes on foot.",
					"Paladru public beach: about 5 minutes by car.",
					"Useful shops: Casino Charavines, Proxy Le Pin, Carrefour Voiron.",
				],
			},
		],
	},
	"it": {
		"title": "Guida completa al soggiorno",
		"intro": "Tutte le informazioni utili del documento di benvenuto sono raccolte qui per facilitare arrivo e permanenza.",
		"kpis": [
			{"label": "Check-in", "value": "15:00"},
			{"label": "Check-out", "value": "10:00"},
			{"label": "Capienza", "value": "Fino a 7 ospiti"},
			{"label": "Distanza", "value": "A 2 minuti a piedi dal lago"},
		],
		"sections": [
			{
				"title": "Arrivo & accesso alla casa",
				"items": [
					"Parcheggiare negli spazi pubblici in strada (accanto alla siepe).",
					"Seguire poi il sentiero erba/ghiaia lungo la recinzione in legno.",
					"Riconoscere la casa con grande vetrata e porta in legno con tre riquadri in vetro.",
				],
			},
			{
				"title": "Regole essenziali",
				"items": [
					"Struttura rigorosamente non fumatori (sanzioni in caso di odore di sigaretta).",
					"Silenzio dalle 22:00 alle 08:00 (no musica alta, feste o raduni).",
					"L'area davanti casa appartiene a terzi: consentito solo passaggio rapido (servitù).",
				],
			},
			{
				"title": "Posti letto & camere",
				"items": [
					"Ingresso/soggiorno: 1 divano letto comodo per 2 persone.",
					"1° piano: 2 stanze (1 ufficio + 1 camera con 1 letto singolo).",
					"2° piano: 1 camera con 1 letto singolo + 1 poltrona letto.",
					"2° piano: 1 camera con 1 letto matrimoniale (coppia).",
				],
			},
			{
				"title": "Comfort & dotazioni",
				"items": [
					"Wi-Fi: Bbox–1202F156.",
					"Smart TV con Internet (Netflix, YouTube, ecc.).",
					"Stufa a pellet gestibile con app MCZ (telefono dedicato disponibile).",
					"Pellet disponibili nel piccolo armadietto esterno.",
					"Lavatrice all'ultimo piano (bagno).",
					"Postazione ufficio con monitor, tastiera e mouse.",
				],
			},
			{
				"title": "Biancheria, pulizia, animali",
				"items": [
					"Lenzuola, coperte e asciugamani non sono forniti.",
					"La casa viene consegnata pulita e deve essere restituita pulita.",
					"Aspirapolvere e strumenti per la pulizia sono disponibili.",
					"Cani e gatti benvenuti; si prega di pulire dopo di loro.",
				],
			},
			{
				"title": "Sicurezza & consigli pratici",
				"items": [
					"Barriere di sicurezza per scale disponibili.",
					"Pannello elettrico e interruttori: non manipolare.",
					"Non lasciare cavi USB collegati senza dispositivo connesso.",
					"Si prega di rispettare poster e spazi personali decorati dai nostri figli.",
				],
			},
			{
				"title": "Nei dintorni",
				"items": [
					"Spiaggia del campeggio: circa 2 minuti a piedi.",
					"Spiaggia municipale di Paladru: circa 5 minuti in auto.",
					"Negozi utili: Casino Charavines, Proxy Le Pin, Carrefour Voiron.",
				],
			},
		],
	},
}

CONTENT = {
	"fr": {
		"lang_name": "Français",
		"meta_title": "Bilieu & lac de Paladru",
		"nav": {
			"beauties": "Beautés du lac",
			"house": "Maison Airbnb",
			"house_photos": "Photos maison",
			"services": "Services & marchés",
			"pdf": "Infos du PDF",
			"contact": "Contact",
		},
		"hero": {
			"title": "Bienvenue à Bilieu, au bord du lac de Paladru",
			"subtitle": "Un site simple pour découvrir les beautés du lac, la maison en location et toutes les informations utiles de votre séjour.",
		},
		"beauties": {
			"title": "Les beautés du lac de Paladru",
			"text": "Le lac de Paladru offre des paysages calmes, des balades nature et des moments inoubliables au fil de l'eau.",
		},
		"house": {
			"title": "La maison Airbnb",
			"text": "Notre maison est située à deux pas du lac. Vous profitez d'un cadre paisible, d'un accès rapide aux plages et d'un séjour convivial.",
			"airbnb_label": "Voir l'annonce Airbnb",
			"airbnb_url": "https://www.airbnb.fr/rooms/1402915287163928554",
		},
		"house_gallery": {
			"title": "Photos de la maison",
		},
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
						"Hall / salon : 1 canapé convertible confortable pour 2 personnes",
						"1er étage : 2 chambres, dont 1 bureau et 1 chambre avec 1 lit simple",
						"2e étage : 1 chambre avec 1 lit simple + 1 fauteuil-lit",
						"2e étage : 1 chambre avec 1 lit double (couple)",
					],
				},
				{
					"title": "Équipements utiles",
					"items": [
						"Wi-Fi, Smart TV, poêle à granulés (application MCZ)",
						"Lave-linge au dernier étage (salle de bains)",
						"Espace bureau avec écran, clavier et souris",
						"Barrières de sécurité pour escaliers disponibles",
					],
				},
				{
					"title": "Règles principales",
					"items": [
						"Maison strictement non-fumeurs",
						"Silence demandé de 22h00 à 08h00",
						"Draps, couvertures et serviettes non fournis",
						"Animaux bienvenus (merci de nettoyer après eux)",
					],
				},
			],
		},
		"territory_right": {
			"title": "Droit au territoire",
			"text": "Le terrain devant la maison n'appartient pas à cette propriété. Il appartient à un tiers: aucune personne ni aucun véhicule ne doit y stationner ou y rester. Seul un passage rapide, autorisé par la loi (servitude), est permis.",
		},
		"services": {
			"title": "Services & marchés à proximité",
			"home_services_title": "Services de la maison",
			"home_services": [
				"Wi-Fi : Bbox–1202F156",
				"Smart TV connectée (Netflix, YouTube, etc.)",
				"Poêle à granulés (app MCZ)",
				"Lave-linge au dernier étage",
				"Bureau avec écran, clavier et souris",
			],
			"markets_title": "Marchés / commerces proches",
			"markets": [
				"Casino Charavines – 25 Avenue du Lac, 38850 Charavines",
				"Proxy Le Pin – 112 Route de Voiron, 38730 Le Pin",
				"Carrefour Voiron – 21 Boulevard Edgar Kofler, 38500 Voiron",
			],
		},
		"pdf_info": {
			"title": "Informations utiles (du PDF)",
			"cards": [
				{
					"title": "Arrivée & départ",
					"items": [
						"Check-in : 15h00",
						"Check-out : 10h00",
						"Stationnement public gratuit dans la rue",
					],
				},
				{
					"title": "Accès à la maison",
					"items": [
						"Après stationnement, prendre le chemin herbe/gravier",
						"Suivre la clôture en bois",
						"Maison avec grande baie vitrée et porte bois à carrés vitrés",
					],
				},
				{
					"title": "Règles importantes",
					"items": [
						"Maison strictement non-fumeurs",
						"Silence demandé de 22h00 à 08h00",
						"Respecter la zone devant la maison (servitude d'accès)",
					],
				},
				{
					"title": "Confort",
					"items": [
						"Canapé convertible + plusieurs couchages selon étages",
						"Draps, couvertures et serviettes non fournis",
						"Animaux bienvenus (merci de nettoyer après eux)",
					],
				},
			],
		},
		"contact": {
			"title": "Contact",
			"text": "Pour toute question sur la maison, votre arrivée ou votre séjour, contactez-nous directement.",
			"whatsapp_label": "Écrire sur WhatsApp",
			"email_label": "Envoyer un email",
		},
	},
	"en": {
		"lang_name": "English",
		"meta_title": "Bilieu & Lake Paladru",
		"nav": {
			"beauties": "Lake Beauty",
			"house": "Airbnb Home",
			"house_photos": "House Photos",
			"services": "Services & Markets",
			"pdf": "PDF Info",
			"contact": "Contact",
		},
		"hero": {
			"title": "Welcome to Bilieu, near Lake Paladru",
			"subtitle": "A simple website to discover the lake beauty, the rental house, and practical stay information.",
		},
		"beauties": {
			"title": "The beauty of Lake Paladru",
			"text": "Lake Paladru is perfect for peaceful views, nature walks, and unforgettable moments by the water.",
		},
		"house": {
			"title": "The Airbnb house",
			"text": "Our house is just steps from the lake. Enjoy a peaceful setting, quick beach access, and a warm stay.",
			"airbnb_label": "Open Airbnb listing",
			"airbnb_url": "https://www.airbnb.fr/rooms/1402915287163928554",
		},
		"house_gallery": {
			"title": "House photos",
		},
		"stay_details": {
			"title": "Capacity, rooms & sleeping",
			"stats": [
				{"label": "Capacity", "value": "Up to 7 guests"},
				{"label": "Bedrooms", "value": "3 bedrooms + 1 office room"},
				{"label": "Sleeping spots", "value": "5 sleeping spots across floors"},
				{"label": "Living room", "value": "1 double sofa bed"},
			],
			"cards": [
				{
					"title": "Sleeping layout",
					"items": [
						"Hall / living room: 1 comfortable sofa bed for 2 people",
						"1st floor: 2 rooms, including 1 office and 1 bedroom with 1 single bed",
						"2nd floor: 1 bedroom with 1 single bed + 1 armchair bed",
						"2nd floor: 1 bedroom with 1 double bed (couple)",
					],
				},
				{
					"title": "Useful amenities",
					"items": [
						"Wi-Fi, Smart TV, pellet stove (MCZ app)",
						"Washing machine on top floor (bathroom)",
						"Office area with monitor, keyboard and mouse",
						"Safety gates for stairs are available",
					],
				},
				{
					"title": "Main house rules",
					"items": [
						"Strictly non-smoking property",
						"Quiet hours from 10:00 PM to 8:00 AM",
						"Sheets, blankets and towels are not provided",
						"Pets are welcome (please clean after them)",
					],
				},
			],
		},
		"territory_right": {
			"title": "Right to the land",
			"text": "The area in front of the house is not part of this property. It belongs to a third party: no person or vehicle may stop, remain, or park there. Only a brief passage allowed by law (easement) is permitted.",
		},
		"services": {
			"title": "Services & nearby markets",
			"home_services_title": "Home services",
			"home_services": [
				"Wi-Fi: Bbox–1202F156",
				"Smart TV connected to Internet (Netflix, YouTube, etc.)",
				"Pellet stove (MCZ app)",
				"Washing machine on the top floor",
				"Office area with monitor, keyboard and mouse",
			],
			"markets_title": "Nearby markets / shops",
			"markets": [
				"Casino Charavines – 25 Avenue du Lac, 38850 Charavines",
				"Proxy Le Pin – 112 Route de Voiron, 38730 Le Pin",
				"Carrefour Voiron – 21 Boulevard Edgar Kofler, 38500 Voiron",
			],
		},
		"pdf_info": {
			"title": "Useful information (from the PDF)",
			"cards": [
				{
					"title": "Arrival & departure",
					"items": [
						"Check-in: 3:00 PM",
						"Check-out: 10:00 AM",
						"Free public parking in the street",
					],
				},
				{
					"title": "Access to the house",
					"items": [
						"After parking, take the grass/gravel path",
						"Follow the wooden fence",
						"Look for the house with a large bay window and wooden door",
					],
				},
				{
					"title": "Important rules",
					"items": [
						"Strictly non-smoking property",
						"Quiet hours from 10:00 PM to 8:00 AM",
						"Respect the front area (access easement)",
					],
				},
				{
					"title": "Comfort",
					"items": [
						"Sofa bed + multiple sleeping options by floor",
						"Sheets, blankets and towels are not provided",
						"Pets welcome (please clean after them)",
					],
				},
			],
		},
		"contact": {
			"title": "Contact",
			"text": "For any question about the house, your arrival, or your stay, contact us directly.",
			"whatsapp_label": "Message on WhatsApp",
			"email_label": "Send an email",
		},
	},
	"it": {
		"lang_name": "Italiano",
		"meta_title": "Bilieu e lago di Paladru",
		"nav": {
			"beauties": "Bellezze del lago",
			"house": "Casa Airbnb",
			"house_photos": "Foto casa",
			"services": "Servizi e mercati",
			"pdf": "Info PDF",
			"contact": "Contatto",
		},
		"hero": {
			"title": "Benvenuti a Bilieu, vicino al lago di Paladru",
			"subtitle": "Un sito semplice per scoprire le bellezze del lago, la casa in affitto e le informazioni utili del soggiorno.",
		},
		"beauties": {
			"title": "Le bellezze del lago di Paladru",
			"text": "Il lago di Paladru offre panorami tranquilli, passeggiate nella natura e momenti indimenticabili sull'acqua.",
		},
		"house": {
			"title": "La casa Airbnb",
			"text": "La nostra casa si trova a pochi passi dal lago. Godetevi un ambiente tranquillo, accesso rapido alle spiagge e un soggiorno accogliente.",
			"airbnb_label": "Apri annuncio Airbnb",
			"airbnb_url": "https://www.airbnb.fr/rooms/1402915287163928554",
		},
		"house_gallery": {
			"title": "Foto della casa",
		},
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
						"Ingresso / soggiorno: 1 divano letto comodo per 2 persone",
						"1° piano: 2 stanze, di cui 1 ufficio e 1 camera con 1 letto singolo",
						"2° piano: 1 camera con 1 letto singolo + 1 poltrona letto",
						"2° piano: 1 camera con 1 letto matrimoniale (coppia)",
					],
				},
				{
					"title": "Dotazioni utili",
					"items": [
						"Wi-Fi, Smart TV, stufa a pellet (app MCZ)",
						"Lavatrice all'ultimo piano (bagno)",
						"Area ufficio con monitor, tastiera e mouse",
						"Barriere di sicurezza per le scale disponibili",
					],
				},
				{
					"title": "Regole principali",
					"items": [
						"Struttura rigorosamente non fumatori",
						"Silenzio dalle 22:00 alle 08:00",
						"Lenzuola, coperte e asciugamani non forniti",
						"Animali benvenuti (si prega di pulire dopo di loro)",
					],
				},
			],
		},
		"territory_right": {
			"title": "Diritto al passaggio",
			"text": "L'area davanti alla casa non fa parte di questa proprietà. Appartiene a un terzo: nessuna persona o veicolo può sostare o fermarsi lì. È consentito solo un passaggio rapido previsto dalla legge (servitù).",
		},
		"services": {
			"title": "Servizi e mercati vicini",
			"home_services_title": "Servizi della casa",
			"home_services": [
				"Wi‑Fi: Bbox–1202F156",
				"Smart TV con Internet (Netflix, YouTube, ecc.)",
				"Stufa a pellet (app MCZ)",
				"Lavatrice all'ultimo piano",
				"Ufficio con monitor, tastiera e mouse",
			],
			"markets_title": "Mercati / negozi vicini",
			"markets": [
				"Casino Charavines – 25 Avenue du Lac, 38850 Charavines",
				"Proxy Le Pin – 112 Route de Voiron, 38730 Le Pin",
				"Carrefour Voiron – 21 Boulevard Edgar Kofler, 38500 Voiron",
			],
		},
		"pdf_info": {
			"title": "Informazioni utili (dal PDF)",
			"cards": [
				{
					"title": "Arrivo e partenza",
					"items": [
						"Check-in: 15:00",
						"Check-out: 10:00",
						"Parcheggio pubblico gratuito in strada",
					],
				},
				{
					"title": "Accesso alla casa",
					"items": [
						"Dopo il parcheggio, seguire il sentiero erba/ghiaia",
						"Seguire la recinzione in legno",
						"Casa con grande vetrata e porta in legno",
					],
				},
				{
					"title": "Regole importanti",
					"items": [
						"Struttura rigorosamente non fumatori",
						"Silenzio dalle 22:00 alle 08:00",
						"Rispettare l'area davanti casa (servitù di passaggio)",
					],
				},
				{
					"title": "Comfort",
					"items": [
						"Divano letto + diversi posti letto sui piani",
						"Lenzuola, coperte e asciugamani non forniti",
						"Animali benvenuti (pulire dopo di loro)",
					],
				},
			],
		},
		"contact": {
			"title": "Contatto",
			"text": "Per qualsiasi domanda sulla casa, sull'arrivo o sul soggiorno, contattateci direttamente.",
			"whatsapp_label": "Scrivi su WhatsApp",
			"email_label": "Invia un'email",
		},
	},
}


@app.route("/")
def index():
	lang = request.args.get("lang", "fr").lower()
	if lang not in SUPPORTED_LANGS:
		lang = "fr"

	return render_template(
		"index.html",
		lang=lang,
		supported_langs=SUPPORTED_LANGS,
		content=CONTENT[lang],
		carousel_images=CAROUSEL_IMAGES,
		house_images=HOUSE_IMAGES,
		whatsapp_link=f"https://wa.me/{CONTACT['whatsapp_phone']}",
		email_link=f"mailto:{CONTACT['email']}",
	)


@app.route("/house-photos")
def house_photos():
	lang = request.args.get("lang", "fr").lower()
	if lang not in SUPPORTED_LANGS:
		lang = "fr"

	return render_template(
		"house_photos.html",
		lang=lang,
		supported_langs=SUPPORTED_LANGS,
		content=CONTENT[lang],
		house_images=HOUSE_IMAGES,
	)


@app.route("/guid")
@app.route("/guide")
def guide():
	lang = request.args.get("lang", "fr").lower()
	if lang not in SUPPORTED_LANGS:
		lang = "fr"

	return render_template(
		"guide.html",
		lang=lang,
		supported_langs=SUPPORTED_LANGS,
		content=CONTENT[lang],
		guide=GUIDE_CONTENT[lang],
	)


if __name__ == "__main__":
	app.run(debug=True)
