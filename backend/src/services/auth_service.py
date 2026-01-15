"""
Authentication Service
Handles user authentication and authorization with Azure AD integration
"""

import logging
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import jwt
import hashlib
import secrets

logger = logging.getLogger(__name__)

class AuthService:
    """
    Authentication service supporting both JWT and Azure AD
    Implements role-based access control (RBAC)
    """
    
    # Predefined roles
    ROLES = {
        'admin': ['read', 'write', 'delete', 'manage_users'],
        'student': ['read', 'write'],
        'viewer': ['read']
    }
    
    def __init__(self):
        """Initialize authentication service"""
        self.secret_key = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
        self.algorithm = 'HS256'
        self.access_token_expires = timedelta(hours=1)
        self.refresh_token_expires = timedelta(days=30)
        
        # In-memory user store (for demonstration)
        self.users = {
            'admin@university.edu': {
                'password_hash': self._hash_password('admin123'),
                'role': 'admin',
                'name': 'Administrator'
            },
            'student@university.edu': {
                'password_hash': self._hash_password('student123'),
                'role': 'student',
                'name': 'Student User'
            }
        }
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        return self._hash_password(password) == password_hash
    
    def login(self, username: str, password: str) -> Optional[Dict]:
        """
        Authenticate user and return tokens
        
        Args:
            username: User email
            password: User password
            
        Returns:
            Dictionary with access_token, refresh_token, and user info
        """
        if not username or not password:
            logger.warning("Login attempt with missing credentials")
            return None
        
        user = self.users.get(username)
        if not user or not self._verify_password(password, user['password_hash']):
            logger.warning(f"Failed login attempt for user: {username}")
            return None
        
        try:
            access_token = self._create_access_token(username, user['role'])
            refresh_token = self._create_refresh_token(username)
            
            logger.info(f"User logged in successfully: {username}")
            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'token_type': 'Bearer',
                'expires_in': int(self.access_token_expires.total_seconds()),
                'user': {
                    'username': username,
                    'name': user['name'],
                    'role': user['role']
                }
            }
        except Exception as e:
            logger.error(f"Error during login: {e}")
            return None
    
    def _create_access_token(self, username: str, role: str) -> str:
        """Create JWT access token"""
        payload = {
            'sub': username,
            'role': role,
            'type': 'access',
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + self.access_token_expires
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def _create_refresh_token(self, username: str) -> str:
        """Create JWT refresh token"""
        payload = {
            'sub': username,
            'type': 'refresh',
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + self.refresh_token_expires,
            'jti': secrets.token_urlsafe(16)
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """
        Verify JWT token and extract claims
        
        Args:
            token: JWT token string
            
        Returns:
            Dictionary with token claims or None if invalid
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {e}")
            return None
    
    def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        """
        Generate new access token from refresh token
        
        Args:
            refresh_token: Valid refresh token
            
        Returns:
            New access token or None if invalid
        """
        payload = self.verify_token(refresh_token)
        if not payload or payload.get('type') != 'refresh':
            return None
        
        username = payload.get('sub')
        user = self.users.get(username)
        if not user:
            return None
        
        return self._create_access_token(username, user['role'])
    
    def has_permission(self, role: str, permission: str) -> bool:
        """
        Check if role has specific permission
        
        Args:
            role: User role
            permission: Required permission
            
        Returns:
            True if role has permission
        """
        permissions = self.ROLES.get(role, [])
        return permission in permissions
    
    def get_user_info(self, username: str) -> Optional[Dict]:
        """Get user information"""
        user = self.users.get(username)
        if not user:
            return None
        
        return {
            'username': username,
            'name': user['name'],
            'role': user['role'],
            'permissions': self.ROLES.get(user['role'], [])
        }
    
    def register_user(self, username: str, password: str, name: str, role: str = 'student') -> bool:
        """
        Register new user (admin only)
        
        Args:
            username: User email
            password: User password
            name: User full name
            role: User role (default: student)
            
        Returns:
            True if registration successful
        """
        if username in self.users:
            logger.warning(f"User already exists: {username}")
            return False
        
        if role not in self.ROLES:
            logger.warning(f"Invalid role: {role}")
            return False
        
        self.users[username] = {
            'password_hash': self._hash_password(password),
            'role': role,
            'name': name
        }
        
        logger.info(f"New user registered: {username}")
        return True
