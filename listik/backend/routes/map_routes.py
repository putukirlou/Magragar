from flask import Blueprint, jsonify
from services.map_service import assemble_map, save_map_to_db

map_bp = Blueprint("map", __name__)

@map_bp.route("/generate_map", methods=["GET"])
def generate_map():
    full_map = assemble_map()
    save_map_to_db(full_map)
    return jsonify({"message": "Карта успешно создана"})
