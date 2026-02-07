# URL Configuration: Routing Requests

## How URL Routing Works

**Flow:** Browser request → Django URLconf → View function → Response

```
User visits: /blog/5/
    ↓
Django checks: blog/urls.py
    ↓
Finds match: path("blog/<int:pk>/", views.blog_detail, name="blog_detail")
    ↓
Calls: views.blog_detail(request, pk=5)
    ↓
Returns: HTTP response
```

## Two-Level URL Configuration

### 1. Project URLs (Root)

**Location:** `personal_blog/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
]
```

**Line-by-line:**

**path("admin/", admin.site.urls)**
- Routes `/admin/` to Django admin site
- Built-in admin interface
- Example: `http://localhost:8000/admin/`

**path("", include("blog.urls"))**
- Routes root URL to blog app URLs
- `""` means root level (no prefix)
- `include()` delegates to `blog/urls.py`
- All blog URLs start from `/`

**path("accounts/", include("django.contrib.auth.urls"))**
- Routes `/accounts/` to authentication URLs
- Provides 8 built-in auth views
- Examples: `/accounts/login/`, `/accounts/logout/`

### 2. App URLs (Blog)

**Location:** `blog/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.blog_index, name="blog_index"),
    path("blog/<int:pk>/", views.blog_detail, name="blog_detail"),
    path("blog/category/<str:category>/", views.blog_category, name="blog_category"),
    path("register/", views.register, name="register"),
]
```

**Each path() has 3 parts:**
1. **Route pattern** - URL to match
2. **View function** - Function to call
3. **Name** - Identifier for reverse lookup

## URL Patterns Explained

### Pattern 1: Empty String

```python
path("", views.blog_index, name="blog_index")
```

**Matches:** `/` (homepage)

**Why empty?**
- Included at root level in `personal_blog/urls.py`
- `include("blog.urls")` with `""` prefix
- So `""` in blog/urls.py = `/` in browser

**Example:**
```
Project URLs: path("", include("blog.urls"))
Blog URLs:    path("", views.blog_index)
Result:       / → blog_index()
```

**If prefix was different:**
```
Project URLs: path("myblog/", include("blog.urls"))
Blog URLs:    path("", views.blog_index)
Result:       /myblog/ → blog_index()
```

### Pattern 2: Integer Parameter

```python
path("blog/<int:pk>/", views.blog_detail, name="blog_detail")
```

**Matches:** `/blog/1/`, `/blog/5/`, `/blog/999/`

**Does NOT match:** `/blog/abc/`, `/blog/1.5/`

**<int:pk> breakdown:**
- **< >** - Capture URL segment as variable
- **int:** - Type converter (integer only)
- **pk** - Variable name passed to view

**How it works:**
```
URL:  /blog/5/
Match: blog/<int:pk>/
Capture: pk=5
Call: views.blog_detail(request, pk=5)
```

**In view:**
```python
def blog_detail(request, pk):
    # pk is now 5 (integer)
    post = Post.objects.get(pk=pk)
```

### Pattern 3: String Parameter

```python
path("blog/category/<str:category>/", views.blog_category, name="blog_category")
```

**Matches:** `/blog/category/Python/`, `/blog/category/Django/`

**<str:category> breakdown:**
- **< >** - Capture URL segment
- **str:** - Type converter (any text)
- **category** - Variable name

**How it works:**
```
URL:  /blog/category/Python/
Match: blog/category/<str:category>/
Capture: category="Python"
Call: views.blog_category(request, category="Python")
```

**In view:**
```python
def blog_category(request, category):
    # category is now "Python" (string)
    posts = Post.objects.filter(categories__name__contains=category)
```

### Pattern 4: Simple Path

```python
path("register/", views.register, name="register")
```

**Matches:** `/register/` (exact match)

**No parameters captured**

**Call:** `views.register(request)`

## Path Converters

**Available types:**

```python
<str:name>   # Any text (default)
<int:id>     # Integer (positive or negative)
<slug:slug>  # Slug (letters, numbers, - , _)
<uuid:uuid>  # UUID (e.g., 550e8400-e29b-41d4-a716-446655440000)
<path:path>  # Any text including slashes
```

