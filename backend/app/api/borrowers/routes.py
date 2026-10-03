from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Borrower

borrowers_bp = Blueprint('borrowers', __name__)

@borrowers_bp.route('/', methods=['GET'])
@jwt_required()
def get_borrowers():
    search = request.args.get('search')
    query = Borrower.query.filter_by(user_id=get_jwt_identity())
    if search:
        query = query.filter(Borrower.name.ilike(f'%{search}%'))
    borrowers = query.all()
    return jsonify([b.to_dict() for b in borrowers]), 200

@borrowers_bp.route('/', methods=['POST'])
@jwt_required()
def create_borrower():
    data = request.get_json() or {}
    if not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
    borrower = Borrower(
        user_id=get_jwt_identity(),
        name=data['name'],
        phone=data.get('phone'),
        email=data.get('email'),
        address=data.get('address'),
        notes=data.get('notes')
    )
    db.session.add(borrower)
    db.session.commit()
    return jsonify(borrower.to_dict()), 201

@borrowers_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_borrower(id):
    borrower = Borrower.query.filter_by(id=id, user_id=get_jwt_identity()).first()
    if not borrower:
        return jsonify({'error': 'Borrower not found'}), 404
    data = borrower.to_dict()
    data['loans'] = [loan.to_dict() for loan in borrower.loans]
    return jsonify(data), 200

@borrowers_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_borrower(id):
    borrower = Borrower.query.filter_by(id=id, user_id=get_jwt_identity()).first()
    if not borrower:
        return jsonify({'error': 'Borrower not found'}), 404
    data = request.get_json() or {}
    for field in ['name', 'phone', 'email', 'address', 'notes']:
        if field in data:
            setattr(borrower, field, data[field])
    db.session.commit()
    return jsonify(borrower.to_dict()), 200
