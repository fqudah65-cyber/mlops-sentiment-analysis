# API Documentation

Complete reference for all API endpoints in the Sentiment Analysis MLOps System.

## Base URL

```
http://localhost:5000/api/v1
```

## Authentication

All endpoints except `/auth/login` require JWT authentication.

### Header Format
```
Authorization: Bearer <access_token>
```

### Token Expiration
- Access Token: 1 hour
- Refresh Token: 30 days

## Endpoints

### Authentication Endpoints

#### 1. Login
**POST** `/auth/login`

Authenticate user and receive tokens.

**Request Body:**
```json
{
  "username": "student@university.edu",
  "password": "student123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "user": {
    "username": "student@university.edu",
    "name": "Student User",
    "role": "student"
  }
}
```

**Error Responses:**
- 400: Missing username or password
- 401: Invalid credentials

**Test Credentials:**
- Admin: `admin@university.edu` / `admin123`
- Student: `student@university.edu` / `student123`

---

#### 2. Refresh Token
**POST** `/auth/refresh`

Generate new access token using refresh token.

**Request Body:**
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "Bearer"
}
```

**Error Responses:**
- 400: Missing refresh token
- 401: Invalid refresh token

---

#### 3. Get User Info
**GET** `/auth/user`

Retrieve current authenticated user information.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "username": "student@university.edu",
  "name": "Student User",
  "role": "student",
  "permissions": ["read", "write"]
}
```

**Error Responses:**
- 401: Missing or invalid token
- 404: User not found

---

### Sentiment Analysis Endpoints

#### 4. Analyze Single Text
**POST** `/analyze`

Analyze sentiment of a single text input.

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "text": "This product is absolutely amazing! I love it."
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "text": "This product is absolutely amazing! I love it.",
    "sentiment": "positive",
    "confidence": 0.9234,
    "scores": {
      "negative": 0.0234,
      "positive": 0.9234,
      "neutral": 0.0532
    }
  },
  "timestamp": "2024-01-15T10:30:00.000000"
}
```

**Parameters:**
- `text` (string, required): Text to analyze (1-5000 characters)

**Sentiment Values:**
- `positive`: Positive sentiment detected
- `negative`: Negative sentiment detected
- `neutral`: Neutral sentiment detected

**Confidence Score:**
- Range: 0.0 to 1.0
- Higher values indicate stronger prediction confidence

**Error Responses:**
- 400: Missing or invalid text
- 401: Missing or invalid token
- 500: Internal server error

---

#### 5. Batch Analysis
**POST** `/batch`

Analyze sentiment for multiple texts in a single request.

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "texts": [
    "This is great!",
    "This is terrible.",
    "This is okay."
  ]
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "count": 3,
  "data": [
    {
      "text": "This is great!",
      "sentiment": "positive",
      "confidence": 0.8945,
      "scores": {
        "negative": 0.0523,
        "positive": 0.8945,
        "neutral": 0.0532
      }
    },
    {
      "text": "This is terrible.",
      "sentiment": "negative",
      "confidence": 0.9123,
      "scores": {
        "negative": 0.9123,
        "positive": 0.0234,
        "neutral": 0.0643
      }
    },
    {
      "text": "This is okay.",
      "sentiment": "neutral",
      "confidence": 0.6234,
      "scores": {
        "negative": 0.1234,
        "positive": 0.2532,
        "neutral": 0.6234
      }
    }
  ],
  "timestamp": "2024-01-15T10:30:00.000000"
}
```

**Parameters:**
- `texts` (array, required): Array of strings to analyze
  - Minimum: 1 text
  - Maximum: 100 texts
  - Each text: 1-5000 characters

**Error Responses:**
- 400: Invalid texts array or missing field
- 401: Missing or invalid token
- 500: Internal server error

---

#### 6. Get Model Information
**GET** `/model/info`

