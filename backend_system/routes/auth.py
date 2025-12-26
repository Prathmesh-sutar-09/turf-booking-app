from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models import db, User


# to create blueprint
auth_bp = Blueprint("auth", __name__)


# for ragister
@auth_bp.route("/ragister", methods=["POST"])
def ragister():
    data = request.get_json()
    
    # validate input
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"Message":"Missing required fields"}), 400
    
    # check email already exists
    existing_user = User.query.filter_by(email=data["email"]).first()
    if existing_user:
        return jsonify({"Message":"Email already registered"}),409
    
    # hash password
    hashed_password = generate_password_hash(data["password"])
    
    # create user
    user = User(
        name=data.get("name", ""),
        email=data["email"],
        password=hashed_password
    )
    
    # to save database
    db.session.add(user)
    db.session.commit()
    
    return jsonify({"Message":"User reagistered successfully"}), 201


# for login
@auth_bp.route("/login", methods={"POST"})
def login():
    data = request.get_json()
    
    # validate input
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"Message":"Missing credential"}), 400
    
    # fetch users
    user = User.query.filter_by(email=data["email"]).first()
    
    # verify password
    if not user or not check_password_hash(user.password, data["password"]):
        return jsonify({"message":"Invalid credentials"})
    
    # generate JWR token
    access_token= create_access_token(identity=str(user.id))
    
    return jsonify({
        "access_token":access_token,
        "user_id":user.id
    }), 200
        