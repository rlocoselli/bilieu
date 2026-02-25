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

LEGAL_CONTENT = {
	"fr": {
		"title": "Confidentialité & cookies",
		"intro": "Cette page explique comment le site Bilieu traite les données personnelles et utilise les cookies.",
		"sections": [
			{
				"title": "Responsable du traitement",
				"items": [
					"Hébergeur du site: Bilieu (contact via la section Contact).",
					"E-mail de contact: votre-email@example.com.",
				],
			},
			{
				"title": "Données traitées",
				"items": [
					"Ce site ne crée pas de compte utilisateur et ne collecte pas de données marketing.",
					"Les seules données potentiellement transmises sont celles que vous envoyez volontairement (email, WhatsApp).",
				],
			},
			{
				"title": "Cookies",
				"items": [
					"Un cookie local de consentement est utilisé pour mémoriser votre choix (accepté/refusé).",
					"Aucun cookie publicitaire ou traqueur tiers n'est activé par défaut.",
				],
			},
			{
				"title": "Vos droits (RGPD)",
				"items": [
					"Vous pouvez demander l'accès, la rectification ou la suppression de vos données transmises.",
					"Vous pouvez modifier votre consentement cookies à tout moment via le bouton en bas de page.",
				],
			},
		],
	},
	"en": {
		"title": "Privacy & cookies",
		"intro": "This page explains how the Bilieu website handles personal data and uses cookies.",
		"sections": [
			{
				"title": "Data controller",
				"items": [
					"Website owner: Bilieu (contact via the Contact section).",
					"Contact email: your-email@example.com.",
				],
			},
			{
				"title": "Processed data",
				"items": [
					"This website does not create user accounts and does not run marketing collection.",
					"Only data you voluntarily send (email, WhatsApp) may be processed.",
				],
			},
			{
				"title": "Cookies",
				"items": [
					"A local consent cookie equivalent is used to remember your choice (accepted/rejected).",
					"No advertising or third-party tracking cookie is enabled by default.",
				],
			},
			{
				"title": "Your GDPR rights",
				"items": [
					"You may request access, correction, or deletion of data you sent.",
					"You may change cookie consent at any time via the footer button.",
				],
			},
		],
	},
	"it": {
		"title": "Privacy e cookie",
		"intro": "Questa pagina spiega come il sito Bilieu tratta i dati personali e utilizza i cookie.",
		"sections": [
			{
				"title": "Titolare del trattamento",
				"items": [
					"Proprietario del sito: Bilieu (contatto nella sezione Contatto).",
					"Email di contatto: vostra-email@example.com.",
				],
			},
			{
				"title": "Dati trattati",
				"items": [
					"Il sito non crea account utente e non effettua raccolta marketing.",
					"Sono trattati solo i dati inviati volontariamente (email, WhatsApp).",
				],
			},
			{
				"title": "Cookie",
				"items": [
					"Viene usato un cookie locale di consenso per ricordare la tua scelta (accettato/rifiutato).",
					"Nessun cookie pubblicitario o di tracciamento di terze parti è attivo per impostazione predefinita.",
				],
			},
			{
				"title": "I tuoi diritti (GDPR)",
				"items": [
					"Puoi chiedere accesso, rettifica o cancellazione dei dati inviati.",
					"Puoi modificare il consenso cookie in qualsiasi momento dal pulsante nel footer.",
				],
			},
		],
	},
}

