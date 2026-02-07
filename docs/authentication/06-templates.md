# Templates & UI

## Base Template Navigation

### Location
`personal_blog/templates/base.html`

### Implementation

```html
<header>
    <nav style="display: flex; justify-content: space-between;">
        <div>
            <a href="{% url 'blog_index' %}">Home</a>
        </div>
        <div>
            {% if user.is_authenticated %}
                <span>Welcome, <strong>{{ user.username }}</strong>!</span> | 
                <a href="{% url 'logout' %}">Logout</a>
            {% else %}
                <a href="{% url 'login' %}">Login</a> | 
                <a href="{% url 'register' %}">Register</a>
            {% endif %}
        </div>
    </nav>
</header>
```

### How {{ user }} is Available

**Context processor makes it automatic:**

```python
# settings.py
'context_processors': [
    'django.contrib.auth.context_processors.auth',  # This one!
]
```

**Without it, you'd need:**
```python
# In EVERY view
def my_view(request):
    context = {'user': request.user}
    return render(request, 'template.html', context)
```

**With it:**
```python
# Works automatically
def my_view(request):
    return render(request, 'template.html', {})
# {{ user }} still available!
```

### Conditional Display

```django
{% if user.is_authenticated %}
    <!-- Logged in content -->
{% else %}
    <!-- Not logged in content -->
{% endif %}
```

**What user object contains:**

**Logged in:**
```django
{{ user.username }}       <!-- "alice" -->
{{ user.email }}          <!-- "alice@example.com" -->
{{ user.is_staff }}       <!-- True/False -->
{{ user.date_joined }}    <!-- 2026-01-15 -->
{{ user.is_authenticated }}  <!-- True -->
```

**Anonymous:**
```django
{{ user.is_authenticated }}  <!-- False -->
{{ user.username }}       <!-- Empty string -->
```

## Login Template

### Location
`personal_blog/templates/registration/login.html`

### Implementation

```html
{% extends 'base.html' %}

{% block page_title %}Login{% endblock %}

{% block page_content %}
<h1>Login</h1>

<form method="post">
    {% csrf_token %}
    
    {% if form.errors %}
        <p style="color: red;">Username or password is incorrect.</p>
    {% endif %}
    
    {{ form.as_p }}
    
    <button type="submit">Login</button>
</form>

<p>Don't have an account? <a href="{% url 'register' %}">Register here</a></p>
{% endblock %}
```

### Template Tags Explained

**{% csrf_token %}**
```django
{% csrf_token %}
```
Renders:
```html
<input type="hidden" name="csrfmiddlewaretoken" value="abc123...xyz">
```

**Required for all POST forms**. Django checks this token to prevent CSRF attacks.

**{{ form.as_p }}**
```django
{{ form.as_p }}
```
Renders form fields wrapped in `<p>` tags:
```html
<p>
    <label for="id_username">Username:</label>
    <input type="text" name="username" id="id_username" required>
</p>
<p>
    <label for="id_password">Password:</label>
    <input type="password" name="password" id="id_password" required>
</p>
```

**Other options:**
- `{{ form.as_table }}` - Renders as table rows
- `{{ form.as_ul }}` - Renders as list items
- Manual rendering (see below)

**{% if form.errors %}**
```django
{% if form.errors %}
    <p style="color: red;">Username or password is incorrect.</p>
{% endif %}
```

Shows error message if login failed. Django's LoginView automatically populates `form.errors`.

**{% url 'register' %}**
```django
<a href="{% url 'register' %}">Register here</a>
```
Reverse URL lookup. Generates `/register/` based on URL pattern name.

**Benefits:**
- If URL changes, templates update automatically
- No hardcoded URLs

## Registration Template

### Location
`personal_blog/templates/registration/register.html`

### Implementation

```html
{% extends 'base.html' %}

{% block page_title %}Register{% endblock %}

{% block page_content %}
<h1>Create an Account</h1>

<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Sign Up</button>
</form>

<p>Already have an account? <a href="{% url 'login' %}">Login here</a></p>
{% endblock %}
```

### What UserCreationForm Renders

```html
<p>
    <label for="id_username">Username:</label>
    <input type="text" name="username" maxlength="150" required id="id_username">
    <span class="helptext">Required. 150 characters or fewer.</span>
</p>

<p>
    <label for="id_password1">Password:</label>
    <input type="password" name="password1" required id="id_password1">
    <span class="helptext">
        <ul>
            <li>Your password can't be too similar to your other personal information.</li>
            <li>Your password must contain at least 8 characters.</li>
            <li>Your password can't be a commonly used password.</li>
            <li>Your password can't be entirely numeric.</li>
        </ul>
    </span>
</p>

<p>
    <label for="id_password2">Password confirmation:</label>
    <input type="password" name="password2" required id="id_password2">
    <span class="helptext">Enter the same password as before, for verification.</span>
</p>
```

### Field Errors

If form validation fails:

```django
{{ form.as_p }}
```

Renders with error messages:

```html
<p>
    <ul class="errorlist">
        <li>A user with that username already exists.</li>
    </ul>
    <label for="id_username">Username:</label>
    <input type="text" name="username" value="alice" required id="id_username">
</p>
```

## Blog Detail Template (Comments)

### Location
`blog/templates/blog_detail.html`

