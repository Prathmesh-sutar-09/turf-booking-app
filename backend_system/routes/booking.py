from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.booking_service import book_slot
from services.booking_service import get_user_bookings
from services.booking_service import cancel_booking

booking_bp = Blueprint("booking", __name__)

@booking_bp.route("/book", methods=["POST"])
@jwt_required()
def book():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    booking = book_slot(
        user_id,
        data["turf_id"],
        data["slot_id"],
        data["booking_date"]
    )
    
    if not booking:
        return jsonify({"message":"Slot already booked"}), 409
    
    return jsonify({"message":"Booking confirmed"}), 201


@booking_bp.route("/my-bookings", methods=["GET"])
@jwt_required()
def my_bookings():
    user_id = int(get_jwt_identity())
    
    bookings = get_user_bookings(user_id)
    return jsonify(bookings), 200


@booking_bp.route("/cancel_booking", methods=["POST"])
@jwt_required()
def cancel():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    booking_id = data.get("booking_id")
    if not booking_id:
        return jsonify({"message": "booking_id required"}), 400

    booking = cancel_booking(user_id, booking_id)

    if not booking:
        return jsonify({"message": "Booking not found"}), 404

    return jsonify({"message": "Booking cancelled successfully"}), 200