HISTORY_CONTENT = {
	"fr": {
		"title": "L'histoire de Bilieu",
		"intro": "Bilieu est une commune du nord Isère, au bord du lac de Paladru. Son histoire est liée à la vie rurale, aux voies de passage locales et à l'évolution touristique du lac.",
		"kpis": [
			{"label": "Région", "value": "Auvergne-Rhône-Alpes"},
			{"label": "Territoire", "value": "Pays voironnais"},
			{"label": "Repère local", "value": "Lac de Paladru"},
			{"label": "Identité", "value": "Village nature et patrimoine"},
		],
		"sections": [
			{
				"title": "Étymologie du nom Bilieu",
				"items": [
					"Selon des interprétations toponymiques locales, le nom Bilieu pourrait dériver d'une forme ancienne liée à un domaine rural gallo-romain.",
					"Comme pour de nombreux noms de communes anciennes, l'origine exacte n'est pas absolument certaine et peut varier selon les sources historiques.",
				],
			},
			{
				"title": "Origines rurales",
				"items": [
					"Le développement du village s'est appuyé sur l'agriculture, l'élevage et la gestion des terres autour du lac.",
					"L'habitat traditionnel s'organise historiquement en hameaux et maisons familiales tournés vers les activités locales.",
				],
			},
			{
				"title": "Lien avec le lac de Paladru",
				"items": [
					"Le lac a structuré la vie quotidienne: pêche, circulation locale, loisirs, puis attractivité touristique.",
					"Aujourd'hui encore, le lac reste au cœur de l'identité paysagère et culturelle de Bilieu.",
				],
			},
			{
				"title": "Patrimoine et vie locale",
				"items": [
					"Le territoire conserve un caractère résidentiel paisible, mêlant mémoire rurale et usages contemporains.",
					"La commune valorise un cadre de vie naturel, avec un rythme marqué par les saisons et les activités de plein air.",
				],
			},
		],
	},
	"en": {
		"title": "The history of Bilieu",
		"intro": "Bilieu is a municipality in northern Isère, on the shores of Lake Paladru. Its history is tied to rural life, local routes, and the lake's growing tourism role.",
		"kpis": [
			{"label": "Region", "value": "Auvergne-Rhône-Alpes"},
			{"label": "Area", "value": "Pays voironnais"},
			{"label": "Local landmark", "value": "Lake Paladru"},
			{"label": "Identity", "value": "Nature and heritage village"},
		],
		"sections": [
			{
				"title": "Etymology of the name Bilieu",
				"items": [
					"According to local toponymic interpretations, the name Bilieu may come from an older form linked to a rural Gallo-Roman estate.",
					"As with many old place names, the exact origin is not fully certain and can vary depending on historical sources.",
				],
			},
			{
				"title": "Rural roots",
				"items": [
					"The village developed through agriculture, livestock activity, and land use around the lake.",
					"Traditional settlement patterns historically relied on hamlets and family homes linked to local work.",
				],
			},
			{
				"title": "Connection with Lake Paladru",
				"items": [
					"The lake shaped daily life: fishing, local movement, leisure, and later visitor attraction.",
					"Today, it remains central to Bilieu's landscape and cultural identity.",
				],
			},
			{
				"title": "Heritage and local life",
				"items": [
					"The area keeps a calm residential character, combining rural memory with modern uses.",
					"The municipality values a nature-focused lifestyle with strong seasonal outdoor activities.",
				],
			},
		],
	},
	"it": {
		"title": "La storia di Bilieu",
		"intro": "Bilieu è un comune del nord dell'Isère, sulle rive del lago di Paladru. La sua storia è legata alla vita rurale, ai percorsi locali e allo sviluppo turistico del lago.",
		"kpis": [
			{"label": "Regione", "value": "Auvergne-Rhône-Alpes"},
			{"label": "Territorio", "value": "Pays voironnais"},
			{"label": "Riferimento locale", "value": "Lago di Paladru"},
			{"label": "Identità", "value": "Natura e patrimonio"},
		],
		"sections": [
			{
				"title": "Etimologia del nome Bilieu",
				"items": [
					"Secondo interpretazioni toponomastiche locali, il nome Bilieu potrebbe derivare da una forma antica legata a un dominio rurale gallo-romano.",
					"Come per molti toponimi antichi, l'origine precisa non è del tutto certa e può variare a seconda delle fonti storiche.",
				],
			},
			{
				"title": "Origini rurali",
				"items": [
					"Lo sviluppo del villaggio si è basato su agricoltura, allevamento e gestione delle terre attorno al lago.",
					"L'insediamento tradizionale si è storicamente organizzato in piccoli nuclei e case familiari legate alle attività locali.",
				],
			},
			{
				"title": "Legame con il lago di Paladru",
				"items": [
					"Il lago ha strutturato la vita quotidiana: pesca, spostamenti locali, svago e poi attrattività turistica.",
					"Ancora oggi il lago resta al centro dell'identità paesaggistica e culturale di Bilieu.",
				],
			},
			{
				"title": "Patrimonio e vita locale",
				"items": [
					"Il territorio mantiene un carattere residenziale tranquillo, tra memoria rurale e usi contemporanei.",
					"Il comune valorizza uno stile di vita naturale, scandito dalle stagioni e dalle attività all'aperto.",
				],
			},
		],
	},
}

