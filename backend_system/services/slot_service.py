from models import Slot, Booking

def get_available_slots(turf_id, booking_date):
    # get all slots
    slots = Slot.query.filter_by(turf_id=turf_id).all()
    
    
    # get confirmed bookings for that date
    bookings = Booking.query.filter_by(
        turf_id=turf_id,
        booking_date=booking_date,
        status="CONFIRMED"
    ).all()
    
    # hash set booked slot ids
    booked_slot_ids={b.slot_id for b in bookings}
    
    # build response
    result = []
    for slot in slots:
        result.append({
            "slot_id":slot.id,
            "start_time":slot.start_time,
            "end_time":slot.end_time,
            "available":slot.id not in booked_slot_ids
        })
    
    return result    