# Templates: Rendering HTML

## Location
`blog/templates/`

## Template Hierarchy

```
personal_blog/templates/
    base.html                  # Master layout
blog/templates/
    blog_index.html           # Homepage (extends base)
    blog_detail.html          # Post detail (extends base)
    blog_category.html        # Category filter (extends base)
```

## 1. base.html - Master Template

**Location:** `personal_blog/templates/base.html`

```django
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My Blog{% endblock %}</title>
    <link rel="stylesheet" href="https://cdn.simplecss.org/simple.min.css">
</head>
<body>
    <header>
        <nav>
            <a href="/">Home</a>
            {% if user.is_authenticated %}
                <span>Welcome, {{ user.username }}!</span>
                <a href="{% url 'logout' %}">Logout</a>
            {% else %}
                <a href="{% url 'login' %}">Login</a>
                <a href="{% url 'register' %}">Register</a>
            {% endif %}
        </nav>
    </header>
    
    <main>
        {% block content %}
        {% endblock %}
    </main>
</body>
</html>
```

**Key concepts:**

### {% block %} Tags

```django
{% block title %}My Blog{% endblock %}
{% block content %}{% endblock %}
```

**Purpose:** Define sections child templates can override

**How it works:**
1. Parent defines block with default content
2. Child template overrides block
3. Django replaces block content

**Example:**
```django
{# base.html #}
<title>{% block title %}Default Title{% endblock %}</title>

{# blog_index.html #}
{% block title %}Homepage{% endblock %}

{# Result: #}
<title>Homepage</title>
```

### Conditional Rendering

```django
{% if user.is_authenticated %}
    <span>Welcome, {{ user.username }}!</span>
{% else %}
    <a href="{% url 'login' %}">Login</a>
{% endif %}
```

**Logic:**
- If user logged in → Show welcome + logout
- If not → Show login + register links

**Variables:**
- `user` - Available in all templates via context processor
- `user.is_authenticated` - Boolean property
- `user.username` - Logged-in username

### {% url %} Tag

```django
<a href="{% url 'login' %}">Login</a>
<a href="{% url 'logout' %}">Logout</a>
```

**Purpose:** Generate URLs from route names (reverse lookup)

**Why not hardcode?**
```django
{# Bad - hardcoded #}
<a href="/accounts/login/">Login</a>

{# Good - dynamic #}
<a href="{% url 'login' %}">Login</a>
```

**Benefits:**
- Change URL in one place (urls.py)
- Links update automatically
- No broken links

**With parameters:**
```django
{% url 'blog_detail' pk=5 %}  {# /blog/5/ #}
{% url 'blog_category' category='Python' %}  {# /blog/category/Python/ #}
```

### Simple.css

```html
<link rel="stylesheet" href="https://cdn.simplecss.org/simple.min.css">
```

**Purpose:** Classless CSS framework

**Features:**
- No CSS classes needed
- Automatic styling for HTML elements
- Responsive design
- Clean, modern look

**Example:**
```html
<button>Click me</button>  <!-- Automatically styled -->
<form>...</form>           <!-- Automatically styled -->
```

## 2. blog_index.html - Homepage

```django
{% extends "base.html" %}

{% block title %}Blog Index{% endblock %}

{% block content %}
    <h1>Welcome to My Blog</h1>
    
    {% for post in posts %}
        <article>
            <h2><a href="{% url 'blog_detail' pk=post.pk %}">{{ post.title }}</a></h2>
            <p><small>Posted on {{ post.created_on|date:"F d, Y" }}</small></p>
            
            <p>
                {% for category in post.categories.all %}
                    <a href="{% url 'blog_category' category=category.name %}">{{ category.name }}</a>
                {% endfor %}
            </p>
            
            <p>{{ post.body|slice:":400" }}...</p>
        </article>
    {% endfor %}
{% endblock %}
```

**Key concepts:**

### {% extends %}

```django
{% extends "base.html" %}
```

