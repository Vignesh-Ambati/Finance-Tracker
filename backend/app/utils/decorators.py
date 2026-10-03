from functools import wraps
from flask_jwt_extended import get_jwt_identity
from werkzeug.exceptions import NotFound
from app.models.user import User

def get_current_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            raise NotFound('User not found')
        return f(current_user=user, *args, **kwargs)
    return decorated_function
