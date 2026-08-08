import os
from flask import Flask, render_template

app = Flask(__name__)

GUIDE_CONTENT = {
    "description": "Découvrez notre logement spacieux et confortable",
    "amenities": [
        "Salon/hall : 1 canapé convertible confortable pour 2 personnes.",
        "1er étage : 2 pièces (1 bureau + 1 chambre avec 1 lit simple).",
        "2e étage : 1 chambre avec 1 lit simple + 1 fauteuil-lit",
        "2e étage : 1 chambre avec 1 lit double (couple).",
        "climatisation": {
            "type": "climatisation",
            "description": "Climatisation centralisée"
        }
    ]
}

@app.route('/')
def home():
    return render_template('index.html', content=GUIDE_CONTENT)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)