BUS_CONTENT = {
	"fr": {
		"title": "Lignes de bus",
		"intro": "Informations pratiques pour organiser vos trajets autour de Bilieu et du lac de Paladru. Les horaires peuvent évoluer selon la saison: vérifiez toujours les horaires officiels avant départ.",
		"links": [
			{"label": "Consulter les horaires (PDF ligne 526-1)", "url": "https://www.paysvoironnais.com/wp-content/uploads/2025/08/526-1.pdf"},
			{"label": "Itinéraire en transport (Google Maps)", "url": "https://www.google.com/maps/dir/?api=1&destination=Bilieu"},
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
					"Lundi-vendredi: passages renforcés le matin et en fin d'après-midi.",
					"Samedi: fréquence réduite, vérifier les retours en soirée.",
					"Dimanche et jours fériés: service limité selon période.",
				],
			},
			{
				"title": "Itinéraires utiles",
				"items": [
					"Bilieu → Charavines: accès commerces et zones du lac.",
					"Bilieu → Voiron: correspondance train et services urbains.",
					"Bilieu → Le Pin / Paladru: déplacements locaux et balades.",
				],
			},
			{
				"title": "Conseils voyageurs",
				"items": [
					"Prévoir l'appoint ou un titre de transport validé avant montée.",
					"En période touristique, anticiper les départs très demandés.",
					"Conserver une alternative (taxi/covoiturage) pour les retours tardifs.",
				],
			},
		],
	},
	"en": {
		"title": "Bus lines",
		"intro": "Practical information to plan trips around Bilieu and Lake Paladru. Timetables may change by season: always check official updates before departure.",
		"links": [
			{"label": "Check timetables (PDF line 526-1)", "url": "https://www.paysvoironnais.com/wp-content/uploads/2025/08/526-1.pdf"},
			{"label": "Transit route (Google Maps)", "url": "https://www.google.com/maps/dir/?api=1&destination=Bilieu"},
		],
		"kpis": [
			{"label": "Recommended stop", "value": "Bilieu center"},
			{"label": "Main connection", "value": "Voiron station"},
			{"label": "Toward the lake", "value": "Bilieu / Charavines"},
			{"label": "Tip", "value": "Arrive 5 min early"},
		],
		"sections": [
			{
				"title": "Typical timetables (indicative)",
				"items": [
					"Monday-Friday: stronger frequency in early morning and late afternoon.",
					"Saturday: reduced service, check evening return options.",
					"Sundays and holidays: limited service depending on period.",
				],
			},
			{
				"title": "Useful routes",
				"items": [
					"Bilieu → Charavines: access to shops and lake areas.",
					"Bilieu → Voiron: train connection and urban services.",
					"Bilieu → Le Pin / Paladru: local trips and nature outings.",
				],
			},
			{
				"title": "Traveler tips",
				"items": [
					"Prepare fare or a valid ticket before boarding.",
					"During tourist season, anticipate peak departures.",
					"Keep a backup option (taxi/carpool) for late returns.",
				],
			},
		],
	},
	"it": {
		"title": "Linee bus",
		"intro": "Informazioni pratiche per organizzare gli spostamenti intorno a Bilieu e al lago di Paladru. Gli orari possono cambiare in base alla stagione: verificare sempre gli aggiornamenti ufficiali prima della partenza.",
		"links": [
			{"label": "Consulta orari (PDF linea 526-1)", "url": "https://www.paysvoironnais.com/wp-content/uploads/2025/08/526-1.pdf"},
			{"label": "Percorso trasporto pubblico (Google Maps)", "url": "https://www.google.com/maps/dir/?api=1&destination=Bilieu"},
		],
		"kpis": [
			{"label": "Fermata consigliata", "value": "Bilieu centro"},
			{"label": "Coincidenza", "value": "Stazione di Voiron"},
			{"label": "Verso il lago", "value": "Bilieu / Charavines"},
			{"label": "Consiglio", "value": "Arrivare 5 min prima"},
		],
		"sections": [
			{
				"title": "Orari tipici (indicativi)",
				"items": [
					"Lunedì-venerdì: frequenza maggiore al mattino e nel tardo pomeriggio.",
					"Sabato: servizio ridotto, verificare i rientri serali.",
					"Domenica e festivi: servizio limitato secondo il periodo.",
				],
			},
			{
				"title": "Itinerari utili",
				"items": [
					"Bilieu → Charavines: accesso a negozi e aree del lago.",
					"Bilieu → Voiron: coincidenza treno e servizi urbani.",
					"Bilieu → Le Pin / Paladru: spostamenti locali e passeggiate.",
				],
			},
			{
				"title": "Consigli di viaggio",
				"items": [
					"Preparare il pagamento o un titolo di viaggio valido prima della salita.",
					"In alta stagione, anticipare le partenze più richieste.",
					"Tenere un'alternativa (taxi/carpooling) per i rientri tardivi.",
				],
			},
		],
	},
}

