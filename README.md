# DO_practice

Production-ready REST API service for data ingestion and processing, built with TypeScript, Express, and modern best practices.

## Features

- ✅ **RESTful API** - Clean, well-structured API endpoints for data management
- ✅ **Data Ingestion** - Accepts and stores data with metadata
- ✅ **Data Processing** - Process ingested data with tracking
- ✅ **TypeScript** - Full type safety and excellent IDE support
- ✅ **Testing** - Comprehensive test suite with Jest (unit + integration tests)
- ✅ **Validation** - Request validation middleware
- ✅ **Error Handling** - Centralized error handling with proper HTTP status codes
- ✅ **Logging** - Structured logging with Winston
- ✅ **Security** - Helmet for security headers, CORS support
- ✅ **Docker** - Production-ready Docker image
- ✅ **CI/CD** - Automated testing, linting, and building with GitHub Actions
- ✅ **Health Checks** - Built-in health and readiness endpoints
- ✅ **Graceful Shutdown** - Proper cleanup on termination signals

## Tech Stack

- **Runtime**: Node.js 20
- **Language**: TypeScript
- **Framework**: Express.js
- **Testing**: Jest + Supertest
- **Logging**: Winston
- **Linting**: ESLint + Prettier
- **Security**: Helmet + CORS
- **Container**: Docker

## Prerequisites

- Node.js 20 or higher
- npm or yarn
- Docker (optional, for containerization)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Pritiks23/DO_practice.git
cd DO_practice
```

2. Install dependencies:
```bash
npm install
```

3. Create environment file:
```bash
cp .env.example .env
```

4. Configure environment variables in `.env`:
```env
PORT=3000
NODE_ENV=development
API_VERSION=v1
API_PREFIX=/api
LOG_LEVEL=info
CORS_ORIGIN=*
```

## Development

### Run in development mode
```bash
npm run dev
```

### Build the project
```bash
npm run build
```

### Run in production mode
```bash
npm start
```

### Run tests
```bash
# Run all tests
npm test

# Run tests with coverage
npm run test:coverage

# Run tests in watch mode
npm run test:watch
```

### Code quality
```bash
# Lint code
npm run lint

# Fix linting issues
npm run lint:fix

# Format code
npm run format

# Check formatting
npm run format:check

# Type check
npm run typecheck
```

## API Documentation

Base URL: `http://localhost:3000/api/v1`

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
     - Build Command: `npm ci && npm run build`
     - Run Command: `npm start`
   - Set environment variables
   - Deploy!

### Environment Variables for Production

Ensure these are set in your deployment environment:
- `PORT` - Port to run the server (default: 3000)
- `NODE_ENV` - Set to "production"
- `API_VERSION` - API version (default: v1)
- `LOG_LEVEL` - Logging level (info, warn, error)
- `CORS_ORIGIN` - CORS allowed origins

## CI/CD

The project includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that:

- ✅ Lints code with ESLint
- ✅ Checks code formatting with Prettier
- ✅ Type-checks with TypeScript compiler
- ✅ Runs test suite with coverage
- ✅ Builds the application
- ✅ Builds Docker image
- ✅ Runs security audit

The workflow runs on:
- Push to `main`, `develop`, or `copilot/**` branches
- Pull requests to `main` or `develop`

## Project Structure

```
.
├── src/
│   ├── __tests__/          # Test files
│   ├── config/             # Configuration
│   ├── controllers/        # Request handlers
│   ├── middleware/         # Express middleware
│   ├── routes/             # API routes
│   ├── services/           # Business logic
│   ├── types/              # TypeScript types
│   ├── utils/              # Utility functions
│   ├── app.ts              # Express app setup
│   └── index.ts            # Entry point
├── dist/                   # Compiled JavaScript (generated)
├── coverage/               # Test coverage (generated)
├── .github/
│   └── workflows/          # GitHub Actions
├── Dockerfile              # Docker configuration
├── .dockerignore           # Docker ignore file
├── .gitignore              # Git ignore file
├── .env.example            # Example environment variables
├── tsconfig.json           # TypeScript configuration
├── jest.config.js          # Jest configuration
├── eslint.config.js        # ESLint configuration
├── .prettierrc.json        # Prettier configuration
├── package.json            # Project dependencies
└── README.md               # This file
```

## Code Quality

### Test Coverage
The project maintains high test coverage (70%+ threshold) across:
- Branches
- Functions
- Lines
- Statements

### Code Style
- TypeScript strict mode enabled
- ESLint for code quality
- Prettier for consistent formatting
- Conventional naming and structure

### Security
- Helmet for security headers
- Input validation on all endpoints
- Error handling without exposing internals
- Non-root Docker user
- Regular dependency audits

## Operational Excellence

### Logging
Structured JSON logging with Winston:
- Request/response logging
- Error logging with stack traces
- Info logging for business events

### Monitoring
- Health check endpoint for liveness probes
- Readiness endpoint for readiness probes
- Graceful shutdown handling

### Scalability
- Stateless design (in-memory store is for demo; replace with database for production)
- Docker containerization for easy scaling
- Resource-efficient Node.js runtime

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