Retrieve information about the sentiment analysis model.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "is_trained": true,
    "model_type": "Naive Bayes with TF-IDF",
    "vectorizer": "TF-IDF (max_features=5000, ngram_range=(1,2))",
    "classifier": "Multinomial Naive Bayes",
    "sentiment_classes": ["negative", "positive", "neutral"]
  }
}
```

**Error Responses:**
- 401: Missing or invalid token
- 500: Internal server error

---

### Admin Endpoints

#### 7. Get System Statistics
**GET** `/admin/stats`

Retrieve system statistics and health information (admin only).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "status": "operational",
    "timestamp": "2024-01-15T10:30:00.000000",
    "model_info": {
      "is_trained": true,
      "model_type": "Naive Bayes with TF-IDF",
      "vectorizer": "TF-IDF (max_features=5000, ngram_range=(1,2))",
      "classifier": "Multinomial Naive Bayes",
      "sentiment_classes": ["negative", "positive", "neutral"]
    }
  }
}
```

**Error Responses:**
- 401: Missing or invalid token
- 403: Insufficient permissions (not admin)
- 500: Internal server error

---

#### 8. List All Users
**GET** `/admin/users`

List all registered users (admin only).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "count": 2,
  "data": [
    {
      "username": "admin@university.edu",
      "name": "Administrator",
      "role": "admin",
      "permissions": ["read", "write", "delete", "manage_users"]
    },
    {
      "username": "student@university.edu",
      "name": "Student User",
      "role": "student",
      "permissions": ["read", "write"]
    }
  ]
}
```

**Error Responses:**
- 401: Missing or invalid token
- 403: Insufficient permissions (not admin)
- 500: Internal server error

---

### System Endpoints

#### 9. Health Check
**GET** `/health`

Check application health status.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000000",
  "version": "1.0.0"
}
```

---

#### 10. Root Endpoint
**GET** `/`

Get API information and available endpoints.

**Response (200 OK):**
```json
{
  "name": "Sentiment Analysis MLOps System",
  "version": "1.0.0",
  "description": "RESTful API for sentiment analysis with cloud-native deployment",
  "endpoints": {
    "health": "/health",
    "analyze": "/api/v1/analyze",
    "batch": "/api/v1/batch",
    "auth": "/api/v1/auth/login"
  }
}
```

---

## Error Handling

### Standard Error Response Format
```json
{
  "error": "Error type",
  "message": "Detailed error message"
}
```

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Internal Server Error |

---

## Rate Limiting

Currently no rate limiting is implemented. Future versions will include:
- Per-user rate limits
- IP-based throttling
- Burst allowances

---

## Pagination

Batch endpoints support pagination for large result sets:

```json
{
  "success": true,
  "count": 100,
  "page": 1,
  "total_pages": 5,
  "data": [...]
}
```

---

## Examples

### Example 1: Complete Authentication Flow

**Step 1: Login**
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student@university.edu",
    "password": "student123"
  }'
```

**Step 2: Analyze Sentiment**
```bash
curl -X POST http://localhost:5000/api/v1/analyze \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This API is fantastic!"
  }'
```

**Step 3: Refresh Token**
```bash
curl -X POST http://localhost:5000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "<refresh_token>"
  }'
```

### Example 2: Batch Processing

```bash
curl -X POST http://localhost:5000/api/v1/batch \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "texts": [
      "Excellent service!",
      "Very disappointed.",
      "Average experience."
    ]
  }'
```

### Example 3: Python Client

```python
import requests

# Login
response = requests.post(
    'http://localhost:5000/api/v1/auth/login',
    json={
        'username': 'student@university.edu',
        'password': 'student123'
    }
)
token = response.json()['access_token']

# Analyze sentiment
headers = {'Authorization': f'Bearer {token}'}
response = requests.post(
    'http://localhost:5000/api/v1/analyze',
    json={'text': 'This is amazing!'},
    headers=headers
)
result = response.json()
print(f"Sentiment: {result['data']['sentiment']}")
print(f"Confidence: {result['data']['confidence']}")
```

---

## API Versioning

Current API version: **v1**

Future versions will be available at:
- `/api/v2/...`
- `/api/v3/...`

Backward compatibility is maintained for at least 2 major versions.

---

## Support

For API issues or questions:
1. Check this documentation
2. Review example requests
3. Check application logs
4. Contact development team

---

**Last Updated**: January 2024  
**API Version**: 1.0.0
