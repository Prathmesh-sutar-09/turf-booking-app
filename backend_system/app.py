from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db
from routes.auth import auth_bp
from routes.slot import slot_bp
from routes.booking import booking_bp
from routes.payment import payment_bp

app =Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Initialize JWT
jwt = JWTManager(app)

# Registers auth blueprint
app.register_blueprint(auth_bp)

app.register_blueprint(slot_bp)

app.register_blueprint(booking_bp)

app.register_blueprint(payment_bp)

@app.route("/")
def home():
    return "Turf Booking Backend Running"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # create tables
    app.run(debug=True)    
    #app.run(debug=True, port=5050)