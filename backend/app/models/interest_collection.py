from app.extensions import db
from datetime import datetime, timezone

class InterestCollection(db.Model):
    __tablename__ = 'interest_collections'
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loans.id'), nullable=False)
    amount_collected = db.Column(db.Float, nullable=False)
    date_collected = db.Column(db.Date, nullable=False)
    period_start = db.Column(db.Date)
    period_end = db.Column(db.Date)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'loan_id': self.loan_id,
            'amount_collected': self.amount_collected,
            'date_collected': self.date_collected.isoformat() if self.date_collected else None,
            'period_start': self.period_start.isoformat() if self.period_start else None,
            'period_end': self.period_end.isoformat() if self.period_end else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
