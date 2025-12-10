# High-Level Architecture

## 3.1 Project Overview
This project is a QR Bill application designed to streamline the creation and management of QR-bill payments in Switzerland. It aims to provide a user-friendly interface for generating QR bills, managing customer data, and tracking payment statuses. The application targets small to medium-sized businesses and individuals who need an efficient way to handle their invoicing and payment collection.

Key Features include QR bill generation, customer management, payment tracking, and integration with financial systems.

## 3.2 Technology Stack
| Category | Technology | Version | Purpose |
|-----------|-----------|---------|------------|
| Backend | Python | 3.11 | Core logic |
| Web Framework | FastAPI | 0.104 | REST API |
| Database | PostgreSQL | 14 | Data Storage |
| ORM | SQLAlchemy | 2.0 | Database interaction |

## 3.3 Architectural Diagram


## 3.4 System Components
### FastAPI Application
- **Purpose:** Exposes the REST API for client interactions and handles request routing and validation.
- **Location:** 
- **Key dependencies:** Business Logic Layer, Authentication/Authorization, SQLAlchemy

### Business Logic Layer
- **Purpose:** Contains the core business rules and orchestrates data flows between the API and the database.
- **Location:** 
- **Key dependencies:** Database (via ORM), Utility functions

### Authentication/Authorization
- **Purpose:** Manages user authentication, session management, and access control for API endpoints.
- **Location:** 
- **Key dependencies:** Database (for user data), JWT libraries

### PostgreSQL Database
- **Purpose:** Stores all persistent data including user information, QR bill details, and payment records.
- **Location:** External service
- **Key dependencies:** Accessed via SQLAlchemy ORM

## 3.5 Design Patterns
- **Repository Pattern:** Used for abstracting data access logic, particularly in the  module.
- **Dependency Injection:** Utilized throughout the FastAPI application for managing component dependencies.

## 3.6 Data Flows (high-level)
User requests from the Web Client are routed through the FastAPI application. The API layer then interacts with the Authentication/Authorization component for security checks and the Business Logic Layer for processing. The Business Logic Layer, in turn, communicates with the PostgreSQL database to retrieve or store data. Responses are then sent back through the same path to the client.

