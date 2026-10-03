from app.extensions import db
from app.models import Notification, Loan
from app.services.interest_service import InterestService

class NotificationService:
    @staticmethod
    def create_notification(user_id, message, notification_type='reminder', loan_id=None):
        notif = Notification(
            user_id=user_id,
            message=message,
            notification_type=notification_type,
            loan_id=loan_id,
            is_read=False
        )
        db.session.add(notif)
        db.session.commit()
        return notif

    @staticmethod
    def get_notifications(user_id, unread_only=False):
        query = Notification.query.filter_by(user_id=user_id)
        if unread_only:
            query = query.filter_by(is_read=False)
        return query.order_by(Notification.created_at.desc()).all()

    @staticmethod
    def get_unread_count(user_id):
        return Notification.query.filter_by(user_id=user_id, is_read=False).count()

    @staticmethod
    def mark_as_read(notification_id, user_id):
        notif = Notification.query.filter_by(id=notification_id, user_id=user_id).first()
        if notif:
            notif.is_read = True
            db.session.commit()
        return notif

    @staticmethod
    def mark_all_as_read(user_id):
        notifs = Notification.query.filter_by(user_id=user_id, is_read=False).all()
        count = len(notifs)
        for n in notifs:
            n.is_read = True
        if count > 0:
            db.session.commit()
        return count

    @staticmethod
    def create_monthly_reminders():
        active_loans = Loan.query.filter_by(status='active').all()
        for loan in active_loans:
            info = InterestService.calculate_interest(loan)
            if info['pending'] > 0:
                NotificationService.create_notification(
                    user_id=loan.user_id,
                    message=f"Pending interest of {info['pending']} for loan to {loan.borrower.name}",
                    notification_type='reminder',
                    loan_id=loan.id
                )
