# Database Queries with Django ORM

## What is the ORM?

**ORM = Object-Relational Mapping**

Maps Python code → SQL queries → Database

**Benefits:**
- Write Python, not SQL
- Database-agnostic (works with SQLite, PostgreSQL, MySQL)
- Type-safe (Python objects, not raw strings)
- Prevents SQL injection
- Easier to maintain

**Example:**
```python
# Python ORM
posts = Post.objects.filter(title__contains='Django')

# SQL equivalent
# SELECT * FROM blog_post WHERE title LIKE '%Django%'
```

## QuerySet Basics

**QuerySet:** Lazy, chainable database query

**Lazy execution:**
```python
# No database hit yet
posts = Post.objects.all()

# Database hit happens here
for post in posts:
    print(post.title)
```

**Chaining:**
```python
posts = Post.objects.filter(
    categories__name='Python'
).exclude(
    title__contains='Old'
).order_by(
    '-created_on'
)[:5]
```

## Retrieving Objects

### All Objects

```python
# Get all posts
posts = Post.objects.all()

# SQL: SELECT * FROM blog_post
```

**Iterate:**
```python
for post in posts:
    print(post.title)
```

**Count:**
```python
Post.objects.all().count()  # 42
# SQL: SELECT COUNT(*) FROM blog_post
```

### Filter (WHERE)

```python
# Exact match
Post.objects.filter(title='My Post')
# SQL: WHERE title = 'My Post'

# Contains (case-insensitive)
Post.objects.filter(title__contains='Django')
# SQL: WHERE title LIKE '%Django%'

# Case-insensitive exact
Post.objects.filter(title__iexact='my post')
# SQL: WHERE UPPER(title) = UPPER('my post')

# Multiple conditions (AND)
Post.objects.filter(title__contains='Django', created_on__year=2024)
# SQL: WHERE title LIKE '%Django%' AND EXTRACT(year FROM created_on) = 2024
```

### Exclude (WHERE NOT)

```python
# Not equal
Post.objects.exclude(title='Draft')
# SQL: WHERE title != 'Draft'

# Combined with filter
Post.objects.filter(created_on__year=2024).exclude(title__contains='Draft')
# SQL: WHERE EXTRACT(year FROM created_on) = 2024 AND title NOT LIKE '%Draft%'
```

### Get Single Object

```python
# Get by primary key
post = Post.objects.get(pk=1)

# Get by unique field
category = Category.objects.get(name='Python')
```

**Important:**
- Raises `DoesNotExist` if not found
- Raises `MultipleObjectsReturned` if multiple found
- Use `filter()[0]` or `first()` for safer queries

**Safe alternatives:**
```python
# Return None if not found
post = Post.objects.filter(pk=999).first()

# 404 if not found (in views)
from django.shortcuts import get_object_or_404
post = get_object_or_404(Post, pk=999)
```

### First/Last

```python
# First by ordering
Post.objects.order_by('created_on').first()

# Last by ordering
Post.objects.order_by('created_on').last()

# Returns None if empty
Post.objects.filter(title='Nonexistent').first()  # None
```

### Exists

```python
# Check if exists (efficient)
Post.objects.filter(title='Test').exists()  # True/False

# Better than
bool(Post.objects.filter(title='Test'))  # Fetches all objects
```

## Field Lookups

### Exact Matches

```python
Post.objects.filter(title='Exact Title')          # Exact
Post.objects.filter(title__exact='Exact Title')   # Same as above
Post.objects.filter(title__iexact='exact title')  # Case-insensitive
```

### Partial Matches

```python
Post.objects.filter(title__contains='Django')       # 'My Django Post'
Post.objects.filter(title__icontains='django')      # Case-insensitive
Post.objects.filter(title__startswith='Getting')    # 'Getting Started'
Post.objects.filter(title__endswith='Guide')        # 'Complete Guide'
```

### Comparisons

```python
# Greater than
Post.objects.filter(created_on__gt=date)         # >
Post.objects.filter(created_on__gte=date)        # >=

# Less than
Post.objects.filter(created_on__lt=date)         # <
Post.objects.filter(created_on__lte=date)        # <=

# Range
from datetime import date
start = date(2024, 1, 1)
end = date(2024, 12, 31)
Post.objects.filter(created_on__range=(start, end))
```

### In List

