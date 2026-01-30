import requests
from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# URL ZET-ovih podataka (protobuff format)
ZET_URL = "https://www.zet.hr/gtfs-rt-2.0/realtime/vehicle-positions"

@app.route('/')
def index():
    return "ZET Live API je aktivan!"

@app.route('/podaci')
def get_data():
    try:
        # Povuci svježe podatke sa ZET-a
        response = requests.get(ZET_URL, timeout=10)
        
        # Ovdje bi išlo dekodiranje Protobufa, ali za test
        # ako server samo prosljeđuje status, to je dovoljno.
        # Ako imaš spreman parser, ovdje se on ubacuje.
        
        return jsonify({"status": "ok", "message": "Server je budan!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Render zahtijeva port iz okoline
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
