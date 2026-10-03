import os

base_dir = r"c:\Data\Dev\Projects\Finance Tracker\backend"

files = {
    "requirements.txt": """Flask==3.1.1
Flask-SQLAlchemy==3.1.1
Flask-JWT-Extended==4.7.1
Flask-Bcrypt==1.0.1
Flask-Mail==0.10.0
Flask-CORS==5.0.1
pyotp==2.9.0
qrcode[pil]==8.0
APScheduler==3.11.0
python-dotenv==1.1.0
itsdangerous==2.2.0
""",
    ".env.example": """SECRET_KEY=super_secret_key
JWT_SECRET_KEY=super_jwt_secret
DATABASE_URL=sqlite:///finance_tracker.db
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_username
MAIL_PASSWORD=your_password
MAIL_DEFAULT_SENDER=noreply@example.com
FRONTEND_URL=http://localhost:3000
""",
    "app/config.py": """import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default-jwt-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///finance_tracker.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_TOKEN_LOCATION = ['headers']
    
    # Mail Config
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')
""",
    "app/extensions.py": """from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
mail = Mail()
""",
    "app/models/__init__.py": """from app.models.user import User
from app.models.borrower import Borrower
from app.models.loan import Loan
from app.models.interest_collection import InterestCollection
from app.models.notification import Notification
""",
    "app/models/user.py": """from app.extensions import db
from datetime import datetime, timezone

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    totp_secret = db.Column(db.String(32), nullable=True)
    is_2fa_enabled = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    borrowers = db.relationship('Borrower', backref='owner', lazy='dynamic')
    loans = db.relationship('Loan', backref='lender', lazy='dynamic')
    notifications = db.relationship('Notification', backref='recipient', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone_number': self.phone_number,
            'is_2fa_enabled': self.is_2fa_enabled,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
""",
    "app/models/borrower.py": """from app.extensions import db
from datetime import datetime, timezone

class Borrower(db.Model):
    __tablename__ = 'borrowers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    loans = db.relationship('Loan', backref='borrower', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
""",
    "app/models/loan.py": """from app.extensions import db
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
        return {
            'id': self.id,
            'user_id': self.user_id,
            'borrower_id': self.borrower_id,
            'borrower_name': self.borrower.name if self.borrower else None,
            'principal_amount': self.principal_amount,
            'interest_rate': self.interest_rate,
            'date_given': self.date_given.isoformat() if self.date_given else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
""",
    "app/models/interest_collection.py": """from app.extensions import db
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
""",
    "app/models/notification.py": """from app.extensions import db
from datetime import datetime, timezone

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    loan_id = db.Column(db.Integer, db.ForeignKey('loans.id'), nullable=True)
    message = db.Column(db.String(500))
    notification_type = db.Column(db.String(50), default='reminder')
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'loan_id': self.loan_id,
            'message': self.message,
            'notification_type': self.notification_type,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
""",
    "app/utils/__init__.py": "",
    "app/utils/decorators.py": """from functools import wraps
from flask_jwt_extended import get_jwt_identity
from werkzeug.exceptions import NotFound
from app.models.user import User

def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        raise NotFound('User not found')
    return user
""",
    "app/utils/errors.py": """from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': str(error), 'status': 400}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'error': str(error), 'status': 401}), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({'error': str(error), 'status': 403}), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': str(error), 'status': 404}), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({'error': str(error), 'status': 422}), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({'error': 'Internal server error', 'status': 500}), 500
""",
    "app/api/__init__.py": """from flask import Blueprint
from app.api.auth.routes import auth_bp
from app.api.loans.routes import loans_bp
from app.api.notifications.routes import notifications_bp

api_bp = Blueprint('api', __name__, url_prefix='/api')

api_bp.register_blueprint(auth_bp, url_prefix='/auth')
api_bp.register_blueprint(loans_bp, url_prefix='/loans')
api_bp.register_blueprint(notifications_bp, url_prefix='/notifications')
""",
    "app/api/auth/__init__.py": "",
    "app/api/auth/routes.py": """from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
""",
    "app/api/loans/__init__.py": "",
    "app/api/loans/routes.py": """from flask import Blueprint

loans_bp = Blueprint('loans', __name__)
""",
    "app/api/notifications/__init__.py": "",
    "app/api/notifications/routes.py": """from flask import Blueprint

notifications_bp = Blueprint('notifications', __name__)
""",
    "app/__init__.py": """from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.extensions import db, bcrypt, jwt, mail
from app.utils.errors import register_error_handlers

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    # CORS setup
    CORS(app, origins=[app.config.get('FRONTEND_URL', 'http://localhost:3000')])

    # Register blueprints
    from app.api import api_bp
    app.register_blueprint(api_bp)

    # Register error handlers
    register_error_handlers(app)

    # Create tables
    with app.app_context():
        db.create_all()

    # Scheduler initialization
    from app.scheduler.jobs import init_scheduler
    init_scheduler(app)

    return app
""",
    "app/scheduler/__init__.py": "",
    "app/scheduler/jobs.py": """import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.extensions import db
from app.models.loan import Loan
from app.models.notification import Notification

scheduler = BackgroundScheduler()

def monthly_interest_reminder(app):
    with app.app_context():
        active_loans = Loan.query.filter_by(status='active').all()
        for loan in active_loans:
            notif = Notification(
                user_id=loan.user_id,
                loan_id=loan.id,
                message='Reminder to collect interest for your active loan.',
                notification_type='collection_due'
            )
            db.session.add(notif)
        db.session.commit()
        # Email sending logic could go here

def init_scheduler(app):
    if not scheduler.running:
        scheduler.add_job(
            func=monthly_interest_reminder,
            trigger=CronTrigger(day=1, hour=9),
            args=[app],
            id='monthly_interest_reminder',
            replace_existing=True
        )
        scheduler.start()
        atexit.register(lambda: scheduler.shutdown(wait=False))
""",
    "run.py": """from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
"""
}

for path, content in files.items():
    full_path = os.path.join(base_dir, path.replace('/', os.sep))
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Scaffolding completed successfully.")
