import requests
from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

ZET_URL = "https://www.zet.hr/gtfs-rt-2.0/realtime/vehicle-positions"

@app.route('/')
def home():
    return "ZET Live API - Podaci s internim brojevima"

@app.route('/podaci')
def get_data():
    try:
        # Dohvaćamo sirove podatke
        r = requests.get(ZET_URL, timeout=10)
        
        # Ovdje simuliramo obradu svih polja koja ZET šalje.
        # Dodajemo 'id' (interni broj vozila) i 'brzina' (speed).
        podaci_s_detaljima = [
            {
                "id": "2201",         # Interni broj vozila
                "lat": 45.8131, 
                "lon": 15.9775, 
                "linija": "11", 
                "tip": "tram",
                "brzina": "24 km/h",  # Podatak o brzini
                "oznaka": "NT2200"    # Tip vozila
            },
            {
                "id": "2245", 
                "lat": 45.8150, 
                "lon": 15.9810, 
                "linija": "6", 
                "tip": "tram",
                "brzina": "12 km/h",
                "oznaka": "NT2200"
            },
            {
                "id": "812", 
                "lat": 45.8010, 
                "lon": 15.9650, 
                "linija": "109", 
                "tip": "bus",
                "brzina": "45 km/h",
                "oznaka": "MAN"
            }
        ]
        
        return jsonify(podaci_s_detaljima)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
