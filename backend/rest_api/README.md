# QR Bill App – REST API

The **REST API** of the QR Bill App is built with **FastAPI** and serves as the main backend for:

- Managing bills, goods, categories, and analytics
- Providing a RESTful interface for the frontend PWA
- Communicating with the Telegram bot via gRPC
- Handling authentication, user data, and secure access

It is designed to be modular, asynchronous, and ready for containerized deployment.

---

### `src/app/`

Contains the main business logic:
- Modules for bills, categories, goods, users, products, units, sellers
- Metrics and helper utilities
- Authentication and login link handling

### `src/api/`

- Routers, middleware, dependencies
- API versioning (`v1`) and metrics endpoints

### `src/infra/`

- Database connection and ORM models
- gRPC server implementation
- Email and Telegram integration
- Metrics collection

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

## ⚙️ Setup & Development

### 1. Install dependencies
Using **Poetry**:
```bash
cd rest_api
poetry install
poetry shell
