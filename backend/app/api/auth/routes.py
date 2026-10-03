from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt, decode_token
from datetime import timedelta
from app.services.auth_service import AuthService
from app.services.email_service import EmailService
from app.utils.decorators import get_current_user
from app.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400
    try:
        user = AuthService.register(data['username'], data['email'], data['password'], data.get('phone_number'))
        token = create_access_token(identity=str(user.id))
        return jsonify({'user': user.to_dict(), 'token': token}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400
    result = AuthService.login(data['email'], data['password'])
    if not result:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    user = result['user']
    if result['requires_2fa']:
        temp_token = create_access_token(
            identity=str(user.id),
            expires_delta=timedelta(minutes=5),
            additional_claims={'type': '2fa_pending'}
        )
        return jsonify({'requires_2fa': True, 'temp_token': temp_token}), 200
    else:
        token = create_access_token(identity=str(user.id))
        return jsonify({'token': token, 'user': user.to_dict()}), 200

@auth_bp.route('/verify-2fa', methods=['POST'])
def verify_2fa():
    data = request.get_json() or {}
    temp_token = data.get('temp_token')
    
    # Also support Authorization header if supplied
    auth_header = request.headers.get('Authorization')
    if not temp_token and auth_header and auth_header.startswith('Bearer '):
        temp_token = auth_header.split(' ')[1]
        
    if not temp_token:
        return jsonify({'error': 'Missing temporary token'}), 400
        
    try:
        claims = decode_token(temp_token)
    except Exception as e:
        return jsonify({'error': 'Invalid or expired temporary token'}), 401
        
    if claims.get('type') != '2fa_pending':
        return jsonify({'error': 'Invalid token type'}), 403
        
    totp_code = data.get('totp_code')
    user_id = claims.get('sub')
    
    if AuthService.verify_2fa(user_id, totp_code):
        token = create_access_token(identity=str(user_id))
        return jsonify({'token': token}), 200
    return jsonify({'error': 'Invalid code'}), 401

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json() or {}
    email = data.get('email')
    if email:
        token = AuthService.generate_reset_token(email)
        user = User.query.filter_by(email=email).first()
        if user:
            EmailService.send_password_reset(user, token, current_app.config.get('FRONTEND_URL', 'http://localhost:3000'))
    return jsonify({'message': 'If an account exists, an email was sent.'}), 200

@auth_bp.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    data = request.get_json() or {}
    new_password = data.get('password')
    if not new_password:
        return jsonify({'error': 'Password required'}), 400
    user = AuthService.verify_reset_token(token)
    if not user:
        return jsonify({'error': 'Invalid or expired token'}), 400
    AuthService.reset_password(user, new_password)
    return jsonify({'message': 'Password reset successfully'}), 200

@auth_bp.route('/setup-2fa', methods=['GET'])
@jwt_required()
def setup_2fa():
    user_id = get_jwt_identity()
    result = AuthService.setup_2fa(user_id)
    if result:
        return jsonify(result), 200
    return jsonify({'error': 'Failed to setup 2FA'}), 400

@auth_bp.route('/enable-2fa', methods=['POST'])
@jwt_required()
def enable_2fa():
    data = request.get_json() or {}
    totp_code = data.get('totp_code')
    if AuthService.enable_2fa(get_jwt_identity(), totp_code):
        return jsonify({'message': '2FA enabled'}), 200
    return jsonify({'error': 'Invalid code'}), 400

@auth_bp.route('/disable-2fa', methods=['POST'])
@jwt_required()
def disable_2fa():
    data = request.get_json() or {}
    if AuthService.disable_2fa(get_jwt_identity(), data.get('password'), data.get('totp_code')):
        return jsonify({'message': '2FA disabled'}), 200
    return jsonify({'error': 'Invalid credentials or code'}), 400

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
@get_current_user
def get_profile(current_user):
    return jsonify(current_user.to_dict()), 200

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user = AuthService.update_profile(get_jwt_identity(), request.get_json() or {})
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({'error': 'Failed to update profile'}), 400
