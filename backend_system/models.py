from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

db = SQLAlchemy()

#--------------------------USER MODEL--------------------------------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    bookings = db.relationship(
        "Booking",
        backref="user",
        lazy=True
    )

# ---------------- TURF MODEL ----------------
class Turf(db.Model):
    __tablename__ = "turfs"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(200), nullable=False)

    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    price_per_hour = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    slots = db.relationship("Slot", backref="turf", lazy=True)
    bookings = db.relationship("Booking", backref="turf", lazy=True)


# ---------------- SLOT MODEL ----------------
class Slot(db.Model):
    __tablename__ = "slots"

    id = db.Column(db.Integer, primary_key=True)
    turf_id = db.Column(db.Integer, db.ForeignKey("turfs.id"), nullable=False)

    start_time = db.Column(db.String(10), nullable=False)  # "06:00"
    end_time = db.Column(db.String(10), nullable=False)    # "07:00"

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    bookings = db.relationship("Booking", backref="slot", lazy=True)


# ---------------- BOOKING MODEL ----------------
class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    turf_id = db.Column(
        db.Integer,
        db.ForeignKey("turfs.id"),
        nullable=False
    )

    slot_id = db.Column(
        db.Integer,
        db.ForeignKey("slots.id"),
        nullable=False
    )

    booking_date = db.Column(db.String(20), nullable=False)

    status = db.Column(db.String(20), default="CONFIRMED")
    payment_status = db.Column(db.String(20), default="PENDING")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint(
            "turf_id", "slot_id", "booking_date",
            name="unique_slot_booking"
        ),
    )