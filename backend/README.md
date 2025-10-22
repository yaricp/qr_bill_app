# QR Bill App – Backend

The **backend** of the QR Bill App consists of three main services that together handle all data processing, analytics, and integrations.

It provides both a **REST API** (for the web frontend) and a **gRPC interface** (for communication with the Telegram bot).

---

## 🧱 Architecture Overview

```
Frontend (PWA) ──► REST API (FastAPI)
                        │
                        ▼
                   PostgreSQL DB
                        ▲
                        │
             Telegram Bot (gRPC client)
                        │
                        ▼
               gRPC Proto Definitions
```

---

## 🗂 Components

### 1. `rest_api/`
The main FastAPI backend providing:
- REST endpoints for users, bills, goods, categories, sellers and analytics  
- Authentication and user data management  
- Integration with PostgreSQL using async SQLAlchemy  
- gRPC server interface for Telegram bot communication  

See [`rest_api/README.md`](rest_api/README.md) for details.

---

### 2. `tg_bot/`
A standalone Telegram bot service that:
- Receives QR codes or receipt photos from users  
- Sends parsed data to the backend via gRPC  
- Creates temporary login links for web access  
- Supports multilingual interaction (EN / RU / ME)  

See [`tg_bot/README.md`](tg_bot/README.md) for setup and usage.

---

### 3. `grpc_proto/`
Contains `.proto` files and generated Python stubs for inter-service communication:
- Defines message schemas and gRPC service contracts  
- Used by both `rest_api` (server) and `tg_bot` (client)  
- Ensures strict type safety and fast communication  

---

## 🧩 Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frameworks** | FastAPI, aiogram |
| **Language** | Python 3.11+ |
| **Database** | PostgreSQL |
| **Inter-service Communication** | gRPC |
| **Auth** | JWT |
| **Containerization** | Docker / Docker Compose |
| **Deployment** | Kubernetes-ready |

---

## ⚙️ Development

Clone the repository and set up your environment:
```bash
git clone https://github.com/yourusername/qr_bill_app.git
cd qr_bill_app/backend
```

### Run locally (with Docker Compose)
```bash
docker compose up --build
```

This will start:
- PostgreSQL database  
- REST API service  
- Telegram bot service  

Each service can also be run individually for development.

---

## 🧪 Testing

Each submodule (`rest_api`, `tg_bot`) contains its own test suite.  
Run tests from the root of the corresponding folder:
```bash
pytest
```

---

## 📄 License

All backend components are part of the **QR Bill App** project and are distributed under the **MIT License**.
