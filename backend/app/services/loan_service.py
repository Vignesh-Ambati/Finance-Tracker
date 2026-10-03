from app.extensions import db
from app.models import Loan, InterestCollection
from app.services.interest_service import InterestService

class LoanService:
    @staticmethod
    def create_loan(user_id, borrower_id, principal_amount, interest_rate, date_given, due_date=None, notes=None):
        loan = Loan(
            user_id=user_id,
            borrower_id=borrower_id,
            principal_amount=principal_amount,
            interest_rate=interest_rate,
            date_given=date_given,
            due_date=due_date,
            notes=notes,
            status='active'
        )
        db.session.add(loan)
        db.session.commit()
        return loan

    @staticmethod
    def get_loans(user_id, status=None, page=1, per_page=20):
        query = Loan.query.filter_by(user_id=user_id)
        if status:
            query = query.filter_by(status=status)
        
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        all_loans = Loan.query.filter_by(user_id=user_id).all()
        total_outstanding = sum(l.principal_amount for l in all_loans if l.status == 'active')
        active_count = sum(1 for l in all_loans if l.status == 'active')
        
        collections = InterestCollection.query.join(Loan).filter(Loan.user_id == user_id).all()
        total_interest_earned = sum(c.amount_collected for c in collections)
        
        summary = {
            'total_outstanding': total_outstanding,
            'total_interest_earned': total_interest_earned,
            'active_count': active_count
        }
        
        return {
            'loans': [loan.to_dict() for loan in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'summary': summary
        }

    @staticmethod
    def get_loan(loan_id, user_id):
        return Loan.query.filter_by(id=loan_id, user_id=user_id).first()

    @staticmethod
    def update_loan(loan_id, user_id, data: dict):
        loan = Loan.query.filter_by(id=loan_id, user_id=user_id).first()
        if not loan:
            return None
        for key, value in data.items():
            if hasattr(loan, key) and key not in ['id', 'user_id', 'created_at', 'updated_at']:
                setattr(loan, key, value)
        db.session.commit()
        return loan

    @staticmethod
    def close_loan(loan_id, user_id, final_notes=None):
        loan = Loan.query.filter_by(id=loan_id, user_id=user_id).first()
        if not loan:
            return None
        loan.status = 'closed'
        if final_notes:
            loan.notes = (loan.notes + f"\nClosing notes: {final_notes}") if loan.notes else final_notes
        db.session.commit()
        return loan

    @staticmethod
    def get_loan_with_interest(loan_id, user_id):
        loan = Loan.query.filter_by(id=loan_id, user_id=user_id).first()
        if not loan:
            return None
        interest_info = InterestService.calculate_interest(loan)
        return {
            'loan': loan.to_dict(),
            'interest_info': interest_info
        }
