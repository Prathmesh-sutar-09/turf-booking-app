from flask import Blueprint, request, jsonify
from services.slot_service import get_available_slots

slot_bp = Blueprint("slot", __name__)

@slot_bp.route("/slots", methods=["GET"])
def slots():
    turf_id = request.args.get("turf_id")
    date = request.args.get("date")
    
    if not turf_id or not date:
        return jsonify({"message":"turf_id and date required"})
    
    date = get_available_slots(turf_id, date)
    return jsonify(date), 200