**Purpose:** Inherit from parent template

**Must be first line in template**

**How it works:**
1. Load base.html structure
2. Fill in blocks from child
3. Keep everything else from parent

### {% for %} Loop

```django
{% for post in posts %}
    <h2>{{ post.title }}</h2>
{% endfor %}
```

**Purpose:** Iterate over QuerySet or list

**Context variable:**
- `posts` - Passed from view: `context = {"posts": posts}`

**Equivalent Python:**
```python
for post in posts:
    print(post.title)
```

**Empty handling:**
```django
{% for post in posts %}
    <h2>{{ post.title }}</h2>
{% empty %}
    <p>No posts yet.</p>
{% endfor %}
```

### {{ variable }} - Variable Output

```django
{{ post.title }}
{{ post.created_on }}
{{ post.body }}
```

**Purpose:** Output variable value

**Rules:**
- Auto-escapes HTML (prevents XSS attacks)
- Calls `__str__()` method if available
- Dot notation for attributes/methods

**Examples:**
```django
{{ post.title }}                    {# Field value #}
{{ post.categories.all }}           {# Related objects #}
{{ post.categories.all.count }}     {# Method call #}
{{ user.username }}                 {# User attribute #}
```

### | Filters

```django
{{ post.created_on|date:"F d, Y" }}
{{ post.body|slice:":400" }}
```

**Purpose:** Transform variable output

#### date Filter

```django
{{ post.created_on|date:"F d, Y" }}
```

**Example:** `January 15, 2024`

**Format codes:**
- `F` - Full month name
- `d` - Day with leading zero
- `Y` - 4-digit year
- `M` - Short month (Jan)
- `y` - 2-digit year (24)
- `H:i` - Hour:minute (14:30)

**More examples:**
```django
{{ post.created_on|date:"M d, Y" }}      {# Jan 15, 2024 #}
{{ post.created_on|date:"Y-m-d" }}       {# 2024-01-15 #}
{{ post.created_on|date:"F j, Y g:i A" }}{# January 15, 2024 2:30 PM #}
```

#### slice Filter

```django
{{ post.body|slice:":400" }}
```

**Purpose:** Get first 400 characters

**Syntax:** `start:end` (Python slicing)

**Examples:**
```django
{{ post.body|slice:":100" }}     {# First 100 chars #}
{{ post.body|slice:"10:20" }}    {# Chars 10-20 #}
{{ post.body|slice:":-100" }}    {# All except last 100 #}
```

#### Common Filters

```django
{{ text|lower }}           {# lowercase #}
{{ text|upper }}           {# UPPERCASE #}
{{ text|title }}           {# Title Case #}
{{ text|length }}          {# String length #}
{{ text|truncatewords:50 }}{# First 50 words #}
{{ html|safe }}            {# Don't escape HTML #}
{{ value|default:"N/A" }}  {# Default if empty #}
{{ list|join:", " }}       {# Join list items #}
```

### Nested {% for %}

```django
{% for category in post.categories.all %}
    <a href="{% url 'blog_category' category=category.name %}">{{ category.name }}</a>
{% endfor %}
```

**Purpose:** Loop through related objects

**post.categories.all:**
- ManyToMany relationship
- Returns QuerySet of Category objects
- Executed for each post

**Example output:**
```html
<a href="/blog/category/Python/">Python</a>
<a href="/blog/category/Django/">Django</a>
<a href="/blog/category/Tutorial/">Tutorial</a>
```

## 3. blog_detail.html - Post Detail

