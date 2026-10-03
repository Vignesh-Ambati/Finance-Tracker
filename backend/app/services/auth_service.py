import pyotp
import qrcode
import base64
import io
from flask import current_app
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from app.extensions import db, bcrypt
from app.models import User

class AuthService:
    @staticmethod
    def register(username, email, password, phone_number=None):
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password_hash=password_hash, phone_number=phone_number)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def login(email, password):
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            return {'user': user, 'requires_2fa': user.is_2fa_enabled}
        return None

    @staticmethod
    def setup_2fa(user_id):
        user = User.query.get(user_id)
        if not user:
            return None
        secret = pyotp.random_base32()
        user.totp_secret = secret
        db.session.commit()
        
        uri = pyotp.TOTP(secret).provisioning_uri(name=user.email, issuer_name='Finance Tracker')
        qrc = qrcode.make(uri)
        buffer = io.BytesIO()
        qrc.save(buffer, format="PNG")
        qr_code_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return {'secret': secret, 'qr_code': qr_code_b64}

    @staticmethod
    def enable_2fa(user_id, totp_code):
        user = User.query.get(user_id)
        if not user or not user.totp_secret:
            return False
        totp = pyotp.TOTP(user.totp_secret)
        if totp.verify(totp_code):
            user.is_2fa_enabled = True
            db.session.commit()
            return True
        return False

    @staticmethod
    def verify_2fa(user_id, totp_code):
        user = User.query.get(user_id)
        if not user or not user.totp_secret:
            return False
        totp = pyotp.TOTP(user.totp_secret)
        return totp.verify(totp_code)

    @staticmethod
    def disable_2fa(user_id, password, totp_code):
        user = User.query.get(user_id)
        if not user or not bcrypt.check_password_hash(user.password_hash, password):
            return False
        totp = pyotp.TOTP(user.totp_secret)
        if totp.verify(totp_code):
            user.is_2fa_enabled = False
            user.totp_secret = None
            db.session.commit()
            return True
        return False

    @staticmethod
    def generate_reset_token(email):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps(email, salt='password-reset-salt')

    @staticmethod
    def verify_reset_token(token, max_age=3600):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            email = serializer.loads(token, salt='password-reset-salt', max_age=max_age)
            return User.query.filter_by(email=email).first()
        except (SignatureExpired, BadSignature):
            return None

    @staticmethod
    def reset_password(user, new_password):
        user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
        db.session.commit()

    @staticmethod
    def update_profile(user_id, data: dict):
        user = User.query.get(user_id)
        if not user:
            return None
        if 'username' in data:
            user.username = data['username']
        if 'phone_number' in data:
            user.phone_number = data['phone_number']
        if 'email' in data:
            user.email = data['email']
        db.session.commit()
        return user
