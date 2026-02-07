# Views: Blog Index, Detail, Category

## Location
`blog/views.py`

## What are Views?

Views are Python functions that:
1. Receive HTTP requests
2. Process data (query database, validate forms, etc.)
3. Return HTTP responses (usually rendered templates)

**Flow:** Browser request → URL routing → View function → Template → Response

## The Three Blog Views

### 1. blog_index() - Homepage

```python
def blog_index(request):
    posts = Post.objects.all().order_by("-created_on")
    context = {
        "posts": posts,
    }
    return render(request, "blog_index.html", context)
```

**Purpose:** Display all blog posts on homepage

**Line-by-line:**

**Line 1:** `def blog_index(request):`
- Function definition
- `request` - HTTP request object (always first parameter)
- Contains: method (GET/POST), user, session, headers, etc.

**Line 2:** `posts = Post.objects.all().order_by("-created_on")`
- **Post.objects.all()** - Query all posts from database
- **.order_by("-created_on")** - Sort by created date
- **"-created_on"** - Minus means descending (newest first)
- **posts** - QuerySet (list-like) of Post objects

**Line 3-5:** Context dictionary
```python
context = {
    "posts": posts,
}
```
- Dictionary passed to template
- Keys become template variables
- `posts` will be accessible as `{{ posts }}` in template

**Line 6:** `return render(request, "blog_index.html", context)`
- **render()** - Shortcut function
- Loads template, combines with context, returns HttpResponse
- Parameters: request, template name, context dict

**Equivalent long form:**
```python
from django.template import loader
from django.http import HttpResponse

template = loader.get_template("blog_index.html")
html = template.render(context, request)
return HttpResponse(html)
```

**Request flow:**
1. User visits `/`
2. URL routes to `blog_index()`
3. Query database: `SELECT * FROM blog_post ORDER BY created_on DESC`
4. Create context with posts
5. Render template with data
6. Return HTML to browser

### 2. blog_detail() - Single Post

```python
def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            if request.user.is_authenticated:
                comment.user = request.user
            comment.save()
            return HttpResponseRedirect(request.path_info)
    
    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
        "form": form,
    }
    return render(request, "blog_detail.html", context)
```

**Purpose:** Display single post with comments and comment form

**Line-by-line:**

**Line 1:** `def blog_detail(request, pk):`
- `request` - HTTP request object
- `pk` - Post ID from URL (e.g., `/blog/5/` → pk=5)

**Line 2:** `post = Post.objects.get(pk=pk)`
- Get specific post by primary key
- Raises `DoesNotExist` if post not found (shows 404 in production)
- `pk=pk` - left pk is field name, right pk is URL parameter

**Line 3:** `form = CommentForm()`
- Create empty comment form
- Will be replaced if POST request
- Initial form for GET requests

**Line 4:** `if request.method == "POST":`
- Check if form submitted
- **GET** - User viewing page (show empty form)
- **POST** - User submitted form (process data)

**Line 5:** `form = CommentForm(request.POST)`
- Create form with submitted data
- `request.POST` - Dictionary of form fields
- Example: `{'body': 'Great post!'}`

**Line 6:** `if form.is_valid():`
- Validate submitted data
- Checks: required fields, max lengths, data types
- Returns True/False
- Adds errors to form if invalid

**Line 7:** `comment = form.save(commit=False)`
- Create Comment object without saving to database
- `commit=False` - Don't save yet (need to add post and user)
- Returns unsaved Comment instance

**Line 8:** `comment.post = post`
- Link comment to current post
- Sets foreign key relationship

**Line 9:** `if request.user.is_authenticated:`
- Check if user logged in
- `request.user` - Current user or AnonymousUser

**Line 10:** `comment.user = request.user`
- Link comment to logged-in user
- Only if authenticated

**Line 11:** `comment.save()`
- Save comment to database
- Now has post, user (if authenticated), and body

