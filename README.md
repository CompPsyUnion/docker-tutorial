# Docker Tutorial

A hands-on tutorial repository for learning Docker & Docker Compose with a real multi-container application.

## Project Overview

This project demonstrates a simple web application with MySQL database integration using Docker & Docker Compose.

**Architecture:**

- **Web Service**: Flask application that connects to MySQL
- **MySQL Service**: Database backend for data persistence

## 1. Quick Start

### Option 1: Use this template + codespaces (recommended for beginners)

1. Click "Use this template" → "Create a new repository"
2. Navigate to your new repository
3. Click "Code" → "Codespaces" → "Create codespace on main"

### Option 2: Clone locally (if you have Docker and Docker Compose installed)

```bash
git clone https://github.com/CompPsyUnion/docker-tutorial.git
cd docker-tutorial
```

## 2. Go through the Docker tutorial in [`/flask_demo_site`](./flask_demo_site) to understand how the application works and how the Dockerfiles are set up

## 3. Compose it up

### Using `GitHub Codespaces`

In the Codespaces `terminal`, run:

```bash
docker compose up -d
```

### Option 2: Local development

```bash
# Under the project directory
docker compose up -d
```

## 4. Access the Application

In Codespaces, Access the application at port `35000`, you can forward your port to the public internet use "Ports" tab in Codespaces, and click the link provided to open in browser.

Once the services are running:

- **Home Page**: [http://localhost:35000](http://localhost:35000)
- **MySQL Test**: [http://localhost:35000/mysql](http://localhost:35000/mysql)

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
