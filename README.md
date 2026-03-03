# Docker Compose Tutorial

A hands-on tutorial repository for learning Docker Compose with a real multi-container application.

## Project Overview

This project demonstrates a simple web application with MySQL database integration using Docker Compose.

**Architecture:**

- **Web Service**: Flask application that connects to MySQL
- **MySQL Service**: Database backend for data persistence

## Quick Start

### Option 1: Use this template

1. Click "Use this template" → "Create a new repository"
2. Navigate to your new repository
3. Click "Code" → "Codespaces" → "Create codespace on main"
4. In the Codespaces terminal, run:

   ```bash
   docker compose up -d
   ```

### Option 2: Clone locally

```bash
git clone https://github.com/YOUR_USERNAME/docker-tutorial.git
cd docker-tutorial
docker compose up -d
```

## Access the Application

Once the services are running:

- **Home Page**: [http://localhost:5000](http://localhost:5000)
- **MySQL Test**: [http://localhost:5000/mysql](http://localhost:5000/mysql)

In Codespaces, use the "Ports" tab to access the forwarded URLs.

## Project Structure

```text
.
├── docker-compose.yml    # Multi-service configuration
├── src/
│   ├── app.py            # Flask application
│   └── Dockerfile        # Web service image definition
└── README.md
```

## Useful Commands

```bash
# Start all services in background
docker compose up -d

# View service status
docker compose ps

# View logs (all services)
docker compose logs -f

# View logs (specific service)
docker compose logs -f web

# Stop all services
docker compose down

# Stop and remove volumes
docker compose down -v

# Rebuild and restart
docker compose up -d --build
```

## Environment Variables

The web service uses the following environment variables to connect to MySQL:

| Variable | Description | Default |
|----------|-------------|---------|
| `MYSQL_HOST` | MySQL server hostname | `mysql` |
| `MYSQL_PORT` | MySQL server port | `3306` |
| `MYSQL_USER` | Database username | `root` |
| `MYSQL_PASSWORD` | Database password | `123456` |
| `MYSQL_DATABASE` | Database name | `testdb` |

## Learning Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Compose File Reference](https://docs.docker.com/compose/compose-file/)
- [Weekly Session Repository](https://github.com/CompPsyUnion/2526-weekly-session)

## License

MIT License - see [LICENSE](LICENSE) for details.
