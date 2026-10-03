from flask import Blueprint, jsonify
from app.api.auth.routes import auth_bp
from app.api.loans.routes import loans_bp
from app.api.borrowers.routes import borrowers_bp
from app.api.notifications.routes import notifications_bp
from app.api.scheduler import scheduler_bp

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/health', methods=['GET'])
def api_health():
    return jsonify({'status': 'healthy', 'api_version': '1.0'}), 200

api_bp.register_blueprint(auth_bp, url_prefix='/auth')
api_bp.register_blueprint(loans_bp, url_prefix='/loans')
api_bp.register_blueprint(borrowers_bp, url_prefix='/borrowers')
api_bp.register_blueprint(notifications_bp, url_prefix='/notifications')
api_bp.register_blueprint(scheduler_bp, url_prefix='/scheduler')