```django
{% extends "base.html" %}

{% block title %}{{ post.title }}{% endblock %}

{% block content %}
    <article>
        <h1>{{ post.title }}</h1>
        <p><small>Posted on {{ post.created_on|date:"F d, Y" }}</small></p>
        
        <p>
            {% for category in post.categories.all %}
                <a href="{% url 'blog_category' category=category.name %}">{{ category.name }}</a>
            {% endfor %}
        </p>
        
        <div>
            {{ post.body|linebreaks }}
        </div>
    </article>
    
    <h3>Comments</h3>
    {% for comment in comments %}
        <div>
            <p><strong>
                {% if comment.user %}
                    {{ comment.user.username }}
                {% else %}
                    {{ comment.author }}
                {% endif %}
            </strong> - {{ comment.created_on|date:"M d, Y" }}</p>
            <p>{{ comment.body|linebreaks }}</p>
        </div>
    {% empty %}
        <p>No comments yet. Be the first!</p>
    {% endfor %}
    
    <h3>Leave a Comment</h3>
    {% if user.is_authenticated %}
        <form method="POST">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit">Submit</button>
        </form>
    {% else %}
        <p><a href="{% url 'login' %}?next={{ request.path }}">Login to leave a comment</a></p>
    {% endif %}
{% endblock %}
```

**Key concepts:**

### linebreaks Filter

```django
{{ post.body|linebreaks }}
```

**Purpose:** Convert text to HTML paragraphs

**Example:**
```
Input:
"This is line 1.

This is line 2."

Output:
<p>This is line 1.</p>
<p>This is line 2.</p>
```

**Alternatives:**
```django
{{ text|linebreaksbr }}  {# Converts newlines to <br> #}
```

### Conditional User Display

```django
{% if comment.user %}
    {{ comment.user.username }}
{% else %}
    {{ comment.author }}
{% endif %}
```

**Logic:**
- New comments have `user` (authenticated)
- Old comments have `author` (legacy field)
- Display whichever exists

### {% empty %} Tag

```django
{% for comment in comments %}
    <p>{{ comment.body }}</p>
{% empty %}
    <p>No comments yet.</p>
{% endfor %}
```

**Purpose:** Handle empty QuerySets

**Equivalent:**
```django
{% if comments %}
    {% for comment in comments %}
        <p>{{ comment.body }}</p>
    {% endfor %}
{% else %}
    <p>No comments yet.</p>
{% endif %}
```

### {% csrf_token %}

```django
<form method="POST">
    {% csrf_token %}
    ...
</form>
```

**Purpose:** Cross-Site Request Forgery protection

**Required for all POST forms**

**Generates:**
```html
<input type="hidden" name="csrfmiddlewaretoken" value="abc123...">
```

**How it works:**
1. Django generates token for session
2. Token embedded in form
3. Server validates token on submission
4. Reject if missing or invalid

**Error if missing:**
```
Forbidden (403)
CSRF verification failed
```

### {{ form.as_p }}

```django
{{ form.as_p }}
```

**Purpose:** Render form fields wrapped in `<p>` tags

**Example output:**
```html
<p>
    <label for="id_body">Body:</label>
    <textarea name="body" id="id_body" required></textarea>
</p>
```

**Alternatives:**
```django
{{ form.as_table }}  {# Table rows #}
{{ form.as_ul }}     {# List items #}
```

**Manual field rendering:**
```django
{{ form.body.label_tag }}
{{ form.body }}
{{ form.body.errors }}
```

### ?next= Parameter

```django
<a href="{% url 'login' %}?next={{ request.path }}">Login</a>
```

**Purpose:** Redirect back after login

**Example:** User at `/blog/5/`
- Click login link → `/accounts/login/?next=/blog/5/`
- Login successful → Redirect to `/blog/5/`

**request.path:**
- Current URL path
- Available in all templates
- Example: `/blog/5/`

## 4. blog_category.html - Category Filter

```django
{% extends "base.html" %}

{% block title %}{{ category }} Posts{% endblock %}

{% block content %}
    <h1>Posts in "{{ category }}"</h1>
    
    {% for post in posts %}
        <article>
            <h2><a href="{% url 'blog_detail' pk=post.pk %}">{{ post.title }}</a></h2>
            <p><small>Posted on {{ post.created_on|date:"F d, Y" }}</small></p>
            <p>{{ post.body|slice:":200" }}...</p>
        </article>
    {% empty %}
        <p>No posts in this category yet.</p>
    {% endfor %}
{% endblock %}
```