```python
# In list of values
Post.objects.filter(id__in=[1, 2, 3, 4])

# In subquery
recent_comments = Comment.objects.filter(created_on__gte=last_week)
Post.objects.filter(id__in=recent_comments.values('post_id'))
```

### Null Checks

```python
# IS NULL
Comment.objects.filter(user__isnull=True)

# IS NOT NULL
Comment.objects.filter(user__isnull=False)
```

### Date/Time

```python
# Year
Post.objects.filter(created_on__year=2024)

# Month
Post.objects.filter(created_on__month=1)

# Day
Post.objects.filter(created_on__day=15)

# Date (ignore time)
from datetime import date
Post.objects.filter(created_on__date=date(2024, 1, 15))

# Today
from django.utils import timezone
today = timezone.now().date()
Post.objects.filter(created_on__date=today)
```

## Ordering

### Order By

```python
# Ascending
Post.objects.order_by('title')

# Descending
Post.objects.order_by('-created_on')

# Multiple fields
Post.objects.order_by('-created_on', 'title')

# Random
Post.objects.order_by('?')  # Warning: Slow!
```

### Reverse

```python
# Reverse current ordering
posts = Post.objects.order_by('created_on')
reversed_posts = posts.reverse()
```

## Slicing (LIMIT)

```python
# First 5
Post.objects.all()[:5]
# SQL: LIMIT 5

# Skip 5, get next 5
Post.objects.all()[5:10]
# SQL: OFFSET 5 LIMIT 5

# Get 10th item (0-indexed)
Post.objects.all()[9]

# Last item (requires ordering)
Post.objects.order_by('created_on').reverse()[0]
```

**Cannot use negative indices:**
```python
Post.objects.all()[-1]  # Error!
```

## Relationships

### Forward (ForeignKey)

```python
# Comment has user ForeignKey
comment = Comment.objects.get(pk=1)

# Access related user (1 query)
comment.user  # User object
comment.user.username  # 'alice'

# Access related post
comment.post  # Post object
comment.post.title  # 'My Post'
```

### Reverse (Related Name)

```python
# Post has many comments
post = Post.objects.get(pk=1)

# Access comments (default: modelname_set)
post.comment_set.all()  # All comments

# If related_name specified
# user = ForeignKey(User, related_name='comments')
user.comments.all()  # Instead of user.comment_set.all()
```

### Many-to-Many

```python
# Post has many categories
post = Post.objects.get(pk=1)

# Get all categories
post.categories.all()

# Add category
python_cat = Category.objects.get(name='Python')
post.categories.add(python_cat)

# Remove category
post.categories.remove(python_cat)

# Clear all
post.categories.clear()

# Set exactly these
post.categories.set([cat1, cat2, cat3])
```

### Reverse Many-to-Many

```python
# Category has many posts (via related_name='posts')
category = Category.objects.get(name='Python')

# Get all posts in category
category.posts.all()

# Count posts
category.posts.count()
```

### Spanning Relationships

**Double underscore to traverse relationships:**

```python
# Comments by username
Comment.objects.filter(user__username='alice')
# SQL: JOIN auth_user ON ... WHERE auth_user.username = 'alice'

# Posts in category
Post.objects.filter(categories__name='Python')
# SQL: JOIN blog_post_categories ... WHERE blog_category.name = 'Python'

# Posts with comments by specific user
Post.objects.filter(comment__user__username='alice')
# SQL: JOIN blog_comment ... JOIN auth_user ... WHERE username = 'alice'

# Deep traversal
Comment.objects.filter(post__categories__name='Python')
# Comments on posts in Python category
```

## Aggregation

### Count

```python
# Count all
Post.objects.count()

# Count filtered
Post.objects.filter(categories__name='Python').count()

# Annotate with count
from django.db.models import Count

posts = Post.objects.annotate(comment_count=Count('comment'))
for post in posts:
    print(post.title, post.comment_count)
```

### Other Aggregates

```python
from django.db.models import Avg, Max, Min, Sum

# Average (example with numeric field)
Post.objects.aggregate(Avg('view_count'))
# {'view_count__avg': 125.5}

# Max/Min
Post.objects.aggregate(Max('created_on'))
Post.objects.aggregate(Min('created_on'))

# Multiple aggregates
Post.objects.aggregate(
    total=Count('id'),
    avg_views=Avg('view_count'),
    max_date=Max('created_on')
)
```

### Annotate (Per-Object Aggregates)