ENVIRONMENT_CONTENT = {
	"fr": {
		"title": "Astuces environnement",
		"intro": "Des gestes simples pour profiter du séjour à Bilieu tout en respectant la nature, le lac et le voisinage.",
		"kpis": [
			{"label": "Objectif", "value": "Réduire les déchets"},
			{"label": "Priorité", "value": "Économiser l'eau"},
			{"label": "Mobilité", "value": "Privilégier bus et marche"},
			{"label": "Esprit", "value": "Laisser le lieu propre"},
		],
		"sections": [
			{
				"title": "Eau & énergie",
				"items": [
					"Limiter la durée des douches et couper l'eau pendant le savonnage.",
					"Éteindre les lumières en quittant une pièce.",
					"Ne pas laisser les chargeurs branchés inutilement.",
				],
			},
			{
				"title": "Déchets & tri",
				"items": [
					"Trier les emballages, verre et déchets ménagers selon les bacs locaux.",
					"Éviter le jetable: gourde, sacs réutilisables, boîtes repas.",
					"Ne rien laisser au bord du lac ni sur les sentiers.",
				],
			},
			{
				"title": "Mobilité douce",
				"items": [
					"Privilégier les lignes de bus et les déplacements à pied pour les trajets courts.",
					"Regrouper les courses pour limiter les déplacements en voiture.",
					"Respecter les zones de stationnement autorisées.",
				],
			},
			{
				"title": "Respect du cadre naturel",
				"items": [
					"Rester sur les chemins balisés lors des balades.",
					"Éviter le bruit en soirée pour préserver la tranquillité du lieu.",
					"Observer la faune et la flore sans les perturber.",
				],
			},
		],
	},
	"en": {
		"title": "Environment tips",
		"intro": "Simple actions to enjoy your stay in Bilieu while respecting nature, the lake, and local residents.",
		"kpis": [
			{"label": "Goal", "value": "Reduce waste"},
			{"label": "Priority", "value": "Save water"},
			{"label": "Mobility", "value": "Use bus and walking"},
			{"label": "Mindset", "value": "Leave the place clean"},
		],
		"sections": [
			{
				"title": "Water & energy",
				"items": [
					"Keep showers short and turn off water while soaping.",
					"Switch off lights when leaving a room.",
					"Avoid leaving chargers plugged in unnecessarily.",
				],
			},
			{
				"title": "Waste & sorting",
				"items": [
					"Sort packaging, glass, and household waste using local bins.",
					"Avoid single-use items: reusable bottle, bags, food boxes.",
					"Do not leave litter near the lake or on trails.",
				],
			},
			{
				"title": "Softer mobility",
				"items": [
					"Use bus lines and walk for short trips when possible.",
					"Group errands to reduce car travel.",
					"Respect authorized parking zones.",
				],
			},
			{
				"title": "Respect the natural setting",
				"items": [
					"Stay on marked paths during walks.",
					"Keep noise low in the evening to preserve calm surroundings.",
					"Observe fauna and flora without disturbing them.",
				],
			},
		],
	},
	"it": {
		"title": "Consigli per l'ambiente",
		"intro": "Piccoli gesti per vivere il soggiorno a Bilieu rispettando natura, lago e residenti.",
		"kpis": [
			{"label": "Obiettivo", "value": "Ridurre i rifiuti"},
			{"label": "Priorità", "value": "Risparmiare acqua"},
			{"label": "Mobilità", "value": "Bus e spostamenti a piedi"},
			{"label": "Spirito", "value": "Lasciare il luogo pulito"},
		],
		"sections": [
			{
				"title": "Acqua ed energia",
				"items": [
					"Ridurre la durata della doccia e chiudere l'acqua durante l'insaponamento.",
					"Spegnere le luci quando si esce da una stanza.",
					"Non lasciare i caricabatterie collegati inutilmente.",
				],
			},
			{
				"title": "Rifiuti e raccolta differenziata",
				"items": [
					"Separare imballaggi, vetro e rifiuti domestici secondo i contenitori locali.",
					"Evitare il monouso: borraccia, borse riutilizzabili, contenitori pasto.",
					"Non lasciare rifiuti vicino al lago o sui sentieri.",
				],
			},
			{
				"title": "Mobilità dolce",
				"items": [
					"Preferire le linee bus e gli spostamenti a piedi per i tragitti brevi.",
					"Raggruppare gli acquisti per ridurre gli spostamenti in auto.",
					"Rispettare le aree di parcheggio autorizzate.",
				],
			},
			{
				"title": "Rispetto del contesto naturale",
				"items": [
					"Restare sui sentieri segnalati durante le passeggiate.",
					"Limitare il rumore serale per preservare la tranquillità del luogo.",
					"Osservare fauna e flora senza disturbarle.",
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
			"bus": "Lignes de bus",
			"environment": "Astuces environnement",
			"history": "Histoire de Bilieu",
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
		"history": {
			"title": "L'histoire de Bilieu",
			"text": "Village du pays voironnais, Bilieu s'est développé autour de ses terres agricoles et de sa relation privilégiée avec le lac de Paladru. Son identité mêle patrimoine rural, vie locale et tourisme nature.",
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
			"bus": "Bus lines",
			"environment": "Environment tips",
			"history": "History of Bilieu",
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
		"history": {
			"title": "The history of Bilieu",
			"text": "Bilieu, in the Voironnais area, grew around farming traditions and a strong connection to Lake Paladru. Its identity combines rural heritage, local life, and nature-oriented tourism.",
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
			"bus": "Linee bus",
			"environment": "Consigli ambiente",
			"history": "Storia di Bilieu",
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
		"history": {
			"title": "La storia di Bilieu",
			"text": "Bilieu, nel territorio del Voironnais, si è sviluppata tra tradizione agricola e legame con il lago di Paladru. La sua identità unisce patrimonio rurale, vita locale e turismo nella natura.",
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


@app.route("/privacy")
def privacy():
	lang = request.args.get("lang", "fr").lower()
	if lang not in SUPPORTED_LANGS:
		lang = "fr"

	return render_template(
		"privacy.html",
		lang=lang,
		supported_langs=SUPPORTED_LANGS,
		content=CONTENT[lang],
		legal=LEGAL_CONTENT[lang],
	)


@app.route("/history")
def history():
	lang = request.args.get("lang", "fr").lower()
	if lang not in SUPPORTED_LANGS:
		lang = "fr"

	return render_template(
		"history.html",
		lang=lang,
		supported_langs=SUPPORTED_LANGS,
		content=CONTENT[lang],
		history=HISTORY_CONTENT[lang],
	)


@app.route("/bus")
def bus():
	lang = request.args.get("lang", "fr").lower()
	if lang not in SUPPORTED_LANGS:
		lang = "fr"

	return render_template(
		"bus.html",
		lang=lang,
		supported_langs=SUPPORTED_LANGS,
		content=CONTENT[lang],
		bus=BUS_CONTENT[lang],
	)


@app.route("/environment")
def environment():
	lang = request.args.get("lang", "fr").lower()
	if lang not in SUPPORTED_LANGS:
		lang = "fr"

	return render_template(
		"environment.html",
		lang=lang,
		supported_langs=SUPPORTED_LANGS,
		content=CONTENT[lang],
		environment=ENVIRONMENT_CONTENT[lang],
	)


if __name__ == "__main__":
	app.run(debug=True)
