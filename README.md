# 🎓 IsCoolGPT

> An intelligent educational assistant powered by AI to help students across various academic disciplines.

[![Deploy Production](https://github.com/Yara-R/IsCoolGPT/actions/workflows/deploy-production.yml/badge.svg)](https://github.com/Yara-R/IsCoolGPT/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📋 About The Project

**IsCoolGPT** is a modern educational platform that uses artificial intelligence to provide personalized support to students. The system offers didactic explanations, practical examples, and assistance across various academic disciplines.

### ✨ Key Features

- 🤖 **AI Integration**: Powered by advanced language models
- 📚 **Multiple Disciplines**: Support for 10+ academic subjects
- 💬 **Contextual Conversations**: Maintains conversation history for more accurate responses
- 🎨 **Modern Interface**: Responsive and intuitive design
- 🐳 **Docker Ready**: Complete containerization with multi-stage builds
- 🔒 **Secure**: Non-root user, health checks, and security best practices
- ⚡ **High Performance**: FastAPI + Uvicorn with configurable workers
- 🚀 **Complete CI/CD**: Automated deployment to AWS ECS via GitHub Actions

---

## 🏗️ Architecture

```
┌─────────────────┐
│   Frontend      │
│   (Nginx)       │
└────────┬────────┘
         │
    HTTP │
         ▼
┌─────────────────┐      ┌──────────────────┐
│   Backend       │────▶ │    AI API        │
│   (FastAPI)     │      │  (LLM Service)   │
└─────────────────┘      └──────────────────┘
         │
         ▼
┌─────────────────┐
│   AWS ECS       │
│   (Production)  │
└─────────────────┘
```

### 🛠️ Tech Stack

**Backend:**
- Python 3.11
- FastAPI
- Uvicorn (ASGI server)
- AI SDK integration
- Pydantic (data validation)

**Frontend:**
- HTML5 + CSS3
- Vanilla JavaScript
- Nginx (reverse proxy)

**Infrastructure:**
- Docker + Docker Compose
- AWS ECR (container registry)
- AWS ECS (container orchestration)
- GitHub Actions (CI/CD)

---

## 📂 Project Structure

```
IsCoolGPT/
├── .github/
│   └── workflows/
│       ├── ci.yml                    # Continuous integration
│       ├── deploy-staging.yml        # Staging deployment
│       └── deploy-production.yml     # Production deployment
├── frontend/
│   └── index.html                    # Web interface
├── tests/
│   ├── conftest.py                   # Pytest fixtures
│   └── test_main.py                  # Unit tests
├── main.py                           # FastAPI backend
├── requirements.txt                  # Python dependencies
├── requirements-test.txt             # Test dependencies
├── Dockerfile                        # Multi-stage build
├── docker-compose.yml                # Local orchestration
├── nginx.conf                        # Nginx configuration
├── ecs-task-def.json                # Staging task definition
├── ecs-task-def-prod.json           # Production task definition
├── Makefile                          # Useful commands
├── .env.example                      # Configuration example
└── README.md                         # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- AI API Key (Anthropic)

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Yara-R/IsCoolGPT.git
cd IsCoolGPT
```

### 2️⃣ Configure Environment Variables

```bash
cp .env.example .env
```

Edit the `.env` file and add your API key:

```env
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ENVIRONMENT=development
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=2
```

### 3️⃣ Start with Docker Compose

```bash
# Build and start
docker-compose up -d --build

# Check logs
docker-compose logs -f

# Check status
docker-compose ps
```

### 4️⃣ Access the Application

- **Frontend**: http://localhost
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 🧪 Local Development (Without Docker)

### Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-test.txt
```

### Run Backend

```bash
export API_KEY=your_key  # Linux/Mac
# or
set API_KEY=your_key  # Windows

uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Run Frontend

Open `frontend/index.html` directly in browser or use a local server:

```bash
cd frontend
python -m http.server 8080
```

---

## 📚 API Reference

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-16T10:30:00"
}
```

### List Subjects
```http
GET /api/subjects
```

**Response:**
```json
{
  "subjects": [
    {
      "id": "Cloud Comp",
      "name": "Cloud Computing Fundamentals",
      "icon": "☁️"
    },
    {
      "id": "Math",
      "name": "Computational Mathematics",
      "icon": "🔢"
    }
  ]
}
```

### Chat with Assistant
```http
POST /api/chat
Content-Type: application/json
```

**Request:**
```json
{
  "subject": "Cloud Computing Fundamentals",
  "question": "Explain the concept of virtualization",
  "context": "I'm studying cloud infrastructure",
  "history": []
}
```

**Response:**
```json
{
  "answer": "Virtualization is the technology that allows creating multiple independent virtual environments on a single physical hardware...",
  "subject": "Cloud Computing Fundamentals",
  "timestamp": "2025-11-16T10:30:00"
}
```

---

## 🧪 Testing

The project has complete test coverage with pytest.

### Run Tests

```bash
# All tests
make test

# With coverage
make test-cov

# Unit tests only
make test-unit

# Integration tests only
make test-integration

# View HTML report
make coverage-report
open htmlcov/index.html
```

### Test Coverage

- ✅ Endpoints (health, subjects, chat)
- ✅ Pydantic models
- ✅ CORS
- ✅ Error handling
- ✅ Performance
- ✅ End-to-end integration

**Coverage target**: 80%+

---

## 🔄 CI/CD Pipeline

The project uses GitHub Actions for complete automation.

### Workflows

#### 1. **Continuous Integration** (`.github/workflows/ci.yml`)
- ✅ Tests on Python 3.9, 3.10, 3.11
- ✅ Linting (Flake8, Black, MyPy)
- ✅ Security scanning
- ✅ Coverage reports (Codecov)
- ✅ Docker build validation

#### 2. **Deploy Staging** (`.github/workflows/deploy-staging.yml`)
Trigger: push to `staging` branch
- Build Docker image
- Push to ECR: `iscoolgpt-staging`
- Deploy to ECS staging

#### 3. **Deploy Production** (`.github/workflows/deploy-production.yml`)
Trigger: push to `main` branch
- Build Docker image
- Push to ECR: `iscoolgpt`
- Deploy to ECS production

### Environments

| Environment | Branch | ECR Repository | ECS Cluster |
|-------------|--------|----------------|-------------|
| Staging | `staging` | `iscoolgpt-staging` | Configurable |
| Production | `main` | `iscoolgpt` | Configurable |

---

## 🐳 Docker

### Manual Build

```bash
# Build
docker build -t iscoolgpt:latest .

# Run
docker run -p 8000:8000 \
  -e API_KEY=your_key \
  iscoolgpt:latest
```

### Multi-stage Build

The Dockerfile uses multi-stage build for optimization:

1. **Base**: Base Python configuration
2. **Dependencies**: Dependency installation
3. **Runtime**: Minimal final image

**Benefits:**
- ✅ ~50% smaller final image
- ✅ Non-root user for security
- ✅ Integrated health checks
- ✅ Optimized build cache

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `ANTHROPIC_API_KEY` | AI API Key | - | ✅ |
| `ENVIRONMENT` | Environment (dev/prod/staging) | `production` | ❌ |
| `API_HOST` | API host | `0.0.0.0` | ❌ |
| `API_PORT` | API port | `8000` | ❌ |
| `API_WORKERS` | Uvicorn workers | `2` | ❌ |
| `LOG_LEVEL` | Log level | `info` | ❌ |

### AWS Secrets (GitHub Actions)

Configure in repository: **Settings → Secrets and variables → Actions**

**Production:**
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `ECR_REPOSITORY_PROD`
- `ECS_SERVICE_PROD`
- `ECS_CLUSTER_PROD`

**Staging:**
- `ECR_REPOSITORY_STAGING`
- `ECS_SERVICE_STAGING`
- `ECS_CLUSTER_STAGING`

---

## 📊 Supported Disciplines

The assistant provides support for the following disciplines:

- ☁️ Cloud Computing Fundamentals
- 🔢 Computational Mathematics
- 💻 Programming
- 🗄️ Databases
- 🌐 Computer Networks
- 🔐 Information Security
- 📊 Data Structures
- 🤖 Artificial Intelligence
- 🎨 Software Design
- 📈 Algorithm Analysis

---

## 🛠️ Useful Commands

The project includes a `Makefile` with useful commands:

```bash
# View all available commands
make help

# Complete checks (simulate CI locally)
make check

# Build and deploy locally
make docker-build
make docker-up
make docker-logs

# Tests
make test
make test-cov

# Code quality
make lint
make format

# Cleanup
make clean
```

---

## 🐛 Troubleshooting

### Problem: API doesn't connect to AI service

**Solution:**
```bash
# Check if API key is configured
docker-compose exec api printenv | grep ANTHROPIC

# Check logs
docker-compose logs api
```

### Problem: Frontend doesn't load

**Solution:**
```bash
# Check Nginx
docker-compose logs frontend

# Check if port 80 is available
sudo lsof -i :80

# Restart service
docker-compose restart frontend
```

### Problem: Build fails

**Solution:**
```bash
# Clean Docker cache
docker system prune -a

# Build without cache
docker-compose build --no-cache

# Check dependencies
pip install -r requirements.txt
```

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Guidelines

- Write tests for new features
- Maintain test coverage above 80%
- Follow the style guide (Black + Flake8)
- Update documentation

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Yara R** - [GitHub](https://github.com/Yara-R)

---

## 📞 Support

If you encounter any issues or have questions:

- 🐛 [Open an issue](https://github.com/Yara-R/IsCoolGPT/issues)
- 💬 [Discussions](https://github.com/Yara-R/IsCoolGPT/discussions)
- 📧 Contact via GitHub
