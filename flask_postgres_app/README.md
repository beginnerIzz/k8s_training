# Flask PostgreSQL Docker App

## Project Setup

### Prerequisites
- Docker
- Docker Compose (optional)

### Running the Application

1. Build the Docker image:
```bash
docker build -t flask-postgres-app .
```

2. Run the container:
```bash
docker run -d \
  --name flask-app \
  -p 5000:5000 \
  -e DB_HOST=host.docker.internal \
  -e DB_PORT=5432 \
  -e DB_NAME=postgres \
  -e DB_USER=postgres \
  -e DB_PASS=your_password \
  flask-postgres-app
```

### Environment Variables
- `DB_HOST`: PostgreSQL host (default: localhost)
- `DB_PORT`: PostgreSQL port (default: 5432)
- `DB_NAME`: Database name (default: postgres)
- `DB_USER`: Database username (default: postgres)
- `DB_PASS`: Database password
