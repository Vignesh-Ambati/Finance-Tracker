from flask import request, jsonify, current_app
from app.api.scheduler import scheduler_bp
from app.models.loan import Loan
from app.models.user import User
from app.models.notification import Notification
from app.services.email_service import EmailService
from app.extensions import db
from datetime import datetime, timezone
import calendar

@scheduler_bp.route('/monthly-reminders', methods=['POST'])
def trigger_monthly_reminders():
    # 1. Verify the secret token to ensure only our authorized cron service can call this
    provided_secret = request.headers.get('X-Cron-Secret')
    expected_secret = current_app.config.get('CRON_SECRET')
    
    if not provided_secret or provided_secret != expected_secret:
        return jsonify({'error': 'Unauthorized', 'message': 'Invalid or missing X-Cron-Secret header'}), 401
    
    # 2. Fetch all active loans grouped by user
    active_loans = Loan.query.filter_by(status='active').all()
    user_loans_map = {}
    
    for loan in active_loans:
        if loan.user_id not in user_loans_map:
            user_loans_map[loan.user_id] = []
        user_loans_map[loan.user_id].append(loan)
        
    current_date = datetime.now(timezone.utc).date()
    current_year = current_date.year
    current_month = current_date.month
    
    # Get the last day of the current month
    _, last_day_of_month = calendar.monthrange(current_year, current_month)
    
    users_notified = 0
    
    # 3. Build a summary for each user and send emails
    for user_id, loans in user_loans_map.items():
        user = User.query.get(user_id)
        if not user:
            continue
            
        summary_lines = []
        total_interest_due = 0.0
        
        for loan in loans:
            borrower_name = loan.borrower.name if loan.borrower else "Unknown Borrower"
            
            # The interest collection date is typically the same day of the month as when the loan was given
            due_day = loan.date_given.day
            # Adjust if the month doesn't have that many days (e.g. Feb 30 -> Feb 28)
            collection_day = min(due_day, last_day_of_month)
            
            # Formatting the calculated collection date for this month
            collection_date_str = f"{current_year}-{current_month:02d}-{collection_day:02d}"
            
            monthly_interest = loan.principal_amount * (loan.interest_rate / 100)
            total_interest_due += monthly_interest
            
            summary_lines.append(
                f"- Borrower: {borrower_name} | Loan amount: ${loan.principal_amount:.2f} | "
                f"Interest expected: ${monthly_interest:.2f} | Due this month on: {collection_date_str}"
            )
            
        summary_text = "\n".join(summary_lines)
        summary_text += f"\n\nTotal interest expected this month: ${total_interest_due:.2f}"
        
        # 4. Save notification to database for in-app viewing
        notif = Notification(
            user_id=user_id,
            loan_id=None,
            message=f"Monthly reminder: You have {len(loans)} active loans expecting a total of ${total_interest_due:.2f} in interest this month.",
            notification_type='collection_due'
        )
        db.session.add(notif)
        
        # 5. Send the email
        EmailService.send_monthly_reminder(user, summary_text)
        users_notified += 1
        
    db.session.commit()
    
    return jsonify({
        'status': 'success', 
        'message': f'Successfully processed reminders for {users_notified} users',
        'loans_processed': len(active_loans)
    }), 200
