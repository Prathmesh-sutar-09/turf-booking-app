from sqlalchemy.exc import IntegrityError
from models import db, Booking
from models import Booking

def book_slot(user_id, turf_id, slot_id, booking_date):
    booking = Booking(
        user_id=user_id,
        turf_id=turf_id,
        slot_id=slot_id,
        booking_date=booking_date
    )
    
    try:
        db.session.add(booking)
        db.session.commit()
        return booking
    
    except IntegrityError:
        db.session.rollback()
        return None
        
        
def get_user_bookings(user_id):
    # Returns all bookings of a user ordered by latest first
    
    bookings = Booking.query.filter_by(
        user_id=user_id
    ).order_by(Booking.created_at.desc()).all()
    
    result = []
    for booking in bookings:
        result.append({
            "booking_id": booking.id,
            "turf_id": booking.turf_id,
            "slot_id": booking.slot_id,
            "booking_date": booking.booking_date,
            "status": booking.status,
            "payment_status": booking.payment_status,
            "created_at": booking.created_at.isoformat()
        })
        
    return result    
            
def cancel_booking(user_id, booking_id):
    # Cancels a booking if it belongs to the user
    
    booking = Booking.query.filter_by(
        id = booking_id,
        user_id=user_id
    ).first()
    
    if not booking:
        return None
    
    if booking.status == "CANCELLED":
        return booking
    
    booking.status = "CANCELLED"
    db.session.commit()
    
    return booking
                