**Examples:**

```python
path("post/<int:year>/<int:month>/", views.archive)
# /post/2024/1/ → archive(request, year=2024, month=1)

path("page/<slug:slug>/", views.page)
# /page/about-us/ → page(request, slug="about-us")

path("file/<path:filepath>/", views.download)
# /file/docs/report.pdf → download(request, filepath="docs/report.pdf")
```

## URL Names (Reverse Lookup)

### Why Name URLs?

**Bad approach (hardcoded):**
```django
<a href="/blog/5/">View Post</a>
```

**Problems:**
- Change URL pattern → All links break
- Can't have multiple URL patterns for same view
- Hard to maintain

**Good approach (named):**
```django
<a href="{% url 'blog_detail' pk=5 %}">View Post</a>
```

**Benefits:**
- Change URL in one place (urls.py)
- Django generates URL for you
- Links never break

### Using URL Names

**In templates:**
```django
{# No parameters #}
<a href="{% url 'blog_index' %}">Home</a>
{# Result: / #}

{# With parameters #}
<a href="{% url 'blog_detail' pk=post.pk %}">{{ post.title }}</a>
{# Result: /blog/5/ #}

<a href="{% url 'blog_category' category='Python' %}">Python Posts</a>
{# Result: /blog/category/Python/ #}
```

**In views (redirect):**
```python
from django.urls import reverse
from django.shortcuts import redirect

# Using reverse()
url = reverse('blog_detail', kwargs={'pk': 5})
# Returns: '/blog/5/'

# In redirect
return redirect('blog_detail', pk=5)
# Redirects to: /blog/5/

# Using HttpResponseRedirect
from django.http import HttpResponseRedirect
return HttpResponseRedirect(reverse('blog_detail', kwargs={'pk': 5}))
```

## Complete Request Example

### Example 1: Homepage

**User types:** `http://localhost:8000/`

**Django process:**
1. Check `personal_blog/urls.py`:
   - `path("", include("blog.urls"))` → Matches, check blog/urls.py
2. Check `blog/urls.py`:
   - `path("", views.blog_index, name="blog_index")` → Matches!
3. Call `views.blog_index(request)`
4. View queries posts, renders template
5. Return HTML response

### Example 2: Post Detail

**User types:** `http://localhost:8000/blog/5/`

**Django process:**
1. Check `personal_blog/urls.py`:
   - `path("", include("blog.urls"))` → Matches, check blog/urls.py
2. Check `blog/urls.py`:
   - `path("", ...)` → No (empty != "blog/5/")
   - `path("blog/<int:pk>/", ...)` → Matches! (pk=5)
3. Call `views.blog_detail(request, pk=5)`
4. View gets post 5, renders template
5. Return HTML response

### Example 3: Category

**User types:** `http://localhost:8000/blog/category/Python/`

**Django process:**
1. Check `personal_blog/urls.py`:
   - `path("", include("blog.urls"))` → Matches, check blog/urls.py
2. Check `blog/urls.py`:
   - First two patterns don't match
   - `path("blog/category/<str:category>/", ...)` → Matches! (category="Python")
3. Call `views.blog_category(request, category="Python")`
4. View filters posts, renders template
5. Return HTML response

### Example 4: Login

**User types:** `http://localhost:8000/accounts/login/`

**Django process:**
1. Check `personal_blog/urls.py`:
   - `path("accounts/", include("django.contrib.auth.urls"))` → Matches!
2. Check Django auth URLs:
   - `path("login/", LoginView.as_view(), name="login")` → Matches!
3. Call Django's LoginView
4. Renders `registration/login.html`
5. Return HTML response

## URL Order Matters

**Django checks patterns top-to-bottom, first match wins**

**Example problem:**
```python
urlpatterns = [
    path("blog/<str:slug>/", views.post_by_slug),
    path("blog/new/", views.new_post),  # NEVER REACHED!
]
```

**Why?**
- `/blog/new/` matches first pattern (`slug="new"`)
- Second pattern never checked

