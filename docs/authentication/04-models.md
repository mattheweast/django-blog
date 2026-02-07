# Models & Database

## The User Model

### Import
```python
from django.contrib.auth.models import User
```

### Built-in Fields

Django's User model comes with these fields:

```python
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
```

### Field Explanations

**username**
- Required, unique
- Max 150 characters
- Letters, digits, @/./+/-/_ allowed

**password**
- Stored as hash, not plain text
- Format: `pbkdf2_sha256$260000$salt$hash`
- You never access it directly

**is_staff**
- Can access admin panel?
- `False` for regular users
- `True` for admin users

**is_superuser**
- Has all permissions?
- `False` for regular users
- `True` for admins with full access

**is_active**
- Account enabled?
- `False` = user cannot login
- Useful for soft-delete (disable instead of delete)

### User Methods

```python
user = User.objects.get(username='alice')

# Check password
user.check_password('secret')  # True/False

# Set password (automatically hashes)
user.set_password('new_password')
user.save()

# Get full name
user.get_full_name()  # "Alice Smith"
user.get_short_name()  # "Alice"

# Check permissions
user.has_perm('blog.add_post')
user.has_perms(['blog.add_post', 'blog.change_post'])

# Email user (requires email configured)
user.email_user('Subject', 'Message')
```

## Comment Model Changes

### Before Authentication

```python
class Comment(models.Model):
    author = models.CharField(max_length=60)  # Plain text name
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
```

**Problem:**
- No way to verify who wrote the comment
- Users can impersonate others
- No account association

### After Authentication

```python
from django.contrib.auth.models import User

class Comment(models.Model):
    # NEW: Link to User account
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="comments"
    )
    
    # OLD: Keep for backward compatibility
    author = models.CharField(max_length=60, blank=True)
    
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username if self.user else self.author
```

### ForeignKey Parameters Explained

**`on_delete=models.SET_NULL`**
```python
# If user gets deleted, don't delete their comments
# Just set user=NULL and keep the comment

# Example:
user = User.objects.get(username='alice')
user.delete()
# Alice's comments still exist, but comment.user = None
```

**Other options:**
- `CASCADE` - Delete comments when user deleted
- `PROTECT` - Prevent user deletion if they have comments
- `SET_DEFAULT` - Set to default value

**`null=True`**
- Database can store NULL
- Column allows NULL values

**`blank=True`**
- Form validation allows empty
- Django forms won't require this field

**Why both?**
- `null=True` = database level
- `blank=True` = validation level
- Usually used together for optional fields

**`related_name="comments"`**
```python
# Allows reverse lookup

user = User.objects.get(username='alice')
user.comments.all()  # All comments by alice
user.comments.count()  # Number of comments

# Without related_name:
user.comment_set.all()  # Django's auto-generated name
```

## Database Relationships

### One-to-Many (ForeignKey)

```python
class Comment(models.Model):
    user = models.ForeignKey(User, ...)
    post = models.ForeignKey(Post, ...)
```

**Means:**
- One user has many comments
- One post has many comments
- Each comment belongs to one user and one post

**Database structure:**
```
Comment table:
id | body              | user_id | post_id
1  | "Great!"         | 5       | 1
2  | "Thanks!"        | 3       | 1
3  | "Nice post"      | 5       | 2

User table:              Post table:
id | username          id | title
5  | alice             1  | First Post
3  | bob               2  | Second Post
```

### Querying Relationships

```python
# Get comment's user
comment = Comment.objects.get(id=1)
print(comment.user.username)  # "alice"

# Get user's comments
user = User.objects.get(username='alice')
alice_comments = user.comments.all()

# Filter comments by user
Comment.objects.filter(user__username='alice')

# Count user's comments
user.comments.count()

# Get posts with comments by a specific user
Post.objects.filter(comment__user__username='alice').distinct()
```

## Creating Users

### In Python Shell

```python
from django.contrib.auth.models import User

# Create regular user
user = User.objects.create_user(
    username='alice',
    email='alice@example.com',
    password='secret123'  # Gets hashed automatically
)

# Create superuser
admin = User.objects.create_superuser(
    username='admin',
    email='admin@example.com',
    password='admin123'
)
```

### Via Management Command

```bash
python manage.py createsuperuser
# Prompts for username, email, password
```

### Via Registration Form

```python
# In views.py
from django.contrib.auth.forms import UserCreationForm

form = UserCreationForm(request.POST)
if form.is_valid():
    user = form.save()  # Automatically hashes password
```

## Database Tables

### Auth Tables Created

When you install `django.contrib.auth` and run migrations:

```
auth_user               # User accounts
auth_group              # Permission groups (e.g., "Editors", "Moderators")
auth_permission         # Individual permissions
auth_group_permissions  # Which permissions each group has
auth_user_groups        # Which groups each user belongs to
auth_user_user_permissions  # Direct user permissions
```

### Session Table

When you install `django.contrib.sessions`:

```
django_session
```

**Structure:**
```sql
CREATE TABLE django_session (
    session_key VARCHAR(40) PRIMARY KEY,
    session_data TEXT,
    expire_date DATETIME
);
```

## Migration Example

### Generated Migration

When we added `user` field to Comment, Django created this:

```python
# blog/migrations/0002_comment_user_alter_comment_author.py

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='comments',
                to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.CharField(blank=True, max_length=60),
        ),
    ]
```

**What it does:**
1. Adds `user_id` column to `blog_comment` table (NULL allowed)
2. Creates foreign key constraint to `auth_user` table
3. Makes `author` field optional (blank=True)

### Running Migrations

```bash
# Create migration file
python manage.py makemigrations

# See SQL that will run
python manage.py sqlmigrate blog 0002

# Apply migration
python manage.py migrate
```

## Summary

- Django provides a complete User model with authentication built-in
- ForeignKey creates one-to-many relationships
- `on_delete` controls what happens when related object deleted
- `related_name` enables reverse lookups
- Migrations track database schema changes
- Passwords are automatically hashed - never stored as plain text