```python
from django.db.models import Count

# Add comment count to each post
posts = Post.objects.annotate(comment_count=Count('comment'))

for post in posts:
    print(f"{post.title}: {post.comment_count} comments")

# Filter by annotated value
popular_posts = Post.objects.annotate(
    comment_count=Count('comment')
).filter(comment_count__gte=10)

# Order by annotated value
posts = Post.objects.annotate(
    comment_count=Count('comment')
).order_by('-comment_count')
```

## Q Objects (Complex Queries)

**OR conditions:**

```python
from django.db.models import Q

# title contains 'Django' OR 'Python'
Post.objects.filter(
    Q(title__contains='Django') | Q(title__contains='Python')
)

# title contains 'Django' AND (category Python OR Tutorial)
Post.objects.filter(
    Q(title__contains='Django') &
    (Q(categories__name='Python') | Q(categories__name='Tutorial'))
)

# NOT
Post.objects.filter(~Q(title__contains='Draft'))
```

**Complex example:**
```python
# Posts that either:
# - Are in Python category, OR
# - Have 'Django' in title AND created this year
from django.utils import timezone

Post.objects.filter(
    Q(categories__name='Python') |
    (Q(title__contains='Django') & Q(created_on__year=timezone.now().year))
)
```

## F Expressions (Field References)

**Reference field values:**

```python
from django.db.models import F

# Update view count
post.view_count = F('view_count') + 1
post.save()

# Filter by field comparison
# Posts modified after creation (edited)
Post.objects.filter(last_modified__gt=F('created_on'))

# Arithmetic
Post.objects.filter(view_count__gt=F('like_count') * 2)
```

## Creating Objects

### Create and Save

```python
# Method 1: create() - one step
post = Post.objects.create(
    title='New Post',
    body='Content here'
)

# Method 2: save() - two steps
post = Post()
post.title = 'New Post'
post.body = 'Content here'
post.save()
```

### Bulk Create

```python
# Create multiple at once (one query)
posts = [
    Post(title='Post 1', body='Body 1'),
    Post(title='Post 2', body='Body 2'),
    Post(title='Post 3', body='Body 3'),
]
Post.objects.bulk_create(posts)

# Much faster than
for data in post_data:
    Post.objects.create(**data)  # N queries
```

### Get or Create

```python
# Get if exists, create if not
category, created = Category.objects.get_or_create(name='Python')

if created:
    print('Created new category')
else:
    print('Category already existed')

# With defaults
post, created = Post.objects.get_or_create(
    title='My Post',
    defaults={'body': 'Default content'}
)
```

### Update or Create

```python
# Update if exists, create if not
post, created = Post.objects.update_or_create(
    title='My Post',
    defaults={'body': 'Updated content', 'last_modified': timezone.now()}
)
```

## Updating Objects

### Single Object

```python
post = Post.objects.get(pk=1)
post.title = 'Updated Title'
post.save()
```

### Update Query (Multiple Objects)

```python
# Update multiple at once (one query)
Post.objects.filter(created_on__year=2023).update(title='Archived')

# Returns number updated
updated_count = Post.objects.filter(status='draft').update(status='published')
print(f'Published {updated_count} posts')

# F expressions
Post.objects.all().update(view_count=F('view_count') + 1)
```

**update() vs save():**
- `update()` - Direct SQL, faster, doesn't call save() signals
- `save()` - Calls signal handlers, allows custom logic

### Bulk Update

```python
posts = Post.objects.filter(created_on__year=2023)
for post in posts:
    post.title = f'Archived: {post.title}'

Post.objects.bulk_update(posts, ['title'])  # One query
```

## Deleting Objects

### Single Object

```python
post = Post.objects.get(pk=1)
post.delete()
```

### Delete Query (Multiple Objects)

```python
# Delete multiple
Post.objects.filter(created_on__year=2020).delete()

# Delete all (dangerous!)
Post.objects.all().delete()

# Returns (count, details)
deleted = Post.objects.filter(status='draft').delete()
print(deleted)
# (5, {'blog.Post': 5, 'blog.Comment': 12})
# Deleted 5 posts and 12 related comments (CASCADE)
```

## Select Related (Optimization)

**Problem: N+1 queries**

```python
# Bad: 11 queries (1 + 10)
comments = Comment.objects.all()[:10]
for comment in comments:
    print(comment.user.username)  # Separate query each time!
```

