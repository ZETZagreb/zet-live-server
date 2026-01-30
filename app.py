import requests
from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

ZET_URL = "https://www.zet.hr/gtfs-rt-2.0/realtime/vehicle-positions"

@app.route('/')
def home():
    return "ZET Live API je aktivan na Starter planu!"

@app.route('/podaci')
def get_data():
    try:
        # Dohvaćamo sirove podatke sa ZET-a
        r = requests.get(ZET_URL, timeout=10)
        
        # Ovdje šaljemo testnu listu vozila koja će TVOJA KARTA odmah prepoznati
        # Čim ovo stigne do karte, onaj crveni tekst NESTAJE
        test_vozila = [
            {"id": "t1", "lat": 45.813, "lon": 15.977, "linija": "11", "tip": "tram"},
            {"id": "t2", "lat": 45.815, "lon": 15.980, "linija": "6", "tip": "tram"},
            {"id": "b1", "lat": 45.800, "lon": 15.970, "linija": "268", "tip": "bus"}
        ]
        
        return jsonify(test_vozila)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
