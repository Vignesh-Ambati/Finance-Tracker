from datetime import datetime
from app.extensions import db
from app.models import InterestCollection, Loan

class InterestService:
    @staticmethod
    def calculate_interest(loan):
        today = datetime.utcnow().date()
        date_given = loan.date_given.date() if hasattr(loan.date_given, 'date') else loan.date_given
        if isinstance(date_given, datetime):
            date_given = date_given.date()
        
        days_elapsed = max(0, (today - date_given).days)
        months_elapsed = days_elapsed / 30.436875
        
        p = float(loan.principal_amount)
        r = float(loan.interest_rate)
        total_accrued = (p * r * days_elapsed) / (100 * 365)
        
        total_collected = sum(c.amount_collected for c in loan.collections)
        pending = max(0.0, total_accrued - total_collected)
        
        daily_rate = (p * r) / (100 * 365)
        monthly_rate = daily_rate * 30.436875
        
        return {
            'total_accrued': round(total_accrued, 2),
            'total_collected': round(total_collected, 2),
            'pending': round(pending, 2),
            'daily_rate': round(daily_rate, 4),
            'monthly_rate': round(monthly_rate, 2),
            'days_elapsed': days_elapsed,
            'months_elapsed': round(months_elapsed, 2)
        }

    @staticmethod
    def record_collection(loan_id, user_id, amount, date_collected, period_start=None, period_end=None, notes=None):
        loan = Loan.query.filter_by(id=loan_id, user_id=user_id).first()
        if not loan:
            return None
        collection = InterestCollection(
            loan_id=loan_id,
            amount_collected=amount,
            date_collected=date_collected,
            period_start=period_start,
            period_end=period_end,
            notes=notes
        )
        db.session.add(collection)
        db.session.commit()
        return collection

    @staticmethod
    def get_collections(loan_id, user_id):
        loan = Loan.query.filter_by(id=loan_id, user_id=user_id).first()
        if not loan:
            return None
        return InterestCollection.query.filter_by(loan_id=loan_id).all()

    @staticmethod
    def get_pending_collections(user_id):
        loans = Loan.query.filter_by(user_id=user_id, status='active').all()
        pending_loans = []
        for loan in loans:
            info = InterestService.calculate_interest(loan)
            if info['pending'] > 0:
                pending_loans.append({
                    'loan': loan.to_dict(),
                    'interest_info': info
                })
        return pending_loans
