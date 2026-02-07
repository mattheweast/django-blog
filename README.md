# django-blog

README.md - Django Blog Setup
Create this file in django-blog/ root (code README.md).

text
# Django Blog - Setup Guide

## Project Structure
django-blog/ # Root folder
├── manage.py # Django management script
├── personal_blog/ # Project settings/URLs (whole site)
├── blog/ # Blog app (models/views/templates)
├── db.sqlite3 # SQLite database
├── venv/ # Virtual environment
└── README.md
## Step-by-Step Setup

### 1. Project Directory + Virtual Environment
```bash
mkdir django-blog
cd django-blog
python3 -m venv venv      # Isolated Python environment
source venv/bin/activate  # Activate (shows (venv) prompt)
```
Why: Virtual env keeps project packages separate from system Python.

### 2. Install Django

```bash
pip install Django        # Installs Django 6.0.2 + dependencies
```
Why: Django framework for web app.

### 3. Create Django Project

```bash
django-admin startproject personal_blog .  # "." = current dir (not nested)
Why: personal_blog/ = global project container (settings/URLs).
```

### 4. Test Development Server

```bash
python manage.py migrate              # Create initial DB tables
python manage.py runserver            # http://127.0.0.1:8000/
Why: Confirms project works (Django welcome page).
```

### 5. Create Blog App

```bash
python manage.py startapp blog
Register in personal_blog/settings.py:
```

```python
INSTALLED_APPS = [
    ...
    'blog.apps.BlogConfig',  # Tells Django about blog app
]
```
Why: Apps = modular components. Project contains many apps.

### 6. Create Superuser

```bash
python manage.py createsuperuser      # admin /admin/ login
```
Why: Access Django admin interface.

### 7. Define Models (blog/models.py)

Purpose: Python classes → Database tables

- Category → blog_category table

- Post → blog_post table

- Comment → blog_comment table

Next: python manage.py makemigrations blog + migrate

### Key Concepts Learned

- venv: Isolated dependencies

- Project vs App: personal_blog/ (site) contains blog/ (feature)

- Models: class X(models.Model) = DB table

- Fields: CharField() = column

- __str__(): Human-readable object names

- Meta: Model options (plural names)

```text
**Copy-paste this into README.md**, commit `git add . && git commit -m "Initial setup"`. Perfect future reference!

Say "next" for `admin.py` registration.
```