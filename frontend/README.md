# QR Bill App – Frontend

The **frontend** of the QR Bill App is a **Vue.js Progressive Web App (PWA)** that provides a user-friendly interface for managing receipts, purchases, and analytics.  
It interacts with the REST API backend and supports integration with the Telegram bot.

---

## 🗂 Project Structure

frontend/
├── Dockerfile # Docker image for frontend
├── start.sh # Script to start frontend locally
├── package.json # NPM dependencies and scripts
├── yarn.lock # Yarn lock file
├── babel.config.js
├── jsconfig.json
├── tsconfig.json
├── vue.config.js
├── public/ # Static assets (favicon, index.html)
├── dist/ # Build output
├── node_modules/ # Dependencies
├── nginx/ # Nginx config for deployment
└── src/
├── main.ts # Vue application entry point
├── App.vue # Root Vue component
├── router.ts # Vue Router configuration
├── store/ # Vuex store modules
├── api/ # API requests and services
├── services/ # Business logic services
├── plugins/ # Vue plugins
├── assets/ # Images, fonts, styles
├── locales/ # Translation files
├── components/ # Reusable UI components
├── pages/ # Page components (About, Admin, User)
├── interfaces/ # TypeScript interfaces
├── constants.ts # App-wide constants
├── env.ts # Environment variables
├── shims-vue.d.ts
└── registerServiceWorker.js

### `src/components/`

- UI components like `BSNavbar.vue`, `BSTooltip.vue`, `QRScanner.vue`  
- Analytics and utilities components  

### `src/pages/`

- Application pages: `About.vue`, `admin/`, `user/`  

### `src/interfaces/`

- TypeScript interfaces for data models: bills, categories, products, users, sellers, etc.

---

## 🧩 Tech Stack

| Layer | Technology |
|-------|------------|
| **Framework** | Vue.js 3 (Composition API) |
| **Language** | TypeScript |
| **State Management** | Vuex |
| **Routing** | Vue Router |
| **HTTP Client** | Axios (via `api` folder) |
| **PWA** | Service worker, offline support |
| **Build Tool** | Vite (configured via Vue CLI) |
| **Containerization** | Docker + Nginx for deployment |
| **Localization** | Multi-language support in `locales/` |

---

## ⚙️ Setup & Development

### 1. Install dependencies

```bash
cd frontend
yarn install
```

### 2. Environment Variables

Set any variables in src/env.ts or .env if required. Example:

export const API_BASE_URL = 'http://localhost:8000';


### 3. Running the App Locally

yarn serve

or using the provided script:

./start.sh

The app will be available at:
👉 http://localhost:8080


### 4. Build for Production

yarn build

The build output will be in the dist/ folder.

### 5. Docker Deployment

docker build -t qr-bill-frontend .
docker run -p 80:80 qr-bill-frontend

---

## License

The frontend is part of the QR Bill App and is distributed under the MIT License.