**Line 12:** `return HttpResponseRedirect(request.path_info)`
- Redirect to same page
- **Why?** Prevents duplicate submissions (F5 won't resubmit form)
- **POST/Redirect/GET pattern** - Best practice
- `request.path_info` - Current URL (e.g., `/blog/5/`)

**Line 14:** `comments = Comment.objects.filter(post=post)`
- Get all comments for this post
- `filter()` returns QuerySet (can be empty)
- Alternative: `post.comment_set.all()`

**Line 15-19:** Context dictionary
```python
context = {
    "post": post,
    "comments": comments,
    "form": form,
}
```
- **post** - Post object for display
- **comments** - QuerySet of comments
- **form** - Empty form or form with validation errors

**Line 20:** `return render(request, "blog_detail.html", context)`
- Render template with context

**Request flows:**

**GET request (viewing post):**
1. User visits `/blog/5/`
2. `blog_detail(request, pk=5)`
3. Get post 5 from database
4. Create empty form
5. Get comments for post 5
6. Render template
7. Show post, comments, empty form

**POST request (submitting comment):**
1. User submits form at `/blog/5/`
2. `blog_detail(request, pk=5)`
3. Get post 5
4. Create form with POST data
5. Validate form
6. Create comment (commit=False)
7. Set comment.post = post
8. If authenticated, set comment.user
9. Save comment
10. Redirect to `/blog/5/` (GET request)
11. Show post with new comment

### 3. blog_category() - Category Filter

```python
def blog_category(request, category):
    posts = Post.objects.filter(categories__name__contains=category).order_by("-created_on")
    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "blog_category.html", context)
```

**Purpose:** Display posts in specific category

**Line-by-line:**

**Line 1:** `def blog_category(request, category):`
- `category` - Category name from URL (e.g., `/blog/category/Python/`)

**Line 2:** Complex query
```python
posts = Post.objects.filter(
    categories__name__contains=category
).order_by("-created_on")
```

**Breaking it down:**

**Post.objects.filter()**
- Query posts matching criteria

**categories__name__contains**
- **Double underscore** - Field lookup across relationships
- **categories** - ManyToMany field on Post model
- **name** - Field on Category model
- **contains** - Case-insensitive substring match
- SQL equivalent: `WHERE category.name LIKE '%Python%'`

**Other lookup options:**
```python
# Exact match
categories__name='Python'

# Case-insensitive exact
categories__name__iexact='python'

# Starts with
categories__name__startswith='Py'

# In list
categories__name__in=['Python', 'Django']
```

**.order_by("-created_on")**
- Sort newest first

**Example:** URL `/blog/category/Python/`
- Finds all posts with "Python" in category name
- Posts can have multiple categories
- Returns posts sorted by date

**Line 3-6:** Context with category name and filtered posts

**Line 7:** Render template

**Request flow:**
1. User clicks category link "Python"
2. URL routes to `blog_category(request, category='Python')`
3. Query: `SELECT * FROM blog_post WHERE id IN (SELECT post_id FROM blog_post_categories WHERE category_id IN (SELECT id FROM blog_category WHERE name LIKE '%Python%')) ORDER BY created_on DESC`
4. Create context with category name and posts
5. Render template
6. Show filtered posts

## Common View Patterns

### Get Object or 404

**Problem:** `Post.objects.get(pk=999)` raises exception if not found

**Solution:**
```python
from django.shortcuts import get_object_or_404

def blog_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # ... rest of view
```

**Benefits:**
- Shows 404 page instead of 500 error
- Better user experience
- One line instead of try/except

### List View Pattern

```python
def blog_index(request):
    posts = Post.objects.all().order_by("-created_on")
    context = {"posts": posts}
    return render(request, "blog_index.html", context)
```

**Common for:** Homepage, archives, search results

### Detail View Pattern

```python
def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    context = {"post": post}
    return render(request, "blog_detail.html", context)
```

**Common for:** Single object display

### Form View Pattern (GET/POST)

```python
def my_view(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')
    else:
        form = MyForm()
    
    context = {"form": form}
    return render(request, "my_template.html", context)
```

**Common for:** Contact forms, comment forms, data entry

## The Request Object

Every view receives `request` as first parameter.

**Useful attributes:**

```python
# HTTP method
request.method  # 'GET' or 'POST'

# User
request.user  # Current user or AnonymousUser
request.user.is_authenticated  # True/False
request.user.username  # 'alice'

# Form data
request.POST['field_name']  # Get form field
request.POST.get('field_name', 'default')  # Safer

# URL parameters
request.GET['search']  # /page/?search=django
request.GET.get('page', 1)  # /page/?page=2

# Path
request.path  # '/blog/5/'
request.path_info  # '/blog/5/'
request.get_full_path()  # '/blog/5/?next=/home/'

# Session
request.session['key'] = 'value'
request.session.get('key')
```

## Context Explained

Context is a dictionary passed to templates:

```python
context = {
    "post": post,
    "comments": comments,
    "form": form,
}
```

**In template:**
```django
{{ post.title }}
{% for comment in comments %}
    {{ comment.body }}
{% endfor %}
{{ form.as_p }}
```

**You can pass anything:**
```python
context = {
    "posts": Post.objects.all(),
    "count": 42,
    "username": request.user.username,
    "categories": ["Python", "Django"],
    "is_admin": request.user.is_staff,
}
```

## Form Processing Flow

**GET Request (display form):**
```
User → URL → View → Create empty form → Render template → Show form
```

**POST Request (submit form):**
```
User → Submit → View → Create form with data → Validate
    ↓
Valid → Process → Save → Redirect → GET request → Show success
    ↓
Invalid → Render template with errors → Show form again
```

**Code:**
```python
def my_view(request):
    if request.method == "POST":
        form = CommentForm(request.POST)  # Bind data
        if form.is_valid():               # Validate
            comment = form.save(commit=False)  # Create object
            comment.post = post           # Modify
            comment.save()                # Save
            return redirect('success')    # Redirect
    else:
        form = CommentForm()              # Empty form
    
    return render(request, "template.html", {"form": form})
```

## QuerySet Methods

**All objects:**
```python
Post.objects.all()
```

**Filter (WHERE):**
```python
Post.objects.filter(title='My Post')
Post.objects.filter(title__contains='Django')
Post.objects.filter(created_on__year=2024)
Post.objects.filter(categories__name='Python')
```

**Exclude (WHERE NOT):**
```python
Post.objects.exclude(title='Old Post')
```

**Get one (raises exception if 0 or >1):**
```python
Post.objects.get(pk=1)
```

**Order by (ORDER BY):**
```python
Post.objects.order_by('title')        # Ascending
Post.objects.order_by('-created_on')  # Descending
Post.objects.order_by('title', '-created_on')  # Multiple
```

**Count:**
```python
Post.objects.count()
Post.objects.filter(categories__name='Python').count()
```

**Exists:**
```python
Post.objects.filter(title='Test').exists()  # True/False
```

**Chain methods:**
```python
Post.objects.filter(
    categories__name='Python'
).exclude(
    title__contains='Old'
).order_by(
    '-created_on'
)[:5]  # First 5 results
```

## Summary

- **blog_index()** - List all posts, newest first
- **blog_detail()** - Show single post, handle comment form
- **blog_category()** - Filter posts by category
- Views receive `request` and return responses
- Context dictionary passes data to templates
- GET requests show forms, POST requests process them
- Always redirect after successful POST
- QuerySets are lazy (query only executed when used)
- Double underscores cross relationships: `categories__name`
- `order_by("-field")` sorts descending
