# Habit Tracker

A habit tracking web app built with Django and PostgreSQL.

## Features
- Create, edit, delete habits
- Track streaks
- User authentication

## Tech Stack
- Python
- Django
- PostgreSQL
- HTML and CSS (Glassmorphism design)

## How to run locally

1. Clone the repo
   git clone https://github.com/yourusername/habit-tracker.git
   cd habit-tracker

2. Create virtual environment
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Mac/Linux

3. Install dependencies
   pip install -r requirements.txt

4. Create .env file
   DB_NAME=your-db-name
   DB_USER=postgres
   DB_PASSWORD=yourpassword
   DB_HOST=localhost
   DB_PORT=5432
   SECRET_KEY=your-secret-key
   DEBUG=True

5. Run migrations
   python manage.py migrate

6. Run server
   python manage.py runserver
