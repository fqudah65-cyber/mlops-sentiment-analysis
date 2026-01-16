"""
Main Flask Application for Sentiment Analysis MLOps System
Implements RESTful API with authentication and cloud-native integration
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
import logging
import os
from datetime import datetime
import json

from config.settings import Config
from api.routes import api_bp
from services.auth_service import AuthService
from utils.validators import validate_input

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app(config_class=Config):
    """Application factory function"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Enable CORS
    CORS(app)
    
    # Initialize services
    app.sentiment_analyzer = SentimentAnalyzer()
    app.auth_service = AuthService()
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint for deployment verification"""
        return jsonify({
            'status': 'healthy',
            'version': '1.0.0'
        }), 200
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def root():
        """Root endpoint with API information"""
        return jsonify({
            'name': 'Sentiment Analysis MLOps System',
            'version': '1.0.0',
            'description': 'RESTful API for sentiment analysis with cloud-native deployment',
            'endpoints': {
                'health': '/health',
                'analyze': '/api/v1/analyze',
                'batch': '/api/v1/batch',
                'auth': '/api/v1/auth/login'
            }
        }), 200
    
    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request', 'message': str(error)}), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'error': 'Unauthorized', 'message': 'Authentication required'}), 401
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found', 'message': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f'Internal server error: {error}')
        return jsonify({'error': 'Internal server error', 'message': 'An unexpected error occurred'}), 500
    
    logger.info('Application initialized successfully')
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=False)
