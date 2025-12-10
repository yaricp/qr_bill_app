# REST API Service

This directory contains the FastAPI-based RESTful API service for the QR Bill application. It serves as the primary interface for the frontend and other services to interact with the application's core logic and data.

## Purpose

The REST API handles incoming HTTP requests, processes business logic, interacts with the database, and communicates with other services (e.g., gRPC server, Telegram). It provides a structured and versioned API for managing bills, products, users, and other related entities.

---

## 🧩 Tech Stack

| Layer | Technology |
|-------|------------|
| **Framework** | FastAPI |
| **Language** | Python 3.11+ |
| **Database** | PostgreSQL |
| **Migrations** | Alembic |
| **Inter-service Communication** | gRPC |
| **Containerization** | Docker / Docker Compose |
| **Dependency Management** | Poetry |
| **Testing** | Pytest |

---

## Project Structure

- **Dockerfile**: Defines the Docker image for the REST API service, specifying its environment and dependencies.
- [**alembic/**](alembic/README.md): Contains database migration scripts managed by Alembic.
- , : Poetry configuration files for dependency management.
- [**scripts/**](scripts/README.md): Utility scripts for various development and operational tasks.
- [**src/**](src/README.md): Contains the main source code of the FastAPI application.
    - [**api/**](src/api/README.md): Defines API routes, configurations, dependencies, and middleware.
    - [**app/**](src/app/README.md): Holds the core application business logic, entities, and metrics definitions.
    - [**infra/**](src/infra/README.md): Manages infrastructure-related components such as database connections, email services, gRPC server integration, and Telegram client.
    - [**tests/**](src/tests/README.md): Contains unit and integration tests for the API and application logic.
    - : General utility functions used across the application.
- : Shell script to start the FastAPI application.
- : Script to start the gRPC server component of the API.
- : Shell script to run tests.

---

## Key Interactions

- The FastAPI application in  defines the HTTP endpoints, using dependencies from  for common functionalities like authentication and database sessions.
- Business logic is encapsulated in , which interacts with data models defined in  and external services via clients in .
- Database migrations are managed through Alembic (), ensuring that the database schema is up-to-date with the application's models.
- gRPC communication is handled by , allowing the REST API to interact with other gRPC services.

## Getting Started

To run this service, ensure you have Python and Poetry installed.
1. Navigate to this directory.
2. Install dependencies: poetry install
3. Run migrations (if necessary): 
4. Start the application: 
