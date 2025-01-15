from flask import Blueprint, jsonify, request
from app.models import db, UserAccount, User
from app.schemas import UserAccountS
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.utils import encrypt_data
from sqlalchemy.exc import SQLAlchemyError

add_accounts = Blueprint('add_account', __name__)
accounts = Blueprint('accounts', __name__)

@add_accounts.route('/accounts/add', methods=['POST'])
@jwt_required()
def add_account():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    account_schema = UserAccountS()

    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data.'}), 400
        
        account_data = account_schema.load(data)

        for key, value in account_data.items():
            if key == 'service':
                continue
            if value:
                account_data[key] = value

        user_account = UserAccount(user_id = user_id, **account_data)

        db.session.add(user_account)
        db.session.commit()

    except Exception as e:
        return jsonify({'error': f'An error occurred: {e}. Please try again later.'}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': f'Data base error: {e}. Please try again later.'}), 500
        
    return jsonify({
        'serivce': user_account.service,
        'username': user_account.username,
        'email': user_account.email,
        'password': user_account.password
    }), 201


@accounts.route('/accounts', methods=['GET'])
@jwt_required()
def get_accounts():
    user = get_jwt_identity()
    accounts = UserAccount.query.filter_by(user_id=user)

    service = request.args.get('service')

    if service:
        accounts = accounts.filter(UserAccount.service.ilike(f'%{service}%'))

    accounts = accounts.all()


    return jsonify([{
        'service': acc.service,
        'username': acc.username,
        'email': acc.email,
        'password': acc.password
    } for acc in accounts]), 200