
# 🌱 Habit and Mood Tracker
 
A web application for tracking daily, weekly, and monthly habits with mood 
logging and streak tracking. Built with Django and PostgreSQL.

**Live demo:** https://habittracker-production-8eea.up.railway.app

---
 
## Features
 
- **User authentication** – register, log in, and log out; each user sees only their own habits
- **Habit management** – create, edit, delete, and complete habits
- **Soft delete** – deleted habits are hidden, not permanently removed
- **Track streaks** – complete habits and watch your streak grow
- **Frequency columns** – habits are organized into Daily, Weekly, and Monthly columns
- **Mood logging** – log your mood once per day with notes
- **REST API** – full CRUD API with filtering, searching, and ordering
- **API documentation** – interactive Swagger UI and ReDoc
- Deployed on Railway with PostgreSQL


---
 
## Tech Stack
 - **Backend**: Python 3.14, Django 6.0 , Django REST Framework
 - **Database**: PostgreSQL
 - **API**: Django REST Framework , 
 - **API Docs**: drf-spectacular (Swagger / ReDoc)
 - **Filtering**: django-filter
 - **Auth**: Django built-in authentication 
 - **Frontend**: Django templates, plain CSS
 - **Static files**: WhiteNoise
 - **Deployment**: Railway



---
 
## Project Structure
 
```
## Project Structure
habit_tracker/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── habits/
│   ├── models.py           # Habit and Mood models
│   ├── views.py            # Class-based views
│   ├── api_views.py        # DRF ViewSets
│   ├── serializers.py      # DRF Serializers
│   ├── forms.py            # Django forms
│   ├── urls.py             # URL patterns
│   ├── api_urls.py         # API URL patterns
│   ├── authentication_view.py  # Registration view
│   └── mood_view.py        # Mood views
├── templates/
│   ├── base.html
│   ├── auth/
│   └── habits/
├── static/
├── .env.example
├── manage.py
├── Procfile
├── requirements.txt
└── runtime.txt
```
 

---
 
## Getting Started
 
### Prerequisites
 
- Python 3.10+
- PostgreSQL
### Installation
 
**1. Clone the repository**
```bash
git clone https://github.com/Kotelaa/habit-mood-tracker
cd habit_tracker
```
 
**2. Create and activate a virtual environment**
```bash
python -m venv .venv
 
# Windows
.venv\Scripts\activate
 
# macOS / Linux
source .venv/bin/activate
```
 
**3. Install dependencies**
```bash
pip install -r requirements.txt
```
 
**4. Create a `.env` file in the project root**
```env
SECRET_KEY=your-secret-key-here
DB_NAME=habit_tracker
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```
 
**5. Create the database and run migrations**
```bash
python manage.py migrate
```
 
**6. Create a superuser (optional — for admin access)**
```bash
python manage.py createsuperuser
```
 
**7. Run the development server**
```bash
python manage.py runserver
```
 
Visit `http://127.0.0.1:8000` in your browser.
 

---
 
## API Endpoints

### Habits
 
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/habits/` | List all habits |
| POST | `/api/habits/` | Create a habit |
| GET | `/api/habits/{id}/` | Get one habit |
| PUT | `/api/habits/{id}/` | Update a habit |
| PATCH | `/api/habits/{id}/` | Partially update a habit |
| DELETE | `/api/habits/{id}/` | Soft-delete a habit |
| POST | `/api/habits/{id}/complete/` | Mark habit as completed (+1 streak) |
| GET | `/api/habits/stats/` | Get aggregated stats |


### Query parameters (list endpoint)
 
| Parameter | Description | Example |
|---|---|---|
| `search` | Filter by name or description | `?search=exercise` |
| `frequency` | Filter by frequency | `?frequency=daily` |
| `ordering` | Sort results | `?ordering=-streak` |


### Mood
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/mood/ ` | List mood entries  |
| POST | `/api/mood/  ` | Log today's mood |
| PATCH | `/api/mood/{id}/` | Update today's mood  |


 
### API documentation
 
| URL | Description |
|---|---|
| `/api/swagger/` | Swagger UI – interactive docs |
| `/api/redoc/` | ReDoc – readable docs |
| `/api/schema/` | Raw OpenAPI schema (JSON) |
 
All API endpoints require authentication. Log in via the web interface 
first (session auth), or configure token/JWT authentication for external clients.

---
 
## Environment Variables
 
| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DB_NAME` | PostgreSQL database name |
| `DB_USER` | PostgreSQL user |
| `DB_PASSWORD` | PostgreSQL password |
| `DB_HOST` | Database host (usually `localhost`) |
| `DB_PORT` | Database port (usually `5432`) |'

