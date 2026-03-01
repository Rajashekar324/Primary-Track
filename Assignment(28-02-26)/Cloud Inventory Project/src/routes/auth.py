from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from src.models.mysql_models import db, User
from src.models.mongo_models import MongoUser, ActivityLog

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register User explicitly in MySQL or MongoDB based on DB choice"""
    data = request.json
    db_choice = data.get('db_choice', 'mysql') # 'mysql' or 'mongodb'
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([username, email, password]):
        return jsonify({"error": "Missing required fields"}), 400

    hashed_pw = generate_password_hash(password)

    if db_choice == 'mysql':
        # Check if exists
        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify({"error": "User already exists in MySQL"}), 400
        
        new_user = User(username=username, email=email, password_hash=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        response_data = new_user.to_dict()
    elif db_choice == 'mongodb':
        user = MongoUser.create_user(username, email, hashed_pw)
        if not user:
            return jsonify({"error": "User already exists in MongoDB"}), 400
        
        # Remove hash for response
        del user['password_hash']
        response_data = user
    else:
        return jsonify({"error": "Invalid db_choice"}), 400

    ActivityLog.log_activity("system", "register", {"username": username, "db_choice": db_choice})
    return jsonify({"message": "Registration successful", "user": response_data, "db": db_choice}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login User from MySQL or MongoDB based on DB choice"""
    data = request.json
    db_choice = data.get('db_choice', 'mysql')
    username = data.get('username')
    password = data.get('password')

    if not all([username, password]):
        return jsonify({"error": "Missing credentials"}), 400

    authenticated = False
    user_id = None

    if db_choice == 'mysql':
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            authenticated = True
            user_id = str(user.id)
    elif db_choice == 'mongodb':
        user = MongoUser.get_user_by_username(username)
        if user and check_password_hash(user['password_hash'], password):
            authenticated = True
            user_id = user['_id']
    else:
        return jsonify({"error": "Invalid db_choice"}), 400

    if authenticated:
        ActivityLog.log_activity(user_id, "login", {"status": "success", "db": db_choice})
        return jsonify({"message": "Login successful", "user_id": user_id, "db": db_choice}), 200
    
    ActivityLog.log_activity(username, "login", {"status": "failed", "db": db_choice})
    return jsonify({"error": "Invalid credentials"}), 401

@auth_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user_mysql(user_id):
    """Get User by ID from MySQL"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"user": user.to_dict()}), 200

@auth_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user_mysql(user_id):
    """Delete User by ID from MySQL"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    db.session.delete(user)
    db.session.commit()
    ActivityLog.log_activity(str(user_id), "delete_user", {"user_id": user_id})
    return jsonify({"message": "User deleted successfully"}), 200
