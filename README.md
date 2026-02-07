# Django Blog

Small personal blog built with Django. This repository contains a minimal example app used for learning and small personal sites.

Contents
- `personal_blog/` — Django project (settings, root URLs, WSGI/ASGI)
- `blog/` — Blog app: models, views, templates, forms, admin
- `db.sqlite3` — Local SQLite database (ignored for sharing)
- `.env` — Local environment variables (not committed)

Quick start

```bash
# create & activate virtualenv
python3 -m venv venv
source venv/bin/activate

# install dependencies
pip install -r requirements.txt

# apply DB migrations
python manage.py migrate

# create admin user (optional)
python manage.py createsuperuser

# run development server
python manage.py runserver
```

Secrets & configuration
- Add `SECRET_KEY` to a `.env` file at the project root (same folder as `manage.py`).
- `.env` is loaded by `personal_blog/settings.py` via `python-dotenv`.
- Make sure `.env` is listed in `.gitignore`.

Where to look
- Read the component mapping in `ARCHITECTURE.md` for a short explanation of how the request flow and files interact.
- App views: `blog/views.py`
- Templates: `blog/templates/`
- Models (DB): `blog/models.py`

Contributing / Notes
- This project is intentionally small and educational. If you publish it, rotate the `SECRET_KEY` and set `DEBUG=False` in production.

If you want, I can also add a short developer checklist or badge links. 
