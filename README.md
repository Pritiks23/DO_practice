# DO_practice

Production-ready REST API service for data ingestion and processing, built with Python, FastAPI, and modern best practices.

## Features

- ✅ **RESTful API** - Clean, well-structured API endpoints for data management
- ✅ **Data Ingestion** - Accepts and stores data with metadata
- ✅ **Data Processing** - Process ingested data with tracking
- ✅ **Python** - Full type hints and excellent IDE support with FastAPI
- ✅ **Testing** - Comprehensive test suite with pytest (unit + integration tests)
- ✅ **Validation** - Request validation with Pydantic models
- ✅ **Error Handling** - Centralized error handling with proper HTTP status codes
- ✅ **Logging** - Structured logging with custom formatters
- ✅ **Security** - CORS support and security best practices
- ✅ **Docker** - Production-ready Docker image
- ✅ **CI/CD** - Automated testing, linting, and building with GitHub Actions
- ✅ **Health Checks** - Built-in health and readiness endpoints
- ✅ **Graceful Shutdown** - Proper cleanup on termination signals
- ✅ **API Documentation** - Automatic interactive API docs with Swagger UI

## Tech Stack

- **Runtime**: Python 3.11+
- **Language**: Python with type hints
- **Framework**: FastAPI
- **Testing**: pytest + httpx
- **Logging**: Python logging with custom formatters
- **Linting**: Black + Flake8 + MyPy
- **Validation**: Pydantic
- **Container**: Docker

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Docker (optional, for containerization)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Pritiks23/DO_practice.git
cd DO_practice
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create environment file:
```bash
cp .env.example .env
```

5. Configure environment variables in `.env`:
```env
PORT=3000
NODE_ENV=development
API_VERSION=v1
API_PREFIX=/api
LOG_LEVEL=INFO
CORS_ORIGIN=*
```

## Development

### Run in development mode
```bash
python -m src.main
```

The application will start with auto-reload enabled in development mode.

### Run with uvicorn directly
```bash
uvicorn src.main:app --reload --port 3000
```

### Run tests
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_health.py

# Run with verbose output
pytest -v
```

### Code quality
```bash
# Format code with Black
black src tests

# Check code style with Flake8
flake8 src tests

# Type check with MyPy
mypy src

# Run all quality checks
black src tests && flake8 src tests && mypy src
```

## API Documentation

Base URL: `http://localhost:3000/api/v1`

### Interactive API Documentation

- **Swagger UI**: `http://localhost:3000/api/v1/docs`
- **ReDoc**: `http://localhost:3000/api/v1/redoc`

### Health Endpoints

#### GET /health
Check application health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-02-21T19:00:00.000Z",
  "uptime": 123.45,
  "version": "1.0.0"
}
```

#### GET /ready
Check if the application is ready to serve requests.

**Response:**
```json
{
  "status": "ready",
  "timestamp": "2024-02-21T19:00:00.000Z"
}
```

### Data Endpoints

#### POST /data
Ingest new data.

**Request Body:**
```json
{
  "data": {
    "sensor": "temperature",
    "value": 25.5,
    "unit": "celsius"
  },
  "metadata": {
    "source": "sensor-001",
    "version": "1.0"
  }
}
```

**Response (201):**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "timestamp": "2024-02-21T19:00:00.000Z",
    "data": {
      "sensor": "temperature",
      "value": 25.5,
      "unit": "celsius"
    },
    "processed": false,
    "metadata": {
      "source": "sensor-001",
      "version": "1.0"
    }
  }
}
```

#### GET /data
Retrieve all data records (with pagination).

**Query Parameters:**
- `limit` (optional, default: 100) - Number of records to return
- `offset` (optional, default: 0) - Number of records to skip

**Response (200):**
```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "limit": 100,
    "offset": 0,
    "total": 150
  },
  "stats": {
    "total": 150,
    "processed": 75,
    "unprocessed": 75
  }
}
```

#### GET /data/:id
Retrieve a specific data record.

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    ...
  }
}
```

**Response (404):**
```json
{
  "error": {
    "message": "Record with id ... not found",
    "statusCode": 404
  }
}
```

#### POST /data/:id/process
Process a data record.

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "processed": true,
    "processingTimestamp": "2024-02-21T19:01:00.000Z",
    "processingResult": {
      "status": "success",
      "message": "Data processed successfully"
    },
    ...
  }
}
```

