# URL Configuration

## Location
`personal_blog/urls.py`

## The Configuration

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Built-in auth views
    path('', include('blog.urls'))  # Blog app URLs
]
```

## What `include('django.contrib.auth.urls')` Gives You

This single line provides **8 URLs for free**:

### 1. Login & Logout
```
/accounts/login/          → LoginView
/accounts/logout/         → LogoutView
```

### 2. Password Change (for logged-in users)
```
/accounts/password_change/       → PasswordChangeView
/accounts/password_change/done/  → PasswordChangeDoneView
```

### 3. Password Reset (for forgotten passwords)
```
/accounts/password_reset/          → PasswordResetView
/accounts/password_reset/done/     → PasswordResetDoneView
/accounts/reset/<uidb64>/<token>/  → PasswordResetConfirmView
/accounts/reset/done/              → PasswordResetCompleteView
```

## How It Works

### Built-in View Classes

Django provides these class-based views:

```python
# You don't write this - Django provides it!
class LoginView(FormView):
    template_name = 'registration/login.html'
    form_class = AuthenticationForm
    
    def form_valid(self, form):
        # Authenticate user
        # Create session
        # Redirect to LOGIN_REDIRECT_URL
```

### Template Lookup

Each view looks for a specific template:

| View | Template Path |
|------|--------------|
| LoginView | `registration/login.html` |
| LogoutView | `registration/logged_out.html` |
| PasswordChangeView | `registration/password_change_form.html` |
| PasswordResetView | `registration/password_reset_form.html` |

**That's why we created:** `personal_blog/templates/registration/login.html`

## Custom Registration URL

Registration is NOT built-in, so we added a custom URL:

**In `blog/urls.py`:**
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_index, name='blog_index'),
    path('post/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('category/<str:category>/', views.blog_category, name='blog_category'),
    path('register/', views.register, name='register'),  # Custom view
]
```

## URL Naming

Each URL has a `name` parameter for reverse lookup:

```python
# In views
return redirect('login')  # Goes to /accounts/login/

# In templates
<a href="{% url 'login' %}">Login</a>  <!-- Links to /accounts/login/ -->
<a href="{% url 'register' %}">Register</a>  <!-- Links to /register/ -->
```

## Request Flow Example

### User visits `/accounts/login/`

```
Browser GET /accounts/login/
    ↓
personal_blog/urls.py receives request
    ↓
Matches: path('accounts/', include('django.contrib.auth.urls'))
    ↓
Django's auth URLs take over
    ↓
Matches: login/ → LoginView
    ↓
LoginView renders 'registration/login.html'
    ↓
Response sent to browser
```

### User submits login form

```
Browser POST /accounts/login/
    ↓
LoginView receives POST data
    ↓
Validates username/password
    ↓
If valid: creates session, redirects to LOGIN_REDIRECT_URL
If invalid: re-renders form with errors
```

## Why Use include()?

The `include()` function allows you to plug in entire URL configurations:

```python
path('accounts/', include('django.contrib.auth.urls'))
```

**Expands to:**
```python
path('accounts/login/', LoginView.as_view(), name='login'),
path('accounts/logout/', LogoutView.as_view(), name='logout'),
# ... 6 more URLs
```

**Benefits:**
- Keeps your main `urls.py` clean
- Modular - can include different apps
- Reusable - Django's auth URLs work in any project

## URL Parameters

### The ?next= Parameter

Login/logout views support a `next` parameter:

```
/accounts/login/?next=/post/5/
```

**What it does:**
After successful login, redirect to the `next` URL instead of `LOGIN_REDIRECT_URL`

**Usage in templates:**
```django
<a href="{% url 'login' %}?next={{ request.path }}">Login</a>
```

**Example:**
1. User on `/post/5/` (not logged in)
2. Clicks "Login" → Goes to `/accounts/login/?next=/post/5/`
3. Logs in successfully
4. Redirected back to `/post/5/`

## Common Patterns

### Protecting URLs (not implemented yet)

You can require login for specific URLs:

```python
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('profile/', login_required(views.profile), name='profile'),
]
```

Or in the view:

```python
@login_required
def profile(request):
    return render(request, 'profile.html')
```

If user not logged in → redirects to `/accounts/login/?next=/profile/`

## Summary

- **One line** gives you 8 authentication URLs
- Views are provided by Django
- You only need to create templates
- Registration requires a custom view (not built-in)
- Use `name` parameter for reverse URL lookup
- `?next=` parameter controls post-login redirect