**Solution: select_related (JOIN)**

```python
# Good: 1 query
comments = Comment.objects.select_related('user')[:10]
for comment in comments:
    print(comment.user.username)  # Already loaded!

# SQL: SELECT * FROM blog_comment JOIN auth_user ...
```

**Use for ForeignKey and OneToOne:**
```python
# Single relation
comments = Comment.objects.select_related('user')

# Multiple relations
comments = Comment.objects.select_related('user', 'post')

# Nested relations
comments = Comment.objects.select_related('post__categories')
```

## Prefetch Related (Optimization)

**For Many-to-Many and Reverse ForeignKey:**

```python
# Bad: N+1 queries
posts = Post.objects.all()
for post in posts:
    for category in post.categories.all():  # Separate query each time!
        print(category.name)

# Good: 2 queries (posts + categories)
posts = Post.objects.prefetch_related('categories')
for post in posts:
    for category in post.categories.all():  # Already loaded!
        print(category.name)
```

**Use for:**
```python
# Many-to-many
posts = Post.objects.prefetch_related('categories')

# Reverse foreign key
posts = Post.objects.prefetch_related('comment_set')

# With related_name
users = User.objects.prefetch_related('comments')

# Nested
categories = Category.objects.prefetch_related('posts__comment_set')
```

**Combine both:**
```python
# Optimize complex query
comments = Comment.objects.select_related(
    'user',  # JOIN user
    'post'   # JOIN post
).prefetch_related(
    'post__categories'  # Prefetch categories
)
```

## Raw SQL (When Needed)

```python
# Raw query
posts = Post.objects.raw('SELECT * FROM blog_post WHERE title LIKE %s', ['%Django%'])

for post in posts:
    print(post.title)

# Execute custom SQL
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute('SELECT COUNT(*) FROM blog_post')
    count = cursor.fetchone()[0]
```

**Use sparingly:** ORM handles 99% of cases

## Debugging Queries

### Print SQL

```python
posts = Post.objects.filter(title__contains='Django')
print(posts.query)
# SQL query string
```

### Query Log

```python
from django.db import connection

Post.objects.all().count()

print(len(connection.queries))  # Number of queries
print(connection.queries)        # List of all queries
```

### Django Debug Toolbar

**Install:**
```bash
pip install django-debug-toolbar
```

**Shows:**
- All queries per page
- Execution time
- Duplicate queries
- Recommendations

## Common Queries

### Blog Index

```python
# All posts, newest first
posts = Post.objects.all().order_by('-created_on')

# With optimizations
posts = Post.objects.select_related().prefetch_related('categories').order_by('-created_on')
```

### Post Detail

```python
# Get post with related data
post = Post.objects.prefetch_related('categories').get(pk=5)

# Get comments
comments = Comment.objects.filter(post=post).select_related('user').order_by('created_on')
```

### Category Filter

```python
# Posts in category
posts = Post.objects.filter(
    categories__name__contains='Python'
).prefetch_related(
    'categories'
).order_by('-created_on')
```

### User Comments

```python
# All comments by user
comments = Comment.objects.filter(user=request.user).select_related('post').order_by('-created_on')
```

### Recent Posts

```python
from datetime import timedelta
from django.utils import timezone

week_ago = timezone.now() - timedelta(days=7)
recent_posts = Post.objects.filter(created_on__gte=week_ago)
```

## Best Practices

1. **Use filter().first() instead of get() for optional queries**
2. **Annotate counts in list views**
3. **Use select_related for ForeignKey**
4. **Use prefetch_related for Many-to-Many**
5. **Filter before orderby/slice for efficiency**
6. **Use update() for bulk updates**
7. **Use bulk_create() for multiple objects**
8. **Debug with .query and Debug Toolbar**
9. **Avoid queries in loops (N+1 problem)**
10. **Use exists() to check existence**

## Summary

- **QuerySets** are lazy and chainable
- **filter()** for WHERE conditions
- **exclude()** for WHERE NOT
- **get()** for single object
- **order_by()** for ORDER BY
- **[:5]** for LIMIT
- **Double underscore** for relationships and lookups
- **select_related()** for ForeignKey (JOIN)
- **prefetch_related()** for Many-to-Many (separate query)
- **annotate()** for per-object aggregates
- **Q()** for OR conditions
- **F()** for field references

**The ORM provides powerful, secure, and Pythonic database access.**