### Implementation

```html
{% extends 'base.html' %}
{% block page_content %}
    <h1>{{ post.title }}</h1>
    <p>{{ post.body }}</p>
    <hr>
    
    <h3>Comments</h3>
    {% for comment in comments %}
        <p>
            <strong>
                {% if comment.user %}
                    {{ comment.user.username }}
                {% else %}
                    {{ comment.author }}
                {% endif %}
            </strong>: 
            {{ comment.body }}
        </p>
    {% empty %}
        <p>No comments yet.</p>
    {% endfor %}
    <hr>
    
    {% if user.is_authenticated %}
        <h3>Add Comment</h3>
        <form method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit">Submit</button>
        </form>
    {% else %}
        <p><a href="{% url 'login' %}?next={{ request.path }}">Login</a> to leave a comment.</p>
    {% endif %}
{% endblock %}
```

### Key Features

**Conditional author display:**
```django
{% if comment.user %}
    {{ comment.user.username }}
{% else %}
    {{ comment.author }}
{% endif %}
```
Shows username for new comments, legacy author for old comments.

**Empty state:**
```django
{% for comment in comments %}
    <!-- Comment display -->
{% empty %}
    <p>No comments yet.</p>
{% endfor %}
```
`{% empty %}` runs if `comments` list is empty.

**Conditional form:**
```django
{% if user.is_authenticated %}
    <!-- Show comment form -->
{% else %}
    <!-- Show login link -->
{% endif %}
```

**Login with redirect:**
```django
<a href="{% url 'login' %}?next={{ request.path }}">Login</a>
```

`?next={{ request.path }}` tells login view to return here after login.

**Example:**
- User on `/post/5/`
- Clicks login → `/accounts/login/?next=/post/5/`
- Logs in → Redirected to `/post/5/`

## Manual Form Rendering

Instead of `{{ form.as_p }}`, you can render fields manually:

```django
<form method="post">
    {% csrf_token %}
    
    <div class="form-group">
        {{ form.username.label_tag }}
        {{ form.username }}
        {% if form.username.errors %}
            <span class="error">{{ form.username.errors }}</span>
        {% endif %}
        <small>{{ form.username.help_text }}</small>
    </div>
    
    <div class="form-group">
        {{ form.password.label_tag }}
        {{ form.password }}
        {% if form.password.errors %}
            <span class="error">{{ form.password.errors }}</span>
        {% endif %}
    </div>
    
    <button type="submit">Login</button>
</form>
```

**Gives more control over:**
- HTML structure
- CSS classes
- Error display
- Field order

## Template Filters & Tags

### Useful Auth Filters

```django
{{ user.date_joined|date:"F j, Y" }}
<!-- February 7, 2026 -->

{{ user.username|title }}
<!-- Alice -->

{{ comment.created_on|timesince }} ago
<!-- 2 hours ago -->
```

### Custom Template Tags (Example)

```python
# blog/templatetags/auth_extras.py
from django import template

register = template.Library()

@register.filter
def user_comments_count(user):
    return user.comments.count()
```

```django
{% load auth_extras %}

{{ user|user_comments_count }} comments
```

## Static Files in Templates

```django
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```

**Currently using CDN:**
```html
<link rel="stylesheet" href="https://cdn.simplecss.org/simple.min.css" />
```

## Common Template Patterns

### Check staff status

```django
{% if user.is_staff %}
    <a href="{% url 'admin:index' %}">Admin Panel</a>
{% endif %}
```

### Show login time

```django
{% if user.is_authenticated %}
    Last login: {{ user.last_login|date:"M d, Y H:i" }}
{% endif %}
```

### User profile link

```django
{% if user.is_authenticated %}
    <a href="{% url 'profile' user.username %}">My Profile</a>
{% endif %}
```

### Count user's content

```django
{% if user.is_authenticated %}
    You have {{ user.comments.count }} comments
{% endif %}
```

## Template Inheritance

### Base template structure

```django
<!-- base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block page_title %}My Blog{% endblock %}</title>
</head>
<body>
    <header><!-- Navigation --></header>
    
    {% block page_content %}{% endblock %}
    
    <footer><!-- Footer --></footer>
</body>
</html>
```

### Child template

```django
<!-- login.html -->
{% extends 'base.html' %}

{% block page_title %}Login{% endblock %}

{% block page_content %}
    <h1>Login</h1>
    <!-- Form here -->
{% endblock %}
```

## Messages Framework (Not implemented yet)

Django can show one-time messages:

```python
# views.py
from django.contrib import messages

def register(request):
    # ...
    if form.is_valid():
        user = form.save()
        messages.success(request, f'Welcome, {user.username}!')
        return redirect('blog_index')
```

```django
<!-- base.html -->
{% if messages %}
    {% for message in messages %}
        <div class="alert alert-{{ message.tags }}">
            {{ message }}
        </div>
    {% endfor %}
{% endif %}
```

## Summary

- `{{ user }}` automatically available via context processor
- `{% csrf_token %}` required for all POST forms
- `{{ form.as_p }}` renders form fields automatically
- Templates can check authentication and permissions
- `{% url %}` tag generates URLs from pattern names
- `?next=` parameter controls post-login redirect
- Template inheritance keeps code DRY
- Forms include validation errors and help text
