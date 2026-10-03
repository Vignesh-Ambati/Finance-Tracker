from flask import jsonify

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
