# Models: Post, Category, Comment

## Location
`blog/models.py`

## The Three Models

### 1. Category Model

```python
class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name
```

**Purpose:** Organize posts by topic/tag

**Fields:**
- `name` - Category name (e.g., "Python", "Django", "Tutorial")

**Meta options:**
- `verbose_name_plural` - Fixes admin plural ("categories" not "categorys")

**__str__ method:**
- Returns category name when printed or displayed in admin

**Example usage:**
```python
python_category = Category.objects.create(name="Python")
django_category = Category.objects.create(name="Django")
tutorial_category = Category.objects.create(name="Tutorial")
```

### 2. Post Model

```python
class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField("Category", related_name="posts")

    def __str__(self):
        return self.title
```

**Purpose:** Blog posts/articles

**Fields:**

**title** - CharField(max_length=255)
- Post title/headline
- Required (blank=False by default)
- Database: VARCHAR(255)

**body** - TextField()
- Post content
- No length limit
- Database: TEXT column

**created_on** - DateTimeField(auto_now_add=True)
- Timestamp when post created
- Set automatically once (never changes)
- Not editable in forms

**last_modified** - DateTimeField(auto_now=True)
- Timestamp when post last saved
- Updates automatically on every save()
- Not editable in forms

**categories** - ManyToManyField("Category")
- Links to multiple categories
- Creates junction table: `blog_post_categories`
- `related_name="posts"` - Enables `category.posts.all()`

**Database tables created:**
```sql
-- Main post table
CREATE TABLE blog_post (
    id INTEGER PRIMARY KEY,
    title VARCHAR(255),
    body TEXT,
    created_on DATETIME,
    last_modified DATETIME
);

-- Junction table for many-to-many
CREATE TABLE blog_post_categories (
    id INTEGER PRIMARY KEY,
    post_id INTEGER REFERENCES blog_post(id),
    category_id INTEGER REFERENCES blog_category(id)
);
```

**Example usage:**
```python
# Create post
post = Post.objects.create(
    title="Getting Started with Django",
    body="Django is a web framework..."
)

# Add categories
post.categories.add(python_category, django_category)

# Save triggers auto_now
post.body = "Updated content"
post.save()  # last_modified automatically updated
```

### 3. Comment Model

```python
class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="comments"
    )
    author = models.CharField(max_length=60, blank=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username if self.user else self.author
```

**Purpose:** Reader comments on posts

**Fields:**

**user** - ForeignKey(User)
- Links to User model (authentication)
- `on_delete=SET_NULL` - Keep comment if user deleted
- `null=True, blank=True` - Optional (for old comments)
- `related_name="comments"` - Enables `user.comments.all()`

**author** - CharField(max_length=60)
- Legacy field for old comments
- Before authentication was added
- Now optional (`blank=True`)

**body** - TextField()
- Comment text
- Required

**created_on** - DateTimeField(auto_now_add=True)
- When comment posted
- Automatic timestamp

**post** - ForeignKey("Post")
- Links to Post model
- `on_delete=CASCADE` - Delete comments when post deleted
- One-to-many: Post has many comments

**Database table:**
```sql
CREATE TABLE blog_comment (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES auth_user(id) ON DELETE SET NULL,
    author VARCHAR(60),
    body TEXT,
    created_on DATETIME,
    post_id INTEGER NOT NULL REFERENCES blog_post(id) ON DELETE CASCADE
);
```

**Example usage:**
```python
# Create comment (old way - before auth)
comment = Comment.objects.create(
    author="Alice",
    body="Great post!",
    post=post
)

# Create comment (new way - with auth)
comment = Comment.objects.create(
    user=request.user,
    body="Great post!",
    post=post
)
```

## Field Types Explained

### CharField

```python
name = models.CharField(max_length=30)
```

- Short text strings
- Must specify max_length
- Database: VARCHAR
- Form widget: TextInput (single line)

### TextField

```python
body = models.TextField()
```

- Long text strings
- No length limit
- Database: TEXT
- Form widget: Textarea (multiple lines)

### DateTimeField

```python
created_on = models.DateTimeField(auto_now_add=True)
last_modified = models.DateTimeField(auto_now=True)
```

**auto_now_add:**
- Sets timestamp when object created
- Never changes
- Use for "created_on" fields

**auto_now:**
- Updates timestamp on every save()
- Use for "last_modified" fields

**Manual:**
```python
published_date = models.DateTimeField()
# Set manually: post.published_date = timezone.now()
```

