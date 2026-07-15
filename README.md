# Placement Portal V2 — MAD-II (Jan 2026)

A comprehensive, web-based campus placement management system built for the IIT Madras BS Degree — Modern Application Development II (MAD-II) course. This portal facilitates smooth interactions between students seeking jobs, companies posting placement drives, and administrators overseeing the recruitment lifecycle.

## Features

- **Role-Based Access Control (RBAC):** Distinct dashboards and permissions for Students, Companies, and Administrators.
- **Student Capabilities:** Profile creation, resume uploads, browsing job drives, and applying to jobs.
- **Company Capabilities:** Company profile setup, posting placement drives, managing applications, and updating candidate statuses.
- **Administrator Oversight:** Reviewing and approving company registrations, managing students, system monitoring, and exporting reports.
- **Asynchronous Operations:** Automated email notifications and background CSV report exports using Celery & Redis.
- **Responsive UI:** Modern, reactive, and mobile-friendly interface.

## Tech Stack

### Backend
- **Framework:** Flask (Python)
- **Database:** SQLite with Flask-SQLAlchemy ORM
- **Authentication:** Flask-JWT-Extended (JWT-based secure access)
- **Task Queue:** Celery with Redis broker

### Frontend
- **Framework:** Vue 3 (Composition API)
- **Build Tool:** Vite
- **State Management:** Pinia
- **Routing:** Vue Router 4
- **Styling:** Bootstrap 5 (via CDN)
- **HTTP Client:** Axios

## Project Structure

```text
placement_portal_v2/
├── backend/                  # Flask REST API and Celery workers
│   ├── app.py                # Main application entry point
│   ├── config.py             # Environment and app configuration
│   ├── models/               # SQLAlchemy DB schema models
│   ├── routes/               # API Blueprints (Auth, Admin, Student, Company)
│   ├── services/             # Core business logic
│   ├── tasks/                # Celery async tasks (Emails, Exports)
│   ├── requirements.txt      # Python dependencies
│   └── api.yaml              # Swagger/OpenAPI documentation
│
└── frontend/                 # Vue 3 Frontend app
    ├── src/
    │   ├── components/       # Reusable UI components
    │   ├── views/            # Page-level components
    │   ├── stores/           # Pinia state stores
    │   └── router/           # Vue Router config
    ├── index.html            # Main HTML template
    ├── package.json          # Node dependencies and scripts
    └── vite.config.js        # Vite bundler config
```

## Setup & Installation

### Prerequisites
- Python 3.9+
- Node.js 18+ & npm
- Redis Server (Running locally on default port 6379)

### 1. Backend Setup

Open a terminal and navigate to the `backend` directory:
```bash
cd backend
```

**Create and activate a virtual environment:**
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Environment Variables:**
Create a `.env` file in the `backend` folder with the necessary configuration:
```ini
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_here
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
GOOGLE_CHAT_WEBHOOK_URL=optional_webhook_url
```

**Initialize Database:**
Run the Flask application once. `placement.db` is configured to be automatically created in the `backend/instance` folder on initial startup.

### 2. Frontend Setup

Open a new terminal and navigate to the `frontend` directory:
```bash
cd frontend
```

**Install dependencies:**
```bash
npm install
```

## Running the Application

To run the full stack, you need to start 4 separate services:

**1. Start Redis Server**
Ensure your local Redis server is up and running.
```bash
redis-server
```

**2. Start Flask Backend** (Inside the `backend` folder, with `venv` activated)
```bash
flask run --debug
```

**3. Start Celery Worker** (Inside the `backend` folder, with `venv` activated)
```bash
celery -A celery_app.celery_app worker --loglevel=info
```

**4. Start Vue Frontend** (Inside the `frontend` folder)
```bash
npm run dev
```

The application should now be accessible at `http://localhost:5173` (Frontend) and `http://localhost:5000` (Backend).

## API Documentation
The complete API specification is available in the `backend/api.yaml` file. You can import this file into Postman or Swagger UI to explore and test the available endpoints.
