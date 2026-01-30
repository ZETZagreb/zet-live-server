import requests
from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Link na ZET-ove podatke
ZET_URL = "https://www.zet.hr/gtfs-rt-2.0/realtime/vehicle-positions"

@app.route('/')
def home():
    return "ZET Live API je aktivan na Starter planu!"

@app.route('/podaci')
def get_data():
    try:
        # 1. Dohvaćanje podataka sa ZET-a
        r = requests.get(ZET_URL, timeout=10)
        
        # 2. Privremeno rješenje: Dok ne složimo cijeli parser, 
        # šaljemo testno vozilo da provjerimo miče li se tekst s karte
        test_vozila = [
            {"id": "test1", "lat": 45.813, "lon": 15.977, "linija": "11", "tip": "tram", "oznaka": "123"}
        ]
        
        # Kad proradi parser, ovdje će ići stvarni podaci
        return jsonify(test_vozila)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
