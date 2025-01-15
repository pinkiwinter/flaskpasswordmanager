from flask import Flask, Blueprint, jsonify, request
from app.schemas import UserS
from app.models import db, User
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token

authb = Blueprint('auth', __name__)

@authb.route('/register', methods=['POST'])
def register():
    user_schema = UserS()

    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data'}), 400
        
        user_data = user_schema.load(data)
        password = user_data.get('master_password')
        email = user_data.get('email')

        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify({'error': 'An account with this email already exists. Please log in or use a different email to sign up.'}), 400

        hashed_password = generate_password_hash(password)
        user = User(email=email, master_password=hashed_password)

        db.session.add(user)
        db.session.commit()

    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {e}. Please try again later.'}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': f'Data base error: {e}. Please try again later.'}), 500
    
    return jsonify({'message': "Registration successful! You're all set!"}), 200


@authb.route('/login', methods=['POST'])
def login():
    user_schema = UserS(partial=True)

    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data'}), 400
        
        user_data = user_schema.load(data)
        email = user_data.get('email')
        password = user_data.get('master_password')

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.master_password, password):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        access_token = create_access_token(identity=user.id)

    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {e}. Please try again later.'}), 400

    return jsonify(access_token=access_token), 200
    
