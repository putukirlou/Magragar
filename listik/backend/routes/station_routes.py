from flask import Blueprint, jsonify
from services.station_service import place_stations

station_bp = Blueprint("stations", __name__)

@station_bp.route("/generate_stations", methods=["GET"])
def generate_stations():
    place_stations()
    return jsonify({"message": "Станции успешно установлены"})
