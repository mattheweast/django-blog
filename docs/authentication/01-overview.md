# Overview: How Django Authentication Works

## The Big Picture

Django includes a complete authentication system out of the box. You don't need to build user registration, login, or password management from scratch.

## What Django Provides

### 1. User Model
```python
from django.contrib.auth.models import User
```
A ready-to-use model with:
- `username` - Unique identifier
- `password` - Automatically hashed (never plain text)
- `email` - Optional
- `first_name`, `last_name` - Optional
- `is_staff` - Can access admin panel?
- `is_superuser` - Has all permissions?
- `is_active` - Account enabled?
- `date_joined` - Timestamp of account creation

### 2. Built-in Views
Django provides views for:
- Login (`LoginView`)
- Logout (`LogoutView`)
- Password change
- Password reset (with email)

**You just wire them up to URLs** - no need to write the views yourself!

### 3. Forms
- `AuthenticationForm` - Login form (username + password)
- `UserCreationForm` - Registration form (username + password + password confirmation)
- `PasswordChangeForm` - Change password
- `PasswordResetForm` - Request password reset

### 4. Security Features
- **Password hashing** - Uses PBKDF2-SHA256 by default
- **CSRF protection** - Prevents cross-site request forgery
- **Session management** - Secure cookie-based sessions
- **SQL injection prevention** - ORM handles escaping

### 5. Middleware & Context Processors

**Middleware (runs on every request):**
- `SessionMiddleware` - Handles session cookies
- `AuthenticationMiddleware` - Makes `request.user` available

**Context Processor:**
- `auth` - Makes `{{ user }}` available in all templates automatically

## How Authentication Works

### The Session Cookie Flow

```
1. User submits login form
   ↓
2. Django validates username/password
   ↓
3. Creates session in database
   ↓
4. Sends session cookie to browser (sessionid=abc123)
   ↓
5. Browser includes cookie in all future requests
   ↓
6. Django reads cookie, looks up session, attaches user to request
```

### In Code

**Login Process:**
```python
from django.contrib.auth import authenticate, login

# Check credentials
user = authenticate(request, username='alice', password='secret')
if user is not None:
    # Create session
    login(request, user)
    # Browser now has session cookie
```

**On Future Requests:**
```python
# This happens automatically via middleware
def my_view(request):
    if request.user.is_authenticated:
        print(f"Logged in as: {request.user.username}")
    else:
        print("Anonymous user")
```

## What We Implemented

### 1. URL Configuration
Wired up Django's built-in auth views to URLs like `/accounts/login/`

### 2. Custom Registration
Created a custom view using Django's `UserCreationForm` because registration isn't built-in

### 3. Protected Comments
Only authenticated users can post comments, which are linked to their User account

### 4. UI Updates
Added navigation links showing login status and conditional form display

### 5. Database Changes
Added `user` ForeignKey to Comment model to link comments to accounts

## Key Concepts

### Authentication vs Authorization

**Authentication** - "Who are you?"
- Login/logout
- User identification
- Session management

**Authorization** - "What can you do?"
- Permissions
- User roles (staff, superuser)
- Access control

This blog currently uses authentication. Authorization could be added to control who can create/edit posts.

### request.user Object

This is available in every view:

```python
def my_view(request):
    # Always exists (never raises error)
    user = request.user
    
    # Check if logged in
    if user.is_authenticated:
        # Logged in - has username, email, etc.
        print(user.username)
    else:
        # Anonymous - instance of AnonymousUser
        print("Not logged in")
```

### Template Context

In templates, `{{ user }}` is automatically available:

```django
{% if user.is_authenticated %}
    Welcome, {{ user.username }}!
{% else %}
    Please login
{% endif %}
```

## Security By Default

Django automatically provides:

1. **Password Hashing** - Never stores passwords as plain text
2. **CSRF Tokens** - Every POST form requires `{% csrf_token %}`
3. **Session Security** - Random session IDs, expiration handling
4. **SQL Injection Prevention** - ORM escapes all queries
5. **XSS Protection** - Template engine escapes HTML by default

## Next Steps

Read the other documentation files to understand:
- How URLs are configured ([02-url-configuration.md](02-url-configuration.md))
- What settings are needed ([03-settings.md](03-settings.md))
- How models are structured ([04-models.md](04-models.md))
- How views handle authentication ([05-views.md](05-views.md))
- How templates check auth status ([06-templates.md](06-templates.md))
