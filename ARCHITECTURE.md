# Django Blog — Architecture Overview

A short, simple explanation of how this site components interact.

Request flow (high level)

- Browser sends HTTP request (e.g. GET / or GET /post/1/).
- `personal_blog/urls.py` receives the request and forwards to app routers (it includes `blog.urls`).
- `blog/urls.py` matches the path (e.g. `post/<int:pk>/`) and calls the corresponding view function in `blog/views.py`.
- The view:
  - reads URL params and request data (POST/GET)
  - queries the database via Django ORM (`blog/models.py`) to get model instances (`Post`, `Comment`, `Category`)
  - validates or saves form data (via `blog/forms.py`) if needed
  - builds a context dict and calls `render(request, 'template.html', context)`
- The template from `blog/templates/` (e.g. `blog_detail.html`) uses the context to produce HTML.
- Django returns the rendered HTML as the HTTP response.

Key files and roles

- `manage.py` — CLI for running server, migrations, shell, etc.
- `personal_blog/settings.py` — project settings (INSTALLED_APPS, DATABASES, SECRET_KEY). Loads `.env` when configured.
- `personal_blog/urls.py` — root URL router that includes app URLConfs.
- `blog/models.py` — defines `Post`, `Category`, `Comment` (database schema).
- `blog/views.py` — view functions that handle requests and return responses.
- `blog/urls.py` — URL patterns for the blog app.
- `blog/forms.py` — form classes (e.g. `CommentForm`).
- `blog/templates/` — HTML templates used by views.
- `db.sqlite3` — local SQLite database (ignored in git).

Local dev checklist (quick commands)

```bash
# create & activate venv (if needed)
python3 -m venv venv
source venv/bin/activate

# install deps
pip install -r requirements.txt
# if python-dotenv not in requirements:
pip install python-dotenv

# load env and run DB setup
python manage.py migrate
python manage.py createsuperuser   # optional
python manage.py runserver
```

Secrets and `.env` (short)

- Put `SECRET_KEY` in a `.env` file at the project root (same dir as `manage.py`):

```text
SECRET_KEY=<your-secret-key>
```

- `personal_blog/settings.py` should call `load_dotenv()` (from `python-dotenv`) before using `os.getenv('SECRET_KEY')`.
- Add `.env` to `.gitignore` to avoid pushing secrets.

If you want, I can add a one-line link to this file in `README.md` or update `SETUP.md` instead of creating this file. Which do you prefer?