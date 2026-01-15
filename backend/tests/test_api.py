"""
Integration tests for API endpoints
Tests API functionality and authentication
"""

import unittest
import json
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import create_app
from config.settings import TestingConfig

class TestAPIEndpoints(unittest.TestCase):
    """Test cases for API endpoints"""
    
    def setUp(self):
        """Set up test client"""
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Get test tokens
        login_response = self.client.post(
            '/api/v1/auth/login',
            json={'username': 'student@university.edu', 'password': 'student123'}
        )
        self.access_token = login_response.json['access_token']
        self.auth_headers = {'Authorization': f'Bearer {self.access_token}'}
    
    def tearDown(self):
        """Clean up after tests"""
        self.app_context.pop()
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'healthy')
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('name', response.json)
        self.assertIn('version', response.json)
    
    def test_login_success(self):
        """Test successful login"""
        response = self.client.post(
            '/api/v1/auth/login',
            json={'username': 'student@university.edu', 'password': 'student123'}
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json)
        self.assertIn('refresh_token', response.json)
        self.assertIn('user', response.json)
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post(
            '/api/v1/auth/login',
            json={'username': 'student@university.edu', 'password': 'wrong_password'}
        )
        
        self.assertEqual(response.status_code, 401)
    
    def test_login_missing_fields(self):
        """Test login with missing fields"""
        response = self.client.post(
            '/api/v1/auth/login',
            json={'username': 'student@university.edu'}
        )
        
        self.assertEqual(response.status_code, 400)
    
    def test_analyze_sentiment_success(self):
        """Test successful sentiment analysis"""
        response = self.client.post(
            '/api/v1/analyze',
            json={'text': 'This product is amazing!'},
            headers=self.auth_headers
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['success'])
        self.assertIn('data', response.json)
        self.assertIn('sentiment', response.json['data'])
    
    def test_analyze_sentiment_no_auth(self):
        """Test sentiment analysis without authentication"""
        response = self.client.post(
            '/api/v1/analyze',
            json={'text': 'This product is amazing!'}
        )
        
        self.assertEqual(response.status_code, 401)
    
    def test_analyze_sentiment_missing_text(self):
        """Test sentiment analysis with missing text"""
        response = self.client.post(
            '/api/v1/analyze',
            json={},
            headers=self.auth_headers
        )
        
        self.assertEqual(response.status_code, 400)
    
    def test_analyze_sentiment_empty_text(self):
        """Test sentiment analysis with empty text"""
        response = self.client.post(
            '/api/v1/analyze',
            json={'text': ''},
            headers=self.auth_headers
        )
        
        self.assertEqual(response.status_code, 400)
    
    def test_batch_analysis_success(self):
        """Test successful batch analysis"""
        response = self.client.post(
            '/api/v1/batch',
            json={'texts': ['Great!', 'Terrible!', 'Okay.']},
            headers=self.auth_headers
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['success'])
        self.assertEqual(response.json['count'], 3)
    
    def test_batch_analysis_empty_list(self):
        """Test batch analysis with empty list"""
        response = self.client.post(
            '/api/v1/batch',
            json={'texts': []},
            headers=self.auth_headers
        )
        
        self.assertEqual(response.status_code, 400)
    
    def test_batch_analysis_too_many_items(self):
        """Test batch analysis with too many items"""
        texts = ['text'] * 101
        response = self.client.post(
            '/api/v1/batch',
            json={'texts': texts},
            headers=self.auth_headers
        )
        
        self.assertEqual(response.status_code, 400)
    
    def test_model_info_endpoint(self):
        """Test model info endpoint"""
        response = self.client.get(
            '/api/v1/model/info',
            headers=self.auth_headers
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['success'])
        self.assertIn('data', response.json)
    
    def test_get_user_info(self):
        """Test get user info endpoint"""
        response = self.client.get(
            '/api/v1/auth/user',
            headers=self.auth_headers
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('username', response.json)
        self.assertIn('role', response.json)
    
    def test_refresh_token(self):
        """Test token refresh endpoint"""
        # First get refresh token
        login_response = self.client.post(
            '/api/v1/auth/login',
            json={'username': 'student@university.edu', 'password': 'student123'}
        )
        refresh_token = login_response.json['refresh_token']
        
        # Use refresh token
        response = self.client.post(
            '/api/v1/auth/refresh',
            json={'refresh_token': refresh_token}
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json)

if __name__ == '__main__':
    unittest.main()
