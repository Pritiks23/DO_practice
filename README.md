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

app.yaml-> defining how the backend service is dep;poyed scaled and monitored, source control integration, build and run commands, environmental variables, runtime environment, health checks. Operationalizes the API turnis codebase into a running monitored publicly accessible production service.
ci.yaml-> CI/CD pipeline inside GIthub ACtions, defensive engineering workflow preventing broken code, style drift, failing tests, import errors, container misconfigurations and known security vulnerabilities from reaching production. Ensures every deployment is technically validated before being released.
src/directory-> contains all application source code separates business logic and application modules from infrastructure, configuration, tests, CI files.
src/_init__.py-> turns src directory into an importable module
app.py-> Archietcturally it is responsible for assembling all application components- configuration, middleware, routing and error handling into a fully configured FastAPI runtime instance. I used def create_app() factory function instead of global app=FastAPI() so I can enable test isolation, each test can create a fresh app, support multiple environments(dev,stage,prod).
src/Config.py-> manages all the settings the app needs like which prot to urn on, API version logging which websites are allowed to talk to it(CORS). Instead of hardcoding these values, it loads them from the environment variables, this separation makes the app easier to run in different environments(prod,dev,locally)
src/data_routes.py-> defines API endpoints that let clients read, update, process and delete data records. All request validation, routing and error handling happens here while the actual data operations are delegated to data_service.py.
src/data_service.py-> acts as a centralized brain that manages all operations, architecturally its designed to be the layer that talks to whatever storage we choose keeping the API code decoupled from the database.
src/exceptions.py-> defined custom error classes like AppError so the application can raise and handle errors with consistent HTTP status codes and messages.
src/health-routes.py > provides the endpoints that let external systems check whether the API is running /health and /ready to serve requests giving uptime status and version info to monitor service health.
src/logger.py-> centralized logging system for app color coded (based if its debug, info, warnings, errors, critical)
src/main.py-> the file that starts the FastAPI server. Architecturally it handles graceful startup and shutdown, sets up signal handlers, logs startup info and runs the app using Uvicorn(bridge between ocde app.py and outside world)
src/middleware.py-> app's watchtower and safety net sits between incoming requests and routes to log every request with details and how log ut took and catch and standardize errors whether its a known AppError, a ValueError or unexpected exection client gets a consistent JSON response and the error is logged for monitoring. 
src/types.py-> where all "shapes" of the data is defined, what a data record could look like and what the health check response looks like so app always knows what kind of data to expect and return so everything is more consistent and less error prone.
Dockerfile-> recipe for building a container that can run the app, installs python and dependencies in a "buildinder" stage and copies app code into a production image, telling Docker how to start the app.
.env environment-> provides a template for environment variables for the app, showing what settings needs to be configured without containing real secrets
docker-compose.yaml-> defines how to run the app as a cotainer specifying build inscturoons, ports, environmental variables so it can be easily started with a single command
tests/conftest.py-> creates a test version of the app and a fake browser client to check if the API workstests/test_data.py-> uses automates testing framework called pytest that runs all test by itself each function sends request to your API and assets the response matches what's expected if it doesn't pytest automatically reports it as a failure
tests/test_health-> automatically checks the app /health and /ready endpoints to make sure they return these checks on its own and reports "pass" or "fail" without any manual testing. 





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
