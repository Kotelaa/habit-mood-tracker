# Habit Tracker
A habit tracking web app built with Django and PostgreSQL.

## Features
This app alows you create, edit, delete habits; track streaks; user authentication.

## Tech Stack
- Python
- Django
- PostgreSQL
- HTML and CSS (Glassmorphism design)

## How to run locally

1. Clone the repo
   git clone https://github.com/yourusername/habit-tracker.git
   cd habit-tracker

2. Create and activate virtual environment
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Mac/Linux

3. Install dependencies
   pip install -r requirements.txt

4. Create .env file with: DB_NAME, DB_USER, DB_PASSWORD, DB_HOS, DB_PORT, SECRET_KEY

5. Run migrations: python manage.py migrate

6. Run server: python manage.py runserver
