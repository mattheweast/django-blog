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
- `personal_blog/settings.py` — project settings (INSTALLED_APPS, DATABASES, SECRET_KEY, LOGIN_REDIRECT_URL). Loads `.env` when configured.
- `personal_blog/urls.py` — root URL router that includes app URLConfs and auth URLs.
- `blog/models.py` — defines `Post`, `Category`, `Comment` (database schema). Comment has ForeignKey to User.
- `blog/views.py` — view functions: blog_index, blog_detail, blog_category, register.
- `blog/urls.py` — URL patterns for the blog app (includes /register/).
- `blog/forms.py` — form classes (`CommentForm` with body field only).
- `blog/templates/` — blog-specific HTML templates.
- `personal_blog/templates/` — project-level templates (base.html, registration/).
- `personal_blog/templates/registration/` — authentication templates (login.html, register.html, logged_out.html).
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

Authentication flow

**URL Routing:**
- `/accounts/login/` → Django's built-in LoginView
- `/accounts/logout/` → Django's built-in LogoutView
- `/register/` → Custom `register()` view in `blog/views.py`

**Registration:**
1. User submits UserCreationForm (username, password1, password2)
2. Django validates: passwords match, username unique, password strength
3. Password hashed automatically (PBKDF2-SHA256)
4. User created in database
5. User logged in via `login(request, user)`
6. Redirected to homepage

**Commenting:**
1. User must be authenticated (`request.user.is_authenticated`)
2. Comment form only shows body field
3. View sets `comment.user = request.user` before saving
4. Comment linked to User via ForeignKey
5. Template displays username from `comment.user.username`

**Templates:**
- `base.html` checks `user.is_authenticated` to show login/logout links
- `blog_detail.html` only shows comment form if user logged in
- `{{ user }}` object available in all templates (from auth context processor)

Secrets and `.env` (short)

- Put `SECRET_KEY` in a `.env` file at the project root (same dir as `manage.py`):

```text
SECRET_KEY=<your-secret-key>
```

- `personal_blog/settings.py` should call `load_dotenv()` (from `python-dotenv`) before using `os.getenv('SECRET_KEY')`.
- Add `.env` to `.gitignore` to avoid pushing secrets.