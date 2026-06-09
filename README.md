
# 🌱 HabitTracker
 
A full-stack habit tracking web application built with Django. Track your daily, 
weekly, and monthly habits, build streaks, and monitor progress through a REST API.
 
---
 
## Features
 
- **Habit management** – create, edit, delete, and complete habits
- **Streak tracking** – automatically increments your streak each time you complete a habit
- **Frequency columns** – habits are organized into Daily, Weekly, and Monthly columns
- **Soft delete** – deleted habits are hidden, not permanently removed
- **User authentication** – register, log in, and log out; each user sees only their own habits
- **REST API** – full CRUD API with filtering, searching, and ordering
- **API documentation** – interactive Swagger UI and ReDoc out of the box
---
 
## Tech Stack
 - **Backend**: Django 6, Django REST Framework
 - **Database**: PostgreSQL
 - **API docs**: drf-spectacular (Swagger / ReDoc)
 - **Filtering**: django-filter
 - **Auth**: Django session authentication
 - **Frontend**: Django templates, plain CSS
 
---
 
## Project Structure
 
```
habit_tracker/
├── config/                  # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── habits/                  # Main app
│   ├── models.py            # Habit model
│   ├── views.py             # Template views (ListView, CreateView, etc.)
│   ├── api_views.py         # DRF ViewSet
│   ├── serializers.py       # DRF serializers
│   ├── forms.py             # Django forms
│   ├── urls.py              # Template URL routes
│   ├── api_urls.py          # API URL routes
│   └── templates/
│       ├── base.html
│       ├── habits/
│       │   ├── habit_list.html
│       │   ├── view_habit.html
│       │   ├── add_habit.html
│       │   ├── edit_habit.html
│       │   ├── habit_confirm_delete.html
│       │   ├── _habit_card.html
│       │   └── _form.html
│       └── auth/
│           ├── login.html
│           └── register.html
├── .env                     # Environment variables (not committed)
├── requirements.txt
└── manage.py
```
 
---
 
## Getting Started
 
### Prerequisites
 
- Python 3.10+
- PostgreSQL
### Installation
 
**1. Clone the repository**
```bash
git clone https://github.com/Kotelaa/habit_tracker.git
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
 
## API
 
Base URL: `/api/`
 
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
| `DB_PORT` | Database port (usually `5432`) |
 
---
 
## Contributing
 
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a pull request
