from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.loan_service import LoanService
from app.services.interest_service import InterestService
from datetime import datetime

loans_bp = Blueprint('loans', __name__)

@loans_bp.route('/', methods=['GET'])
@jwt_required()
def get_loans():
    status = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    result = LoanService.get_loans(get_jwt_identity(), status, page)
    return jsonify(result), 200

@loans_bp.route('/', methods=['POST'])
@jwt_required()
def create_loan():
    data = request.get_json() or {}
    
    # Support 'principal' alias from frontend
    if 'principal' in data and 'principal_amount' not in data:
        data['principal_amount'] = data['principal']
        
    required_fields = ['borrower_id', 'principal_amount', 'interest_rate', 'date_given']
    if not all(k in data for k in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    try:
        date_given = datetime.strptime(data['date_given'], '%Y-%m-%d').date()
        due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date() if data.get('due_date') else None
        
        loan = LoanService.create_loan(
            user_id=get_jwt_identity(),
            borrower_id=data['borrower_id'],
            principal_amount=data['principal_amount'],
            interest_rate=data['interest_rate'],
            date_given=date_given,
            due_date=due_date,
            notes=data.get('notes')
        )
        return jsonify(loan.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@loans_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_loan(id):
    result = LoanService.get_loan_with_interest(id, get_jwt_identity())
    if not result:
        return jsonify({'error': 'Loan not found'}), 404
    return jsonify(result), 200

@loans_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_loan(id):
    data = request.get_json() or {}
    if 'principal' in data and 'principal_amount' not in data:
        data['principal_amount'] = data['principal']
    if 'date_given' in data and isinstance(data['date_given'], str):
        data['date_given'] = datetime.strptime(data['date_given'], '%Y-%m-%d').date()
    if 'due_date' in data and data['due_date'] and isinstance(data['due_date'], str):
        data['due_date'] = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
        
    loan = LoanService.update_loan(id, get_jwt_identity(), data)
    if not loan:
        return jsonify({'error': 'Loan not found'}), 404
    return jsonify(loan.to_dict()), 200

@loans_bp.route('/<int:id>/close', methods=['POST', 'PATCH'])
@jwt_required()
def close_loan(id):
    data = request.get_json() or {}
    loan = LoanService.close_loan(id, get_jwt_identity(), data.get('final_notes'))
    if not loan:
        return jsonify({'error': 'Loan not found'}), 404
    return jsonify(loan.to_dict()), 200

@loans_bp.route('/<int:id>/interest', methods=['GET'])
@jwt_required()
def get_interest(id):
    loan = LoanService.get_loan(id, get_jwt_identity())
    if not loan:
        return jsonify({'error': 'Loan not found'}), 404
    return jsonify(InterestService.calculate_interest(loan)), 200

@loans_bp.route('/<int:id>/collect', methods=['POST'])
@jwt_required()
def collect_interest(id):
    data = request.get_json() or {}
    
    # Support 'date' alias from frontend
    if 'date' in data and 'date_collected' not in data:
        data['date_collected'] = data['date']
        
    if 'amount' not in data or 'date_collected' not in data:
        return jsonify({'error': 'Missing amount or date_collected'}), 400
    try:
        date_collected = datetime.strptime(data['date_collected'], '%Y-%m-%d').date()
        period_start = datetime.strptime(data['period_start'], '%Y-%m-%d').date() if data.get('period_start') else None
        period_end = datetime.strptime(data['period_end'], '%Y-%m-%d').date() if data.get('period_end') else None
        
        collection = InterestService.record_collection(
            loan_id=id,
            user_id=get_jwt_identity(),
            amount=data['amount'],
            date_collected=date_collected,
            period_start=period_start,
            period_end=period_end,
            notes=data.get('notes')
        )
        if not collection:
            return jsonify({'error': 'Loan not found'}), 404
        return jsonify(collection.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@loans_bp.route('/<int:id>/collections', methods=['GET'])
@jwt_required()
def get_collections(id):
    collections = InterestService.get_collections(id, get_jwt_identity())
    if collections is None:
        return jsonify({'error': 'Loan not found'}), 404
    return jsonify([c.to_dict() for c in collections]), 200
