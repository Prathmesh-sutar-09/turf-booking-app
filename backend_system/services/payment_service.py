from models import db, Booking

def make_payment(user_id, booking_id):
    booking = Booking.query.filter_by(
        id = booking_id,
        user_id = user_id
    ).first()
    
    if not booking:
        return None, "Booking not found"
    
    if booking.payment_status == "PAID":
        return booking, "Already paid"
    
    booking.payment_status = "PAID"
    db.session.commit()
    
    return booking, "Payment successful"

        