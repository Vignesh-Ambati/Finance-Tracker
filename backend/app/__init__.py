from flask import Flask, jsonify
from flask_cors import CORS
from app.config import Config
from app.extensions import db, bcrypt, jwt, mail
from app.utils.errors import register_error_handlers

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Disable strict slashes so /route and /route/ match uniformly
    app.url_map.strict_slashes = False

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    # Completely open CORS: allows requests from any frontend without circular dependency
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Health check for platforms & monitors
    @app.route('/', methods=['GET'])
    def root_health():
        return jsonify({'status': 'healthy', 'service': 'finance-tracker-api'}), 200

    # Register blueprints
    from app.api import api_bp
    app.register_blueprint(api_bp)

    # Register error handlers
    register_error_handlers(app)

    # Create tables
    with app.app_context():
        db.create_all()

    return app
