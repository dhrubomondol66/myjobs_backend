# MY JOBS Backend

A robust Django REST Framework (DRF) backend API for a Company Review & Compensation Benchmarking platform. This platform enables users to share and view company reviews anonymously, benchmark salaries and benefits, and gain career insights.

---

## 🚀 Features

- **Authentication & Security**: Email/password registration, login via JWT (JSON Web Token), password reset flow.
- **Company Profile Management**: Create, view, update, and delete company profiles.
- **Compensation & Salary Benchmarking**: Anonymous submissions of salary, bonuses, fringe benefits, and other allowances.
- **Anonymous Reviews**: Share and browse anonymous company reviews detailing management quality, work-life balance, environment, and more.
- **Credits System**: Gamified "Give Data, Get Data" model where submitting reviews rewards users with credits.
- **Analytics & Aggregations**: Detailed analytics summary, salary list, and stats on salaries.
- **Interactive Documentation**: Swagger and ReDoc integration.

---

## 🛠️ Tech Stack

- **Framework**: Django 5.2.7 & Django REST Framework 3.16.1
- **Database**: PostgreSQL (via `psycopg2-binary` & `dj-database-url`)
- **Authentication**: JWT (`djangorestframework-simplejwt` & `django-allauth`)
- **Documentation**: Swagger UI & ReDoc (`drf-yasg`)
- **CORS**: `django-cors-headers`
- **Environment**: `django-environ` & `python-dotenv`

---

## ⚙️ Setup and Installation

### 1. Prerequisites
- Python 3.12+ installed on your system.
- PostgreSQL database running locally or hosted.

### 2. Clone and Setup Environment
Navigate to the root directory of the backend:
```bash
cd "e:\react(practice)\MY JOBS\My jobs\myjobs"
```

### 3. Create a Virtual Environment
```bash
python -m venv venv
```
Activate the virtual environment:
- **Windows (CMD/PowerShell)**:
  ```powershell
  .\venv\Scripts\activate
  ```
- **Linux/macOS**:
  ```bash
  source venv/bin/activate
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Environment Variables
Create a `.env` file in the root directory (based on the active configurations):
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/myjobs_db
DEBUG=True
SECRET_KEY=your-django-insecure-key
ALLOWED_HOSTS=127.0.0.1, localhost, .onrender.com
EMAIL_HOST_USER=your_email@domain.com
EMAIL_HOST_PASSWORD=your_email_host_password
SENDGRID_API_KEY=your_sendgrid_key
```

### 6. Run Database Migrations
Apply the migrations to configure your database schema:
```bash
python manage.py migrate
```

### 7. Run the Development Server
```bash
python manage.py runserver
```
The server will start at `http://127.0.0.1:8000/`.

---

## 🔌 API Endpoints Summary

### 🔑 Authentication (`/accounts/`)
- `POST /accounts/register/` - Register a new user account.
- `POST /accounts/login/` - Login and receive JWT tokens.
- `POST /accounts/forgot-password/` - Send password reset email.
- `POST /accounts/reset-password/` - Reset password using the reset token.

### 🏢 Companies (`/companies/`)
- `GET /companies/` - List all companies.
- `POST /companies/create/` - Create a new company.
- `GET /companies/<id>/` - Retrieve details of a specific company.
- `PUT/PATCH /companies/<id>/update/` - Update company details (Authenticated).
- `DELETE /companies/<id>/delete/` - Delete a company (Authenticated).

### 💰 Compensation (`/compensation/`)
- `GET /compensation/` - List all submitted compensations (ordered by newest).
- `POST /compensation/create/` - Submit salary and benefit information (Authenticated).
- `GET /compensation/<id>/` - Retrieve details of a specific compensation.
- `PUT/PATCH /compensation/<id>/update/` - Update compensation data (Only the owner).
- `DELETE /compensation/<id>/delete/` - Delete compensation data (Only the owner).

### 📝 Reviews (`/reviews/`)
- `GET /reviews/` - List all company reviews.
- `POST /reviews/create/` - Create a review. Automatically adds +10 credits to user (Authenticated).
- `GET /reviews/<id>/` - Retrieve specific company review.

### 👤 Profile (`/myprofile/`)
- `GET /myprofile/me/` - Retrieve authenticated user's profile.
- `PUT/PATCH /myprofile/update/` - Update profile details.

### 📊 Analytics (`/analytics/`)
- `GET /analytics/summary/` - Statistical dashboard summary.
- `GET /analytics/salary/` - Detailed salary analytics lists.
- `GET /analytics/salary/stats/` - Salary stats and average breakdowns.

---

## 📖 API Documentation

Interactive API documents are automatically generated and can be accessed at:
- **Swagger UI**: `http://127.0.0.1:8000/swagger/`
- **ReDoc**: `http://127.0.0.1:8000/redoc/`
- **JSON Schema**: `http://127.0.0.1:8000/swagger.json/`
