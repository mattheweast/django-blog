# Settings & Configuration

## Location
`personal_blog/settings.py`

## Essential Authentication Settings

### 1. Installed Apps

```python
INSTALLED_APPS = [
    'django.contrib.admin',      # Admin interface
    'django.contrib.auth',       # ← Authentication system
    'django.contrib.contenttypes',
    'django.contrib.sessions',   # ← Session management
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig'
]
```

**What they do:**

**`django.contrib.auth`**
- Provides User model
- Password hashing
- Permission system
- Authentication backends

**`django.contrib.sessions`**
- Stores session data in database
- Manages session cookies
- Handles session expiration

### 2. Middleware

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',    # ← Sessions
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', # ← Auth
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

**Execution order matters!**

**`SessionMiddleware`** (line 2)
- Reads session cookie from request
- Loads session data from database
- Must run before AuthenticationMiddleware

**`AuthenticationMiddleware`** (line 5)
- Reads user_id from session
- Queries User model
- Attaches `request.user` to every request
- Requires SessionMiddleware to run first

**How they work together:**
```
Request arrives with cookie: sessionid=abc123
    ↓
SessionMiddleware: Finds session with key=abc123
    ↓
Session data: {"user_id": 5}
    ↓
AuthenticationMiddleware: Queries User where id=5
    ↓
Attaches User object to request.user
    ↓
View receives request with request.user populated
```

### 3. Template Context Processors

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'personal_blog/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',  # ← This one!
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

**What `auth` context processor does:**

Makes these variables available in **every template**:
- `{{ user }}` - Current user (or AnonymousUser)
- `{{ perms }}` - User's permissions

**Without it:**
```python
# You'd have to do this in EVERY view:
def my_view(request):
    context = {'user': request.user}
    return render(request, 'template.html', context)
```

**With it:**
```python
# It's automatic!
def my_view(request):
    return render(request, 'template.html', {})
    # {{ user }} still available in template
```

### 4. Redirect URLs

```python
# Authentication redirects
LOGIN_REDIRECT_URL = '/'   # After successful login
LOGOUT_REDIRECT_URL = '/'  # After logout
```

**Why these are needed:**

**DEFAULT behavior:**
```python
# Django's defaults
LOGIN_REDIRECT_URL = '/accounts/profile/'  # Doesn't exist!
LOGOUT_REDIRECT_URL = None  # Uses logged_out.html template
```

**Our configuration:**
```python
# Redirect to homepage instead
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
```

**Can be overridden by `?next=` parameter:**
```
/accounts/login/?next=/post/5/
```
Will redirect to `/post/5/` instead of `LOGIN_REDIRECT_URL`

### 5. Password Validators (Already Configured)

```python
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

**What each validator checks:**

1. **UserAttributeSimilarityValidator**
   - Prevents password too similar to username/email
   - Example: Username "alice" → Password "alice123" ❌

2. **MinimumLengthValidator**
   - Default: 8 characters minimum
   - Example: "pass" ❌, "password123" ✅

3. **CommonPasswordValidator**
   - Checks against list of 20,000 common passwords
   - Example: "password" ❌, "tr0ub4dor&3" ✅

4. **NumericPasswordValidator**
   - Prevents all-numeric passwords
   - Example: "12345678" ❌

## Optional Settings (Not Configured Yet)

### Session Settings

```python
# How long sessions last (default: 2 weeks)
SESSION_COOKIE_AGE = 1209600  # seconds

# Delete session when browser closes?
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# HTTPS only? (set True in production)
SESSION_COOKIE_SECURE = False

# Prevent JavaScript access to session cookie
SESSION_COOKIE_HTTPONLY = True
```

### Password Hashing

```python
# Default hasher (already configured)
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',  # Default
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]
```

**PBKDF2-SHA256** is Django's default - very secure!

### Login URL

```python
# Where to redirect for @login_required decorator
LOGIN_URL = '/accounts/login/'  # Default
```

When using `@login_required`, unauthenticated users redirect here.

## Settings Checklist

**For authentication to work, you need:**

- ✅ `django.contrib.auth` in INSTALLED_APPS
- ✅ `django.contrib.sessions` in INSTALLED_APPS
- ✅ `SessionMiddleware` in MIDDLEWARE
- ✅ `AuthenticationMiddleware` in MIDDLEWARE (after SessionMiddleware)
- ✅ `auth` context processor in TEMPLATES
- ✅ `LOGIN_REDIRECT_URL` set (or use default)
- ✅ `LOGOUT_REDIRECT_URL` set (optional)

**Already included by default:**
- ✅ Password validators
- ✅ Session database table
- ✅ Password hashers

## Database Tables

When you run `python manage.py migrate`, these tables are created:

```
auth_user                 # User accounts
auth_group                # Permission groups
auth_permission           # Individual permissions
django_session            # Session data
```

**Session table structure:**
```
session_key | session_data                    | expire_date
abc123      | {"user_id": 5, "_auth_..."}    | 2026-02-21 10:00:00
```

## Environment Variables

For production, use environment variables:

```python
# .env file
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

```python
# settings.py
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
```

## Summary

- Authentication requires specific apps, middleware, and context processors
- Middleware order matters (SessionMiddleware before AuthenticationMiddleware)
- Context processor makes `{{ user }}` available everywhere
- Redirect URLs control where users go after login/logout
- Password validators enforce security automatically
- Most settings have sensible defaults
