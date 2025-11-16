# QR Bill App

**QR Bill App** is a personal project and a fully functional example of an expense tracking application built from scratch. It demonstrates a practical implementation of modern web technologies, backend development, and data analytics in a compact and user-friendly interface.

## Project Idea

The main goal of **QR Bill App** is to provide a simple, secure, and efficient way to track expenses using QR codes from bills and receipts. It is designed as a personal finance tool that helps users categorize and analyze their spending habits while keeping all data private.

Key principles of the project:  
- **Privacy-first:** No mandatory registration, optional account recovery, no third-party data sharing.  
- **Automation:** Automatic categorization of recurring items to reduce manual input.  
- **Insightful Analytics:** Charts and statistics for expenses, quantities, price changes, and vendor analysis.  
- **Cross-platform:** Works as a Progressive Web App and integrates with a Telegram bot for convenient data input.  

## Features

- Scan QR codes on receipts and bills for instant data entry.  
- Create and manage categories, vendors, and purchases.  
- Automatic categorization of previously entered items.  
- Analytics and reports:  
  - Expenses by category, vendor, and product  
  - Quantity tracking (units, kg, kWh, etc.)  
  - Price change trends for selected items  
- Lists with sorting and filtering: receipts, purchases, vendors, and categories.  
- Telegram bot integration for submitting receipts via images or QR codes.  
- Multi-language support (English, Russian, local language).  
- Fully anonymous use, with optional account linking for data recovery.  

## Tech Stack

- **Frontend:** Vue.js + Nginx (PWA support)  
- **Backend:** FastAPI (Python)  
- **Database:** PostgreSQL  
- **Communication:** gRPC between Telegram bot and API  
- **Containerization:** Docker (for all services)  
- **Deployment:** Can be deployed locally, in Docker Compose, or Kubernetes  
- **Other:** Telegram Bot for easy receipt input  

## Purpose

This project serves as a **demonstration of full-stack application development** including:  
- Backend and API design  
- Frontend UI/UX implementation  
- Database modeling and analytics  
- Secure handling of sensitive data  
- Integration with third-party messaging services (Telegram)  
- Containerized deployment and task automation  

It is intended as a showcase for developers, employers, or anyone interested in seeing a real-life example of a personal finance application built from scratch.

## Getting Started

1. Clone the repository:  
   ```bash
   git clone https://github.com/yourusername/qr_bill_app.git
   ```
2. Install dependencies and configure environment variables (see `.env.example`).  
3. Run with Docker Compose or deploy to Kubernetes for full functionality.