**Similar to blog_index.html but:**
- Shows category name in title
- Filters posts by category (done in view)
- Handles empty category gracefully

## Template Language Summary

### Tags (Logic)

```django
{% extends "parent.html" %}      {# Inherit template #}
{% block name %}...{% endblock %} {# Define/override section #}
{% if condition %}...{% endif %} {# Conditional #}
{% for item in list %}...{% endfor %} {# Loop #}
{% url 'name' arg=value %}       {# Generate URL #}
{% csrf_token %}                 {# CSRF protection #}
{% empty %}                      {# Empty for loop #}
{% comment %}...{% endcomment %} {# Multi-line comment #}
{# Single line comment #}
```

### Variables (Output)

```django
{{ variable }}                   {# Output value #}
{{ object.attribute }}           {# Attribute access #}
{{ object.method }}              {# Method call #}
{{ list.0 }}                     {# List index #}
```

### Filters (Transform)

```django
{{ text|lower }}                 {# Lowercase #}
{{ text|upper }}                 {# Uppercase #}
{{ text|title }}                 {# Title Case #}
{{ date|date:"Y-m-d" }}         {# Format date #}
{{ text|slice:":100" }}         {# Substring #}
{{ text|linebreaks }}           {# Text to <p> #}
{{ text|truncatewords:50 }}     {# First 50 words #}
{{ value|default:"N/A" }}       {# Default if empty #}
{{ html|safe }}                 {# Don't escape #}
{{ list|length }}               {# Count items #}
{{ list|join:", " }}            {# Join with comma #}
```

### Operators

```django
{% if a == b %}      {# Equal #}
{% if a != b %}      {# Not equal #}
{% if a < b %}       {# Less than #}
{% if a > b %}       {# Greater than #}
{% if a <= b %}      {# Less or equal #}
{% if a >= b %}      {# Greater or equal #}
{% if a and b %}     {# Both true #}
{% if a or b %}      {# Either true #}
{% if not a %}       {# False/empty #}
{% if a in list %}   {# Membership #}
```

## Context Variables

**Always available:**
```django
{{ user }}              {# Current user #}
{{ user.is_authenticated }} {# Login status #}
{{ user.username }}     {# Username if logged in #}
{{ request }}           {# Request object #}
{{ request.path }}      {# Current URL #}
{{ request.method }}    {# GET/POST #}
```

**From view context:**
```django
{# From context = {"posts": posts} #}
{{ posts }}

{# From context = {"post": post, "comments": comments} #}
{{ post.title }}
{{ comments|length }}
```

## Auto-escaping

**By default, HTML is escaped:**
```django
{{ user_input }}
{# <script>alert('xss')</script> #}
{# Becomes: &lt;script&gt;alert('xss')&lt;/script&gt; #}
```

**Disable escaping:**
```django
{{ trusted_html|safe }}
{# Use only with trusted content! #}
```

**In blocks:**
```django
{% autoescape off %}
    {{ html_content }}
{% endautoescape %}
```

## Template Loading

**Django searches for templates in:**
1. App directories: `blog/templates/`
2. Project directories: `personal_blog/templates/`
3. Settings TEMPLATES['DIRS']

**Best practice:**
```
app/templates/app/template.html  {# Namespaced #}
```

**Your structure:**
```
blog/templates/blog_index.html         {# Blog app templates #}
personal_blog/templates/base.html      {# Project-wide templates #}
```

## Summary

- **extends** - Inherit parent template
- **block** - Override section in child
- **for** - Loop over QuerySet/list
- **if** - Conditional rendering
- **{{ }}** - Output variables
- **{% %}** - Template tags
- **| filters** - Transform output
- **csrf_token** - Required for POST forms
- **url** - Generate URLs from names
- **Auto-escaping** - Security by default
- Templates loaded from app/project directories
- Context from views available as variables
