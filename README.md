# TaskFlow - Django Task Management System

Stack: Python, Django, MySQL, HTML, CSS, JavaScript

## Setup
1. python -m venv venv  &&  venv\Scripts\activate   (Linux/Mac: source venv/bin/activate)
2. pip install -r requirements.txt
3. In MySQL:  CREATE DATABASE taskmanager_db CHARACTER SET utf8mb4;
4. Set your MySQL password in config/settings.py (or env var DB_PASSWORD)
5. python manage.py makemigrations tasks
6. python manage.py migrate
7. python manage.py createsuperuser   (optional, for /admin/)
8. python manage.py runserver  ->  http://127.0.0.1:8000/

(To try without MySQL first: set USE_SQLITE=1 before running the commands.)

## Features
Register/login, per-user tasks, create/edit/delete, mark done, priority, status,
due dates with overdue highlight, search and filters, dashboard counts.
