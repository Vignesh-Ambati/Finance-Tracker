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

    # CORS setup: Parse allowed origins from FRONTEND_URL or allow all in development
    frontend_raw = app.config.get('FRONTEND_URL', 'http://localhost:3000')
    allowed_origins = [url.strip().rstrip('/') for url in frontend_raw.split(',') if url.strip()]
    if not allowed_origins or '*' in allowed_origins:
        CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    else:
        # Also always permit localhost during local development
        for dev_url in ['http://localhost:3000', 'http://127.0.0.1:3000']:
            if dev_url not in allowed_origins:
                allowed_origins.append(dev_url)
        CORS(app, resources={r"/*": {"origins": allowed_origins}}, supports_credentials=True)

    # Health check for deployment platforms (Render, Railway, Uptime monitors)
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