#### DELETE /data/:id
Delete a data record.

**Response (200):**
```json
{
  "success": true,
  "message": "Record with id ... deleted successfully"
}
```

## Docker

### Build the Docker image
```bash
docker build -t do-practice:latest .
```

### Run the container
```bash
docker run -p 3000:3000 -e PORT=3000 do-practice:latest
```

### Using Docker Compose
```bash
docker-compose up
```

## Deployment

### Prerequisites
- DigitalOcean account
- DigitalOcean CLI (doctl) installed
- Docker registry access

### Deploy to DigitalOcean App Platform

1. **Push your code to GitHub** (already done)

2. **Create app via DigitalOcean CLI:**
```bash
doctl apps create --spec .do/app.yaml
```

3. **Or deploy via DigitalOcean Console:**
   - Go to Apps in DigitalOcean console
   - Click "Create App"
   - Connect your GitHub repository
   - Configure build and run commands:
     - Build Command: `pip install -r requirements.txt`
     - Run Command: `python -m src.main`
   - Set environment variables
   - Deploy!

### Environment Variables for Production

Ensure these are set in your deployment environment:
- `PORT` - Port to run the server (default: 3000)
- `NODE_ENV` - Set to "production"
- `API_VERSION` - API version (default: v1)
- `LOG_LEVEL` - Logging level (INFO, WARNING, ERROR)
- `CORS_ORIGIN` - CORS allowed origins

## CI/CD

The project includes a GitHub Actions workflow that:

- ✅ Lints code with Flake8
- ✅ Checks code formatting with Black
- ✅ Type-checks with MyPy
- ✅ Runs test suite with coverage
- ✅ Builds the application
- ✅ Builds Docker image
- ✅ Runs security checks

The workflow runs on:
- Push to `main`, `develop`, or `copilot/**` branches
- Pull requests to `main` or `develop`

## Project Structure

```
.
├── src/
│   ├── __init__.py         # Package initialization
│   ├── main.py             # Entry point
│   ├── app.py              # FastAPI app setup
│   ├── config.py           # Configuration
│   ├── types.py            # Pydantic models
│   ├── data_service.py     # Business logic
│   ├── data_routes.py      # Data endpoints
│   ├── health_routes.py    # Health endpoints
│   ├── middleware.py       # Middleware
│   ├── exceptions.py       # Custom exceptions
│   └── logger.py           # Logging utility
├── tests/                  # Test files
│   ├── conftest.py         # Test configuration
│   ├── test_health.py      # Health tests
│   └── test_data.py        # Data tests
├── .github/
│   └── workflows/          # GitHub Actions
├── Dockerfile              # Docker configuration
├── .dockerignore           # Docker ignore file
├── .gitignore              # Git ignore file
├── .env.example            # Example environment variables
├── requirements.txt        # Python dependencies
├── pytest.ini              # pytest configuration
├── pyproject.toml          # Python project config
├── .flake8                 # Flake8 configuration
└── README.md               # This file
```

## Code Quality

### Test Coverage
The project maintains high test coverage (70%+ threshold) across:
- Branches
- Functions
- Lines
- Statements

Current coverage: **85%+**

### Code Style
- Python type hints for better IDE support
- Black for code formatting
- Flake8 for code quality
- MyPy for type checking
- Pydantic for data validation

### Security
- CORS configuration
- Input validation on all endpoints
- Error handling without exposing internals
- Non-root Docker user
- Regular dependency audits

## Operational Excellence

### Logging
Structured logging with custom formatters:
- Request/response logging
- Error logging with stack traces
- Colored console output for development

### Monitoring
- Health check endpoint for liveness probes
- Readiness endpoint for readiness probes
- Graceful shutdown handling

### Scalability
- Stateless design (in-memory store is for demo; replace with database for production)
- Docker containerization for easy scaling
- Async/await support with FastAPI
- Resource-efficient Python runtime

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

ISC

## Contact

For questions or support, please open an issue in the repository.
