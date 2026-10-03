from app.extensions import db
from datetime import datetime, timezone

class Loan(db.Model):
    __tablename__ = 'loans'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    borrower_id = db.Column(db.Integer, db.ForeignKey('borrowers.id'), nullable=False)
    principal_amount = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    date_given = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), default='active')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    collections = db.relationship('InterestCollection', backref='loan', lazy='dynamic', order_by='InterestCollection.date_collected.desc()')

    def to_dict(self):
        b_name = self.borrower.name if self.borrower else None
        return {
            'id': self.id,
            'user_id': self.user_id,
            'borrower_id': self.borrower_id,
            'borrower_name': b_name,
            'borrower': {'id': self.borrower_id, 'name': b_name} if b_name else None,
            'principal': self.principal_amount,
            'principal_amount': self.principal_amount,
            'interest_rate': self.interest_rate,
            'date_given': self.date_given.isoformat() if self.date_given else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
