# System Architecture

Comprehensive documentation of the Sentiment Analysis MLOps System architecture.

## Architecture Overview

The system follows a modern cloud-native, microservices-inspired architecture with clear separation of concerns.

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Applications                       │
│                    (Web, Mobile, CLI Tools)                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │   Load Balancer │
                    │   (Optional)    │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
   ┌────▼────┐         ┌────▼────┐         ┌────▼────┐
   │ Instance │         │ Instance │         │ Instance │
   │    1     │         │    2     │         │    N     │
   └────┬────┘         └────┬────┘         └────┬────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
        ┌────────────────────▼────────────────────┐
        │      API Gateway / Reverse Proxy        │
        │         (Nginx / Azure Gateway)         │
        └────────────────────┬────────────────────┘
                             │
        ┌────────────────────▼────────────────────┐
        │     Flask Web Application (REST API)    │
        │                                         │
        │  ┌─────────────────────────────────┐  │
        │  │   Authentication & Authorization │  │
        │  │    (JWT + Azure AD + RBAC)      │  │
        │  └─────────────────────────────────┘  │
        │                                         │
        │  ┌─────────────────────────────────┐  │
        │  │      API Routes & Handlers      │  │
        │  │  - /auth/* (Authentication)    │  │
        │  │  - /analyze (Sentiment Analysis)│  │
        │  │  - /batch (Batch Processing)   │  │
        │  │  - /admin/* (Admin Functions)  │  │
        │  └─────────────────────────────────┘  │
        │                                         │
        │  ┌─────────────────────────────────┐  │
        │  │   Business Logic Services       │  │
        │  │  - SentimentAnalyzer            │  │
        │  │  - AuthService                  │  │
        │  │  - ValidationService            │  │
        │  └─────────────────────────────────┘  │
        │                                         │
        │  ┌─────────────────────────────────┐  │
        │  │    Machine Learning Models      │  │
        │  │  - Naive Bayes Classifier      │  │
        │  │  - TF-IDF Vectorizer            │  │
        │  └─────────────────────────────────┘  │
        └────────────────────┬────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
   ┌────▼────┐         ┌────▼────┐         ┌────▼────┐
   │  Cache  │         │ Database │         │  Logs   │
   │ (Redis) │         │ (Optional)│        │ (ELK)   │
   └─────────┘         └──────────┘         └─────────┘
```

## Component Architecture

### 1. Client Layer

**Responsibilities:**
- User interface and interaction
- Request formation and submission
- Response handling and display

**Technologies:**
- Web browsers (JavaScript/React)
- Mobile applications (iOS/Android)
- CLI tools (Python/curl)
- Third-party integrations

---

### 2. API Gateway Layer

**Responsibilities:**
- Request routing
- Load balancing
- Rate limiting
- SSL/TLS termination
- Request/response logging

**Technologies:**
- Nginx (self-hosted)
- Azure API Management
- AWS API Gateway
- CloudFlare

**Features:**
- Health checks
- Circuit breaking
- Request transformation
- CORS handling

---

### 3. Application Layer

#### 3.1 Flask Web Framework

**Core Application** (`app.py`)
- Application factory pattern
- Blueprint registration
- Error handling
- Middleware configuration

**Key Features:**
- RESTful API design
- Automatic request/response serialization
- Built-in error handling
- CORS support

#### 3.2 API Routes (`api/routes.py`)

**Endpoint Categories:**

**Authentication Endpoints:**
- `POST /auth/login` - User authentication
- `POST /auth/refresh` - Token refresh
- `GET /auth/user` - User information

**Analysis Endpoints:**
- `POST /analyze` - Single text analysis
- `POST /batch` - Batch text analysis
- `GET /model/info` - Model information

**Admin Endpoints:**
- `GET /admin/stats` - System statistics
- `GET /admin/users` - User management

**System Endpoints:**
- `GET /health` - Health check
- `GET /` - API information

#### 3.3 Authentication Service (`services/auth_service.py`)

**Responsibilities:**
- User authentication
- JWT token generation and validation
- Role-based access control (RBAC)
- Permission management

**Security Features:**
- Password hashing (SHA-256)
- Token expiration
- Refresh token rotation
- Azure AD integration support

**Roles:**
- **Admin**: Full system access
- **Student**: Read and write access
- **Viewer**: Read-only access

---

### 4. Business Logic Layer

#### 4.1 Sentiment Analysis Model (`models/sentiment_model.py`)

**Architecture:**
```
Input Text
    │
    ▼
┌──────────────────┐
│  TF-IDF Vector   │
│   Vectorizer     │
│ (max_features=   │
│  5000, ngram=    │
│  (1,2))          │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Multinomial     │
│  Naive Bayes     │
│  Classifier      │
└────────┬─────────┘
         │
         ▼
   Prediction
  (sentiment +
   confidence)
```

**Model Specifications:**
- **Algorithm**: Multinomial Naive Bayes
- **Vectorization**: TF-IDF (Term Frequency-Inverse Document Frequency)
- **Features**: 5000 maximum features
- **N-grams**: Unigrams and bigrams
- **Classes**: Positive, Negative, Neutral

**Model Performance:**
- **Accuracy**: ~85%
- **Inference Time**: <50ms per sample
- **Memory Footprint**: ~20MB

**Capabilities:**
- Single text prediction
- Batch prediction (up to 100 texts)
- Confidence scoring
- Detailed probability distribution

#### 4.2 Validation Service (`utils/validators.py`)

**Input Validation:**
- Email format validation
- Text length validation (1-5000 characters)
- Type checking
- Sanitization

**Error Handling:**
- Comprehensive error messages
- Input constraint enforcement
- Security validation

---

### 5. Data Layer

#### 5.1 Model Storage

**Current Implementation:**
- In-memory model (trained on startup)
- Pickle serialization for persistence

**Future Enhancement:**
- Database storage for model versioning
- Model registry (MLflow)
- A/B testing framework

#### 5.2 Caching (Optional)

**Technologies:**
- Redis for session caching
- In-memory caching for model predictions
- HTTP caching headers

**Benefits:**
- Reduced latency
- Lower database load
- Improved scalability

#### 5.3 Logging & Monitoring

**Logging Stack:**
- Application logs (Python logging)
- Request/response logging
- Error tracking
- Performance metrics

**Monitoring Tools:**
- Application Performance Monitoring (APM)
- Error tracking (Sentry)
- Log aggregation (ELK Stack)
- Metrics collection (Prometheus)

---

## Deployment Architecture

### Development Environment

```
Developer Machine
├── Python Virtual Environment
├── Flask Development Server (port 5000)
├── Local Database (SQLite)
└── Local Model Files
```

### Production Environment

```
Cloud Provider (Azure/AWS)
├── Container Registry
│   └── Docker Image (sentiment-api:latest)
├── Container Orchestration
│   ├── Azure Container Instances / ECS
│   ├── Kubernetes Cluster (optional)
│   └── Load Balancer
├── Managed Services
│   ├── Azure Functions / AWS Lambda
│   ├── Managed Database
│   └── Managed Cache (Redis)
└── Monitoring & Logging
    ├── Application Insights
    ├── CloudWatch / Log Analytics
    └── Alerts & Dashboards
```

---

## Data Flow

### 1. Authentication Flow

```
User Request (username, password)
    │
    ▼
┌─────────────────────────┐
│ AuthService.login()     │
│ - Verify credentials    │
│ - Hash password check   │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Generate JWT Tokens     │
│ - Access Token (1h)     │
│ - Refresh Token (30d)   │
└────────┬────────────────┘
         │
         ▼
Return Tokens + User Info
```

### 2. Sentiment Analysis Flow

```
Client Request (text)
    │
    ▼
┌──────────────────────────┐
│ Verify JWT Token         │
│ Check Authorization      │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ Validate Input           │
│ - Check text length      │
│ - Sanitize input         │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ SentimentAnalyzer.       │
│ predict(text)            │
│ - Vectorize text         │
│ - Classify               │
│ - Calculate confidence   │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ Format Response          │
│ - Add metadata           │
│ - Add timestamp          │
└────────┬─────────────────┘
         │
         ▼
Return JSON Response
```

### 3. Batch Processing Flow

```
Client Request (texts array)
    │
    ▼
┌──────────────────────────┐
│ Verify Authentication    │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ Validate Array           │
│ - Check size (≤100)      │
│ - Validate each text     │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ For Each Text:           │
│ - Predict sentiment      │
│ - Store result           │
└────────┬─────────────────┘
         │
         ▼
Return Array of Results
```

---

## Security Architecture

### Authentication & Authorization

```
┌─────────────────────────────────────────┐
│         Request with JWT Token          │
└────────────────┬────────────────────────┘
                 │
                 ▼
        ┌────────────────────┐
        │ Verify JWT Signature│
        │ Check Expiration    │
        └────────┬───────────┘
                 │
         ┌───────┴────────┐
         │                │
    Valid           Invalid/Expired
         │                │
         ▼                ▼
    ┌────────┐      ┌──────────┐
    │ Extract │      │ Return   │
    │ Claims  │      │ 401 Error│
    └────┬───┘      └──────────┘
         │
         ▼
    ┌──────────────────┐
    │ Check User Role  │
    │ & Permissions    │
    └────────┬─────────┘
             │
      ┌──────┴──────┐
      │             │
  Authorized   Unauthorized
      │             │
      ▼             ▼
  Process      Return 403
  Request      Forbidden
```

### Data Protection

1. **In Transit:**
   - HTTPS/TLS encryption
   - JWT token signing
   - Secure headers

2. **At Rest:**
   - Environment variable secrets
   - Encrypted configuration
   - Secure credential storage

3. **Application Level:**
   - Input validation
   - SQL injection prevention
   - CSRF protection
   - Rate limiting

---

## Scalability Architecture

### Horizontal Scaling

```
┌──────────────────────────────────────┐
│         Load Balancer                │
└──────────────────┬───────────────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
    ▼              ▼              ▼
┌────────┐    ┌────────┐    ┌────────┐
│Instance│    │Instance│    │Instance│
│   1    │    │   2    │    │   N    │
│ (5000) │    │ (5001) │    │ (500N) │
└────────┘    └────────┘    └────────┘
    │              │              │
    └──────────────┼──────────────┘
                   │
            ┌──────▼──────┐
            │ Shared Cache │
            │   (Redis)    │
            └──────────────┘
```

### Vertical Scaling

- Increase CPU cores
- Increase memory allocation
- Upgrade storage
- Optimize algorithms

### Database Scaling

- Connection pooling
- Read replicas
- Sharding (if needed)
- Caching layer

---

## Disaster Recovery

### Backup Strategy

1. **Model Backup**
   - Regular model snapshots
   - Version control
   - Multiple storage locations

2. **Configuration Backup**
   - Environment variables
   - Secrets management
   - Infrastructure as Code

3. **Data Backup**
   - Database backups
   - Log archival
   - Point-in-time recovery

### Recovery Procedures

1. **Application Failure:**
   - Automatic restart
   - Health check monitoring
   - Failover to standby

2. **Data Loss:**
   - Restore from backup
   - Verify data integrity
   - Gradual rollout

3. **Security Breach:**
   - Revoke compromised tokens
   - Rotate secrets
   - Audit logs review

---

## Performance Optimization

### Caching Strategy

```
Request
  │
  ├─ Check Cache
  │  ├─ Hit → Return Cached Response
  │  └─ Miss → Process Request
  │
  ├─ Process
  │  ├─ Authenticate
  │  ├─ Validate
  │  └─ Analyze
  │
  ├─ Cache Result
  │  └─ Store in Redis/Memory
  │
  └─ Return Response
```

### Database Optimization

- Connection pooling
- Query optimization
- Indexing strategy
- Query caching

### Model Optimization

- Model quantization
- Feature selection
- Batch prediction
- GPU acceleration (future)

---

## Monitoring & Observability

### Metrics Collection

```
Application
    │
    ├─ Request Count
    ├─ Response Time
    ├─ Error Rate
    ├─ CPU Usage
    ├─ Memory Usage
    └─ Model Predictions
         │
         ▼
    Prometheus
         │
         ▼
    Grafana Dashboard
```

### Logging Strategy

```
Application Logs
    │
    ├─ Info Logs
    ├─ Warning Logs
    ├─ Error Logs
    └─ Debug Logs
         │
         ▼
    Log Aggregation
    (ELK/Splunk)
         │
         ▼
    Analysis & Alerting
```

### Alerting

- High error rate (>5%)
- High latency (>500ms)
- Low availability (<99%)
- Resource exhaustion
- Security incidents

---

## Technology Decisions

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Framework | Flask | Lightweight, flexible, perfect for APIs |
| ML Model | scikit-learn | Fast, reliable, easy to deploy |
| Vectorization | TF-IDF | Efficient, interpretable, proven |
| Authentication | JWT | Stateless, scalable, industry standard |
| Containerization | Docker | Reproducible, portable, standard |
| Orchestration | Kubernetes | Scalable, resilient, industry standard |
| CI/CD | GitHub Actions | Integrated, free for public repos |
| Monitoring | Prometheus | Open-source, time-series, scalable |
| Logging | ELK Stack | Comprehensive, searchable, scalable |

---

## Future Architecture Enhancements

1. **Microservices:**
   - Separate authentication service
   - Dedicated model serving service
   - Independent scaling

2. **Advanced ML:**
   - Transformer models (BERT)
   - Multi-language support
   - Real-time model updates

3. **Streaming:**
   - Kafka integration
   - Real-time processing
   - Event-driven architecture

4. **Advanced Caching:**
   - Distributed caching
   - Cache invalidation strategies
   - Cache warming

5. **GraphQL:**
   - GraphQL API layer
   - Flexible querying
   - Better mobile support

---

**Version**: 1.0.0  
**Architecture Pattern**: Layered + Cloud-Native
