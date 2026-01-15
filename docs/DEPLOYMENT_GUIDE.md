# Deployment Guide

Comprehensive guide for deploying the Sentiment Analysis MLOps System to production environments.

## Table of Contents

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [CI/CD Pipeline](#cicd-pipeline)
5. [Monitoring & Maintenance](#monitoring--maintenance)
6. [Troubleshooting](#troubleshooting)

## Local Development

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Virtual environment tool (venv)
- Git

### Setup Steps

1. **Clone Repository**
```bash
git clone <repository-url>
cd ai381_mlops_project
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r backend/requirements.txt
```

4. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Run Application**
```bash
cd backend/src
python app.py
```

6. **Verify Installation**
```bash
curl http://localhost:5000/health
```

### Development Workflow

```bash
# Run tests
pytest backend/tests/ -v

# Run with debug mode
FLASK_ENV=development python app.py

# Generate coverage report
pytest backend/tests/ --cov=backend/src --cov-report=html
```

---

## Docker Deployment

### Building Docker Image

1. **Build Image**
```bash
docker build -f docker/Dockerfile -t sentiment-api:latest .
```

2. **Verify Image**
```bash
docker images | grep sentiment-api
```

### Running Container

1. **Basic Run**
```bash
docker run -p 5000:5000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-secret-key \
  sentiment-api:latest
```

2. **Run with Environment File**
```bash
docker run -p 5000:5000 \
  --env-file .env.production \
  sentiment-api:latest
```

3. **Run with Volume Mounting**
```bash
docker run -p 5000:5000 \
  -v $(pwd)/models:/app/models \
  -e FLASK_ENV=production \
  sentiment-api:latest
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  sentiment-api:
    build:
      context: .
      dockerfile: docker/Dockerfile
    ports:
      - "5000:5000"
    environment:
      FLASK_ENV: production
      SECRET_KEY: ${SECRET_KEY}
      JWT_SECRET_KEY: ${JWT_SECRET_KEY}
    volumes:
      - ./models:/app/models
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 5s
    restart: unless-stopped
```

Run with Docker Compose:
```bash
docker-compose up -d
```

### Container Management

```bash
# View logs
docker logs sentiment-api

# Execute command in container
docker exec sentiment-api python -m pytest

# Stop container
docker stop sentiment-api

# Remove container
docker rm sentiment-api

# View container stats
docker stats sentiment-api
```

---

## Cloud Deployment

### Azure Container Instances

1. **Push to Azure Container Registry**
```bash
# Login to ACR
az acr login --name <registry-name>

# Tag image
docker tag sentiment-api:latest <registry>.azurecr.io/sentiment-api:latest

# Push image
docker push <registry>.azurecr.io/sentiment-api:latest
```

2. **Deploy Container Instance**
```bash
az container create \
  --resource-group myResourceGroup \
  --name sentiment-api \
  --image <registry>.azurecr.io/sentiment-api:latest \
  --cpu 1 \
  --memory 1 \
  --registry-login-server <registry>.azurecr.io \
  --registry-username <username> \
  --registry-password <password> \
  --ports 5000 \
  --protocol TCP \
  --environment-variables \
    FLASK_ENV=production \
    SECRET_KEY=<secret-key> \
  --restart-policy OnFailure
```

3. **Verify Deployment**
```bash
az container show \
  --resource-group myResourceGroup \
  --name sentiment-api \
  --query ipAddress.fqdn
```

### Azure App Service

1. **Create App Service Plan**
```bash
az appservice plan create \
  --name myAppServicePlan \
  --resource-group myResourceGroup \
  --sku B1 \
  --is-linux
```

2. **Create Web App**
```bash
az webapp create \
  --resource-group myResourceGroup \
  --plan myAppServicePlan \
  --name sentiment-api \
  --deployment-container-image-name-user <username> \
  --deployment-container-image-name <registry>.azurecr.io/sentiment-api:latest
```

3. **Configure Settings**
```bash
az webapp config appsettings set \
  --resource-group myResourceGroup \
  --name sentiment-api \
  --settings \
    FLASK_ENV=production \
    SECRET_KEY=<secret-key> \
    WEBSITES_PORT=5000
```

### AWS Elastic Container Service (ECS)

1. **Create ECR Repository**
```bash
aws ecr create-repository --repository-name sentiment-api
```

2. **Push Image**
```bash
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com

docker tag sentiment-api:latest <account>.dkr.ecr.us-east-1.amazonaws.com/sentiment-api:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/sentiment-api:latest
```

3. **Create ECS Task Definition**
```json
{
  "family": "sentiment-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "sentiment-api",
      "image": "<account>.dkr.ecr.us-east-1.amazonaws.com/sentiment-api:latest",
      "portMappings": [
        {
          "containerPort": 5000,
          "hostPort": 5000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "FLASK_ENV",
          "value": "production"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/sentiment-api",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

4. **Create ECS Service**
```bash
aws ecs create-service \
  --cluster sentiment-cluster \
  --service-name sentiment-api \
  --task-definition sentiment-api \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

### Kubernetes Deployment

1. **Create Deployment**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sentiment-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: sentiment-api
  template:
    metadata:
      labels:
        app: sentiment-api
    spec:
      containers:
      - name: sentiment-api
        image: sentiment-api:latest
        ports:
        - containerPort: 5000
        env:
        - name: FLASK_ENV
          value: "production"
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: secret-key
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 10
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

2. **Create Service**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: sentiment-api-service
spec:
  selector:
    app: sentiment-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
  type: LoadBalancer
```

3. **Deploy to Kubernetes**
```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl get pods
kubectl get svc
```

---

## CI/CD Pipeline

### GitHub Actions Workflow

The project includes automated CI/CD through GitHub Actions (`.github/workflows/ci-cd.yml`):

**Stages:**
1. **Testing**: Run unit and integration tests
2. **Linting**: Code quality checks
3. **Building**: Docker image creation
4. **Security**: Vulnerability scanning

### Manual Deployment

1. **Trigger Workflow**
```bash
git push origin main
```

2. **Monitor Pipeline**
- View progress on GitHub Actions tab
- Check build logs for errors
- Verify test results

3. **Verify Deployment**
```bash
curl https://your-deployed-api.com/health
```

---

## Monitoring & Maintenance

### Health Monitoring

1. **Health Check Endpoint**
```bash
curl http://localhost:5000/health
```

2. **Application Logs**
```bash
# Docker logs
docker logs sentiment-api

# Kubernetes logs
kubectl logs -f deployment/sentiment-api

# Azure logs
az container logs --resource-group myResourceGroup --name sentiment-api
```

### Performance Monitoring

1. **Response Time Tracking**
```python
import time
from flask import request

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def log_response(response):
    elapsed = time.time() - request.start_time
    print(f"Request took {elapsed}s")
    return response
```

2. **Resource Monitoring**
```bash
# Docker stats
docker stats sentiment-api

# Kubernetes metrics
kubectl top pods
kubectl top nodes
```

### Backup & Recovery

1. **Database Backup** (if using database)
```bash
docker exec sentiment-api pg_dump -U user dbname > backup.sql
```

2. **Model Backup**
```bash
docker cp sentiment-api:/app/models ./backup/models
```

3. **Recovery**
```bash
docker cp ./backup/models sentiment-api:/app/models
```

### Updates & Patches

1. **Update Dependencies**
```bash
pip install --upgrade -r backend/requirements.txt
```

2. **Rebuild Docker Image**
```bash
docker build -f docker/Dockerfile -t sentiment-api:v1.1.0 .
```

3. **Rolling Update (Kubernetes)**
```bash
kubectl set image deployment/sentiment-api \
  sentiment-api=sentiment-api:v1.1.0 \
  --record
```

---

## Troubleshooting

### Common Issues

**Issue: Port Already in Use**
```bash
# Find process using port
lsof -i :5000

# Kill process
kill -9 <PID>

# Or use different port
docker run -p 8000:5000 sentiment-api:latest
```

**Issue: Authentication Failures**
```bash
# Check token expiration
jwt.decode(token, options={"verify_signature": False})

# Refresh token
curl -X POST http://localhost:5000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "<token>"}'
```

**Issue: Model Loading Error**
```bash
# Verify model file
ls -la models/sentiment_model.pkl

# Check permissions
chmod 644 models/sentiment_model.pkl

# Retrain model
python backend/src/models/sentiment_model.py
```

**Issue: High Memory Usage**
```bash
# Check container memory
docker stats sentiment-api

# Increase memory limit
docker run -m 2g sentiment-api:latest

# Optimize model
# Consider using model quantization or pruning
```

**Issue: Slow Response Times**
```bash
# Check application logs
docker logs sentiment-api

# Monitor resource usage
docker stats sentiment-api

# Check network connectivity
curl -v http://localhost:5000/health

# Consider caching or load balancing
```

### Debug Mode

Enable debug logging:
```bash
FLASK_ENV=development LOG_LEVEL=DEBUG python app.py
```

### Performance Profiling

```python
from flask_profiler import Profiler

profiler = Profiler()
profiler.init_app(app)

# Access profiling results at /flask-profiler/
```

---

## Security Checklist

- [ ] Change default credentials
- [ ] Set strong SECRET_KEY
- [ ] Enable HTTPS in production
- [ ] Configure firewall rules
- [ ] Set up rate limiting
- [ ] Enable logging and monitoring
- [ ] Regular security updates
- [ ] Backup sensitive data
- [ ] Test disaster recovery
- [ ] Document access procedures

---

## Performance Optimization

1. **Caching**
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'redis'})

@app.route('/api/v1/model/info')
@cache.cached(timeout=3600)
def get_model_info():
    ...
```

2. **Load Balancing**
```bash
# Using Nginx
upstream sentiment_api {
    server localhost:5000;
    server localhost:5001;
    server localhost:5002;
}
```

3. **Database Optimization**
```python
# Add indexes
db.Index('idx_user_id', User.id)

# Use connection pooling
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True,
}
```

---

## Rollback Procedures

### Docker Rollback
```bash
# Tag previous version
docker tag sentiment-api:v1.0.0 sentiment-api:latest

# Run previous version
docker run -p 5000:5000 sentiment-api:v1.0.0
```

### Kubernetes Rollback
```bash
# View rollout history
kubectl rollout history deployment/sentiment-api

# Rollback to previous version
kubectl rollout undo deployment/sentiment-api

# Rollback to specific revision
kubectl rollout undo deployment/sentiment-api --to-revision=2
```

---

**Last Updated**: January 2024  
**Version**: 1.0.0