**Solution:**
```python
urlpatterns = [
    path("blog/new/", views.new_post),      # Check specific first
    path("blog/<str:slug>/", views.post_by_slug),  # Then generic
]
```

**Rule:** Specific patterns before generic patterns

## Include() Explained

**Purpose:** Delegate URL routing to another module

**Example:**
```python
# personal_blog/urls.py
urlpatterns = [
    path("blog/", include("blog.urls")),
    path("comments/", include("comments.urls")),
]
```

**How it works:**
1. User visits `/blog/post/5/`
2. Django matches `path("blog/", ...)`
3. Strips `blog/` from path → `post/5/`
4. Checks `blog/urls.py` for `post/5/`
5. Finds match: `path("post/<int:pk>/", ...)`

**Benefits:**
- Organize URLs by app
- Reusable apps
- Cleaner structure

## URL Parameters vs Query Strings

### URL Parameters (Path)

```python
path("blog/<int:pk>/", views.blog_detail)
```

**URL:** `/blog/5/`

**Access:** `views.blog_detail(request, pk=5)`

**Use for:** Resource identification (posts, users, etc.)

### Query Strings

**URL:** `/blog/?page=2&sort=date`

**Access in view:**
```python
def blog_index(request):
    page = request.GET.get('page', 1)
    sort = request.GET.get('sort', 'date')
```

**Use for:** Filters, sorting, pagination, search

**Comparison:**
```
Resource:    /blog/5/           (URL parameter)
Filter:      /blog/?tag=python  (query string)
Both:        /blog/5/?print=true
```

## Trailing Slashes

**Django convention: Always include trailing slash**

```python
path("blog/", ...)       # Good
path("blog", ...)        # Works but non-standard
```

**Why?**
- Django redirects `/blog` to `/blog/` automatically
- Consistent URLs
- Follows Django best practices

**Exception:** Root URL
```python
path("", ...)  # No slash needed for root
```

## Regular Expressions (Advanced)

**For complex patterns, use re_path:**

```python
from django.urls import re_path

urlpatterns = [
    # Match year/month/day
    re_path(r'^archive/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.archive),
    
    # Match username (alphanumeric + underscore)
    re_path(r'^user/(?P<username>\w+)/$', views.profile),
]
```

**When to use:**
- Complex validation (specific formats)
- Multiple optional parameters
- Path() converters insufficient

**Prefer path() when possible** (cleaner, easier to read)

## Testing URLs

**Django shell:**
```bash
python manage.py shell
```

```python
from django.urls import reverse

# Test URL generation
reverse('blog_index')  # '/'
reverse('blog_detail', kwargs={'pk': 5})  # '/blog/5/'
reverse('blog_category', args=['Python'])  # '/blog/category/Python/'
```

**Test URL resolution:**
```python
from django.urls import resolve

match = resolve('/blog/5/')
print(match.view_name)  # 'blog_detail'
print(match.kwargs)      # {'pk': 5}
```

## Common Patterns

### List and Detail

```python
path("posts/", views.post_list, name="post_list")
path("posts/<int:pk>/", views.post_detail, name="post_detail")
```

### CRUD Operations

```python
path("posts/", views.post_list, name="post_list")
path("posts/create/", views.post_create, name="post_create")
path("posts/<int:pk>/", views.post_detail, name="post_detail")
path("posts/<int:pk>/edit/", views.post_edit, name="post_edit")
path("posts/<int:pk>/delete/", views.post_delete, name="post_delete")
```

### Nested Resources

```python
path("posts/<int:post_pk>/comments/", views.comment_list)
path("posts/<int:post_pk>/comments/<int:comment_pk>/", views.comment_detail)
```

## Summary

- **path()** - Define URL pattern
- **<type:name>** - Capture URL parameters
- **include()** - Delegate to app URLs
- **name=** - Enable reverse lookup
- **{% url %}** - Generate URLs in templates
- **reverse()** - Generate URLs in views
- Order matters: specific before generic
- Trailing slashes are Django convention
- URL parameters vs query strings: resources vs filters
- Two-level routing: project → app
- Type converters: str, int, slug, uuid, path

**URL routing connects browser requests to view functions, enabling clean, maintainable URL structures.**
