# QR Bill App

This project is a full-stack application for generating and managing bills with QR codes. It consists of a FastAPI backend, a web-based frontend, and all the necessary configurations for deployment.

## Table of Contents

- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Backend](backend/README.md)
- [Frontend](frontend/README.md)
- [Deployment](deployment/README.md)

## Project Structure

The project is organized into the following directories:

- **backend:** Contains the FastAPI application, including the API, database models, and business logic.
- **frontend:** Contains the web-based frontend, built with a modern JavaScript framework.
- **deployment:** Contains Docker files and other configurations for deploying the application.
- **scripts:** Contains various scripts for managing the project, such as database migrations and tests.
- **email_templates:** Contains templates for emails sent by the application.
- **openapi:** Contains the OpenAPI specification for the backend API.
- **ubuntu_system:** Contains system-level configurations for the Ubuntu server.

## Architecture diagram of the project

```mermaid
graph TD
    %% Определение стилей
    classDef user fill:#f9f,stroke:#333,stroke-width:2px;
    classDef front fill:#d4edda,stroke:#28a745,stroke-width:2px;
    classDef back fill:#cce5ff,stroke:#007bff,stroke-width:2px;
    classDef db fill:#fff3cd,stroke:#ffc107,stroke-width:2px;
    classDef ext fill:#e2e3e5,stroke:#6c757d,stroke-width:2px,stroke-dasharray: 5 5;

    %% Внешние узлы
    UserWeb("👤 Web User<br>Browser")
    UserTG("👤 Telegram User<br>Mobile/Desktop")
    ExtSMTP("📧 External SMTP<br>Email Provider")
    TeleAPI("☁️ Telegram API<br>Cloud")

    %% Docker Окружение
    subgraph Docker_Network [🐳 DOCKER COMPOSE NETWORK]
        direction TB
        
        subgraph FrontContainer [Frontend Container :80]
            Nginx("Nginx Proxy")
            VueApp("Vue.js Files")
        end

        subgraph BotContainer [TG Bot Container]
            TGBot("🤖 AIOGRAM Bot<br>Long Polling")
        end

        subgraph APIContainer [REST API Container :8080]
            FastAPI("⚡ FastAPI<br>REST Server :80")
            GRPCServer("🔌 gRPC Server<br>Port :50051")
        end

        subgraph DataLayer
            Postgres[("🐘 PostgreSQL<br>Port :5432")]
            Redis[("🔴 Redis<br>Cache/Queue<br>Port :6379")]
            PgAdmin("🛠️ PgAdmin4<br>Port :5050")
        end
    end

    %% Связи
    UserWeb -- "HTTP/HTTPS (80/443)" --> Nginx
    Nginx -- "Static Files" --> VueApp
    Nginx -- "Proxy /api/* (JSON)" --> FastAPI
    
    UserTG -.-> TeleAPI
    TeleAPI -- "Updates (Polling)" --> TGBot
    TGBot == "gRPC / Protobuf" ==> GRPCServer

    FastAPI -- "SQL (SQLAlchemy)" --> Postgres
    FastAPI -- "Redis Protocol" --> Redis
    FastAPI -- "SMTP" --> ExtSMTP
    
    PgAdmin -- "SQL" --> Postgres
    GRPCServer -.-> FastAPI

    %% Применение стилей
    class UserWeb,UserTG user;
    class Nginx,VueApp front;
    class TGBot,FastAPI,GRPCServer back;
    class Postgres,Redis,PgAdmin db;
    class ExtSMTP,TeleAPI ext;

```

## Getting Started

To get started with the project, you'll need to have Docker and Docker Compose installed. Then, you can run the following command to start the application:

`docker-compose up -d`

This will start the backend, frontend, and all the necessary services. You can then access the frontend at `http://localhost:3000` and the backend at `http://localhost:8000`.
