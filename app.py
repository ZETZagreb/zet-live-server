from flask import Flask, jsonify
from flask_cors import CORS
import requests
from google.transit import gtfs_realtime_pb2

app = Flask(__name__)
CORS(app)

ZET_URL = "https://www.zet.hr/gtfs-rt-protobuf"

@app.route('/podaci')
def get_zet_data():
    try:
        response = requests.get(ZET_URL, timeout=15)
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)
        
        vozila = []
        for entity in feed.entity:
            if entity.HasField('vehicle'):
                v = entity.vehicle
                vozila.append({
                    "linija": v.trip.route_id,
                    "lat": v.position.latitude,
                    "lon": v.position.longitude,
                    "id": v.vehicle.id
                })
        return jsonify(vozila)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":

    app.run(debug=True, port=5000)
