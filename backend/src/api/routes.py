"""
API Routes
Defines all RESTful endpoints for the sentiment analysis system
"""

from flask import Blueprint, request, jsonify, current_app
from functools import wraps
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__)

def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid authorization header'}), 401
        
        token = auth_header.replace('Bearer ', '')
        payload = current_app.auth_service.verify_token(token)
        
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Add user info to request context
        request.user = payload
        return f(*args, **kwargs)
    
    return decorated_function

def require_role(role):
    """Decorator to require specific role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(request, 'user'):
                return jsonify({'error': 'Authentication required'}), 401
            
            user_role = request.user.get('role')
            if user_role != role and user_role != 'admin':
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Authentication Endpoints

@api_bp.route('/auth/login', methods=['POST'])
def login():
    """
    User login endpoint
    
    Request body:
    {
        "username": "user@university.edu",
        "password": "password"
    }
    
    Returns:
        - access_token: JWT token for API requests
        - refresh_token: Token to refresh access token
        - user: User information
    """
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Missing username or password'}), 400
        
        result = current_app.auth_service.login(
            data['username'],
            data['password']
        )
        
        if not result:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/auth/refresh', methods=['POST'])
def refresh_token():
    """
    Refresh access token endpoint
    
    Request body:
    {
        "refresh_token": "refresh_token_value"
    }
    
    Returns:
        - access_token: New JWT token
    """
    try:
        data = request.get_json()
        refresh_token = data.get('refresh_token') if data else None
        
        if not refresh_token:
            return jsonify({'error': 'Missing refresh token'}), 400
        
        new_token = current_app.auth_service.refresh_access_token(refresh_token)
        
        if not new_token:
            return jsonify({'error': 'Invalid refresh token'}), 401
        
        return jsonify({
            'access_token': new_token,
            'token_type': 'Bearer'
        }), 200
    
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/auth/user', methods=['GET'])
@require_auth
def get_user_info():
    """
    Get current user information
    
    Returns:
        - User profile and permissions
    """
    try:
        username = request.user.get('sub')
        user_info = current_app.auth_service.get_user_info(username)
        
        if not user_info:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user_info), 200
    
    except Exception as e:
        logger.error(f"Error getting user info: {e}")
        return jsonify({'error': 'Internal server error'}), 500

# Sentiment Analysis Endpoints

@api_bp.route('/analyze', methods=['POST'])
@require_auth
def analyze_sentiment():
    """
    Analyze sentiment of a single text
    
    Request body:
    {
        "text": "This product is amazing!"
    }
    
    Returns:
        - sentiment: positive, negative, or neutral
        - confidence: confidence score (0-1)
        - scores: detailed scores for each sentiment
    """
    try:
        data = request.get_json()
        
        if not data or not data.get('text'):
            return jsonify({'error': 'Missing text field'}), 400
        
        text = data['text'].strip()
        if len(text) == 0:
            return jsonify({'error': 'Text cannot be empty'}), 400
        
        if len(text) > 5000:
            return jsonify({'error': 'Text exceeds maximum length of 5000 characters'}), 400
        
        result = current_app.sentiment_analyzer.predict(text)
        
        return jsonify({
            'success': True,
            'data': result,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Sentiment analysis error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/batch', methods=['POST'])
@require_auth
def analyze_batch():
    """
    Analyze sentiment for multiple texts
    
    Request body:
    {
        "texts": [
            "This is great!",
            "This is terrible.",
            "This is okay."
        ]
    }
    
    Returns:
        - Array of sentiment predictions
    """
    try:
        data = request.get_json()
        
        if not data or not data.get('texts'):
            return jsonify({'error': 'Missing texts field'}), 400
        
        texts = data['texts']
        
        if not isinstance(texts, list):
            return jsonify({'error': 'texts must be an array'}), 400
        
        if len(texts) == 0:
            return jsonify({'error': 'texts array cannot be empty'}), 400
        
        if len(texts) > 100:
            return jsonify({'error': 'Maximum 100 texts per request'}), 400
        
        # Validate each text
        for text in texts:
            if not isinstance(text, str) or len(text.strip()) == 0:
                return jsonify({'error': 'All texts must be non-empty strings'}), 400
        
        results = current_app.sentiment_analyzer.predict_batch(texts)
        
        return jsonify({
            'success': True,
            'count': len(results),
            'data': results,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        logger.error(f"Batch analysis error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/model/info', methods=['GET'])
@require_auth
def get_model_info():
    """
    Get information about the sentiment analysis model
    
    Returns:
        - Model type, features, and capabilities
    """
    try:
        info = current_app.sentiment_analyzer.get_model_info()
        return jsonify({
            'success': True,
            'data': info
        }), 200
    
    except Exception as e:
        logger.error(f"Error getting model info: {e}")
        return jsonify({'error': 'Internal server error'}), 500

# Admin Endpoints

@api_bp.route('/admin/stats', methods=['GET'])
@require_auth
@require_role('admin')
def get_stats():
    """
    Get system statistics (admin only)
    
    Returns:
        - System health and usage statistics
    """
    try:
        return jsonify({
            'success': True,
            'data': {
                'status': 'operational',
                'timestamp': datetime.utcnow().isoformat(),
                'model_info': current_app.sentiment_analyzer.get_model_info()
            }
        }), 200
    
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/admin/users', methods=['GET'])
@require_auth
@require_role('admin')
def list_users():
    """
    List all users (admin only)
    
    Returns:
        - List of user information
    """
    try:
        users = []
        for username in current_app.auth_service.users:
            user_info = current_app.auth_service.get_user_info(username)
            if user_info:
                users.append(user_info)
        
        return jsonify({
            'success': True,
            'count': len(users),
            'data': users
        }), 200
    
    except Exception as e:
        logger.error(f"Error listing users: {e}")
        return jsonify({'error': 'Internal server error'}), 500
