from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.payment_service import make_payment


payment_bp = Blueprint("payment", __name__)

@payment_bp.route("/pay", methods=["POST"])
@jwt_required()
def pay():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    booking_id = data.get("booking_id")
    if not booking_id:
        return jsonify({"message":"booking_id required"}), 400
    
    booking, msg = make_payment(user_id, booking_id)
    if not booking:
        return jsonify({"message":msg}), 404
    
    return jsonify({
        "message":msg,
        "payment_status":booking.payment_status
    }), 200