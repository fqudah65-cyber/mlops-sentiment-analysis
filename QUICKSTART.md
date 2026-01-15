# Quick Start Guide

## Installation & Setup (5 minutes)

### 1. Install Python Dependencies
```bash
pip install -r backend/requirements.txt
```

### 2. Run the Application
```bash
cd backend/src
python app.py
```

The API will be available at `http://localhost:5000`

### 3. Verify Installation
```bash
curl http://localhost:5000/health
```

You should see:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

## Testing the API (10 minutes)

### 1. Login
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student@university.edu",
    "password": "student123"
  }'
```

Save the `access_token` from the response.

### 2. Analyze Sentiment
```bash
curl -X POST http://localhost:5000/api/v1/analyze \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This product is amazing!"
  }'
```

### 3. Batch Analysis
```bash
curl -X POST http://localhost:5000/api/v1/batch \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "texts": [
      "Great product!",
      "Terrible experience.",
      "It is okay."
    ]
  }'
```

## Running Tests (5 minutes)

### Run All Tests
```bash
pytest backend/tests/ -v
```

### Run with Coverage
```bash
pytest backend/tests/ -v --cov=backend/src --cov-report=html
```

## Docker Deployment (10 minutes)

### Build Docker Image
```bash
docker build -f docker/Dockerfile -t sentiment-api:latest .
```

### Run Container
```bash
docker run -p 5000:5000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-secret-key \
  sentiment-api:latest
```

## Test Credentials

**Admin Account:**
- Username: `admin@university.edu`
- Password: `admin123`

**Student Account:**
- Username: `student@university.edu`
- Password: `student123`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/login` | User login |
| POST | `/api/v1/analyze` | Analyze single text |
| POST | `/api/v1/batch` | Analyze multiple texts |
| GET | `/api/v1/model/info` | Get model information |
| GET | `/health` | Health check |

## Documentation

- **README.md** - Full project overview
- **docs/API_DOCUMENTATION.md** - Complete API reference
- **docs/DEPLOYMENT_GUIDE.md** - Deployment instructions
- **docs/ARCHITECTURE.md** - System architecture
- **AI381_Final_Project_Report.md** - Project report

## Troubleshooting

**Port already in use:**
```bash
docker run -p 8000:5000 sentiment-api:latest
```

**Import errors:**
```bash
pip install --upgrade -r backend/requirements.txt
```

**Test failures:**
```bash
cd backend
pytest tests/ -v --tb=short
```

## Next Steps

1. Review the API documentation
2. Explore the code structure
3. Run the tests
4. Deploy to Docker
5. Check the CI/CD pipeline on GitHub

For more information, see the complete documentation in the `docs/` directory.