### ForeignKey

```python
post = models.ForeignKey("Post", on_delete=models.CASCADE)
```

- One-to-many relationship
- Creates foreign key in database
- Requires `on_delete` parameter

**on_delete options:**
- `CASCADE` - Delete this when related deleted
- `SET_NULL` - Set to NULL when related deleted (requires null=True)
- `PROTECT` - Prevent deletion of related object
- `SET_DEFAULT` - Set to default value

### ManyToManyField

```python
categories = models.ManyToManyField("Category", related_name="posts")
```

- Many-to-many relationship
- Creates junction table automatically
- No `on_delete` needed (handled by junction table)

## Model Methods

### __str__()

```python
def __str__(self):
    return self.title
```

**Purpose:** Human-readable representation

**Used in:**
- Admin interface
- Django shell
- print() statements
- Template {{ object }} (if no specific field)

**Example:**
```python
post = Post.objects.get(pk=1)
print(post)  # "Getting Started with Django"
# Without __str__: "<Post object (1)>"
```

### Custom Methods

You can add custom methods to models:

```python
class Post(models.Model):
    # ... fields ...
    
    def comment_count(self):
        return self.comment_set.count()
    
    def get_first_paragraph(self):
        return self.body.split('\n\n')[0]
    
    def is_recent(self):
        from django.utils import timezone
        from datetime import timedelta
        return self.created_on >= timezone.now() - timedelta(days=7)
```

**Usage:**
```python
post = Post.objects.get(pk=1)
post.comment_count()  # 5
post.is_recent()  # True
```

**In templates:**
```django
{{ post.comment_count }} comments
{% if post.is_recent %}
    <span class="badge">New!</span>
{% endif %}
```

## Relationships

### Forward Relationship (ForeignKey)

```python
comment = Comment.objects.get(pk=1)
comment.post  # Access related Post
comment.post.title  # "My Post Title"
```

### Reverse Relationship (comment_set)

```python
post = Post.objects.get(pk=1)
post.comment_set.all()  # All comments on this post
post.comment_set.count()  # Number of comments
post.comment_set.filter(user__username='alice')  # Alice's comments on this post
```

### ManyToMany Relationship

```python
# Add categories
post.categories.add(python_category)
post.categories.add(django_category, tutorial_category)

# Remove categories
post.categories.remove(python_category)

# Clear all
post.categories.clear()

# Set exactly these categories
post.categories.set([python_category, django_category])

# Query
post.categories.all()  # All categories for this post
post.categories.filter(name='Python')  # Specific category
```

### Reverse ManyToMany (related_name)

```python
category = Category.objects.get(name='Python')
category.posts.all()  # All posts in Python category
category.posts.count()  # Number of Python posts
```

## Querying Models

### Get Single Object

```python
# By primary key
post = Post.objects.get(pk=1)

# By field
category = Category.objects.get(name='Python')

# Raises DoesNotExist if not found
# Raises MultipleObjectsReturned if multiple found
```

### Get Multiple Objects

```python
# All objects
Post.objects.all()

# Filter
Post.objects.filter(title__contains='Django')
Post.objects.filter(categories__name='Python')

# Exclude
Post.objects.exclude(title__contains='Old')

# Order
Post.objects.order_by('-created_on')  # Newest first
Post.objects.order_by('title')  # Alphabetical
```

### Create Objects

```python
# Method 1: create()
post = Post.objects.create(
    title="My Post",
    body="Content here"
)

# Method 2: save()
post = Post()
post.title = "My Post"
post.body = "Content here"
post.save()
```

### Update Objects

```python
# Single object
post = Post.objects.get(pk=1)
post.title = "New Title"
post.save()

# Multiple objects
Post.objects.filter(categories__name='Old').update(title='Updated')
```

### Delete Objects

```python
# Single object
post = Post.objects.get(pk=1)
post.delete()

# Multiple objects
Post.objects.filter(created_on__year=2020).delete()
```

## Summary

- **Category** - Simple model with just a name
- **Post** - Main content with title, body, timestamps, categories
- **Comment** - User feedback with text, timestamps, links to Post and User
- **ForeignKey** - One-to-many (Comment → Post)
- **ManyToManyField** - Many-to-many (Post ↔ Category)
- **auto_now_add** - Set timestamp once on creation
- **auto_now** - Update timestamp on every save
- **__str__()** - Makes objects readable
- **related_name** - Enables reverse queries
- **on_delete** - Controls cascade behavior
