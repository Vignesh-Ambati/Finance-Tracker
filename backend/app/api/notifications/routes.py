from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.notification_service import NotificationService

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/', methods=['GET'])
@jwt_required()
def get_notifications():
    unread_only = request.args.get('unread', 'false').lower() == 'true'
    notifs = NotificationService.get_notifications(get_jwt_identity(), unread_only)
    return jsonify([n.to_dict() for n in notifs]), 200

@notifications_bp.route('/unread-count', methods=['GET'])
@jwt_required()
def get_unread_count():
    count = NotificationService.get_unread_count(get_jwt_identity())
    return jsonify({'unread_count': count}), 200

@notifications_bp.route('/<int:id>/read', methods=['POST', 'PATCH'])
@jwt_required()
def mark_as_read(id):
    notif = NotificationService.mark_as_read(id, get_jwt_identity())
    if not notif:
        return jsonify({'error': 'Notification not found'}), 404
    return jsonify(notif.to_dict()), 200

@notifications_bp.route('/read-all', methods=['POST'])
@notifications_bp.route('/mark-all-read', methods=['POST'])
@jwt_required()
def mark_all_as_read():
    count = NotificationService.mark_all_as_read(get_jwt_identity())
    return jsonify({'message': f'Marked {count} notifications as read'}), 200
