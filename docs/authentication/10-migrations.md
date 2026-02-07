# Database Migrations

## What Are Migrations?

Migrations are Django's way of propagating changes you make to your models (adding a field, deleting a model, etc.) into your database schema.

Think of them as **version control for your database**.

## The Two-Step Process

### Step 1: makemigrations

```bash
python manage.py makemigrations
```

**What it does:**
1. Scans all models in INSTALLED_APPS
2. Compares to previous migrations
3. Detects changes
4. Generates Python code to apply changes
5. Creates migration file(s)

**Does NOT modify database** - just creates the migration file.

### Step 2: migrate

```bash
python manage.py migrate
```

**What it does:**
1. Reads migration files
2. Checks which haven't been applied yet
3. Generates SQL
4. Executes SQL on database
5. Records migrations in `django_migrations` table

**Actually modifies the database.**

## Our Authentication Migration

### What Changed

We added `user` field to Comment model:

```python
# blog/models.py
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    author = models.CharField(max_length=60, blank=True)  # Made optional
    # ...
```

### Running makemigrations

```bash
$ python manage.py makemigrations
Migrations for 'blog':
  blog/migrations/0002_comment_user_alter_comment_author.py
    + Add field user to comment
    ~ Alter field author on comment
```

### Generated Migration File

```python
# blog/migrations/0002_comment_user_alter_comment_author.py

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

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

### What Each Part Means

**dependencies**
```python
dependencies = [
    migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ('blog', '0001_initial'),
]
```
This migration depends on:
1. User model existing (from auth app)
2. Previous blog migration (0001_initial) being applied

**operations**
```python
operations = [
    migrations.AddField(...),
    migrations.AlterField(...),
]
```
Changes to apply in order:
1. Add `user` field
2. Make `author` field optional

### Running migrate

```bash
$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, blog, contenttypes, sessions
Running migrations:
  Applying blog.0002_comment_user_alter_comment_author... OK
```

### SQL Generated

To see SQL without running it:
```bash
python manage.py sqlmigrate blog 0002
```

```sql
BEGIN;
--
-- Add field user to comment
--
ALTER TABLE "blog_comment" 
ADD COLUMN "user_id" integer NULL 
REFERENCES "auth_user" ("id") 
ON DELETE SET NULL;

CREATE INDEX "blog_comment_user_id_abc123" 
ON "blog_comment" ("user_id");
--
-- Alter field author on comment
--
-- (Depends on database - SQLite doesn't actually enforce constraints here)
--
COMMIT;
```

## Migration History Tracking

### django_migrations Table

Django tracks applied migrations:

```sql
SELECT * FROM django_migrations;
```

```
id | app  | name                                   | applied
---+------+----------------------------------------+------------
1  | contenttypes | 0001_initial                | 2026-02-07
2  | auth         | 0001_initial                | 2026-02-07
3  | admin        | 0001_initial                | 2026-02-07
4  | sessions     | 0001_initial                | 2026-02-07
5  | blog         | 0001_initial                | 2026-02-07
6  | blog         | 0002_comment_user_alter...  | 2026-02-07
```

This prevents re-running migrations.

## Common Migration Commands

### Check migration status

```bash
python manage.py showmigrations
```

```
admin
 [X] 0001_initial
 [X] 0002_logentry_remove_auto_add
auth
 [X] 0001_initial
 [X] 0002_alter_permission_name_max_length
blog
 [X] 0001_initial
 [X] 0002_comment_user_alter_comment_author
sessions
 [X] 0001_initial
```

`[X]` = applied, `[ ]` = pending

### Migrate specific app

```bash
python manage.py migrate blog
```

### Migrate to specific migration

```bash
# Go back to migration 0001
python manage.py migrate blog 0001
```

### Fake migration (mark as applied without running)

```bash
python manage.py migrate blog 0002 --fake
```

Useful when manually modifying database.

### Show SQL

```bash
python manage.py sqlmigrate blog 0002
```

### Create empty migration

```bash
python manage.py makemigrations --empty blog
```

For custom data migrations.

## Types of Migrations

### Schema Migrations (Automatic)

Changes to model structure:

```python
# Add field
operations = [
    migrations.AddField(
        model_name='post',
        name='slug',
        field=models.SlugField(),
    ),
]

# Remove field
operations = [
    migrations.RemoveField(
        model_name='post',
        name='old_field',
    ),
]

# Rename field
operations = [
    migrations.RenameField(
        model_name='post',
        old_name='content',
        new_name='body',
    ),
]

# Create model
operations = [
    migrations.CreateModel(
        name='Tag',
        fields=[
            ('id', models.BigAutoField(primary_key=True)),
            ('name', models.CharField(max_length=50)),
        ],
    ),
]

# Delete model
operations = [
    migrations.DeleteModel(name='Tag'),
]
```

### Data Migrations (Manual)

Modifying data, not structure:

```python
# blog/migrations/0003_populate_slugs.py

def populate_slugs(apps, schema_editor):
    Post = apps.get_model('blog', 'Post')
    for post in Post.objects.all():
        post.slug = post.title.lower().replace(' ', '-')
        post.save()

def reverse_populate_slugs(apps, schema_editor):
    # Reverse operation (for rollback)
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0002_add_slug_field'),
    ]

    operations = [
        migrations.RunPython(populate_slugs, reverse_populate_slugs),
    ]
```

Create with:
```bash
python manage.py makemigrations --empty blog
```

Then edit the file manually.

## Migration Best Practices

### 1. Always Review Generated Migrations

```bash
python manage.py makemigrations
# Check the file in blog/migrations/
# Read the operations
# Run sqlmigrate to see SQL
python manage.py migrate
```

### 2. Don't Edit Applied Migrations

If migration already applied to database:
- Create new migration instead of editing
- Exception: Development database (can reset)

### 3. Version Control

Commit migration files to git:
```bash
git add blog/migrations/0002_*.py
git commit -m "Add user field to Comment"
```

Team members run:
```bash
git pull
python manage.py migrate
```

### 4. Test Migrations

```bash
# Test forward
python manage.py migrate blog 0002

# Test backward
python manage.py migrate blog 0001

# Test forward again
python manage.py migrate blog 0002
```

### 5. Squashing Migrations

After many migrations accumulate:

```bash
python manage.py squashmigrations blog 0001 0005
```

Combines multiple migrations into one.

## Handling Existing Data

### Adding Non-Nullable Field

```python
# Problem: What value for existing rows?
class Post(models.Model):
    author = models.ForeignKey(User)  # No null=True!
```

**Solutions:**

**Option 1: Two-step migration**
```python
# Step 1: Add as nullable
author = models.ForeignKey(User, null=True)
# Migrate
# Step 2: Populate data
# Step 3: Make non-nullable
author = models.ForeignKey(User)
```

**Option 2: Provide default**
```python
author = models.ForeignKey(User, default=1)
```

**Option 3: Make nullable**
```python
author = models.ForeignKey(User, null=True, blank=True)
```

### Our Approach

We used nullable ForeignKey:
```python
user = models.ForeignKey(User, null=True, blank=True)
```

**Allows:**
- Existing comments: `user=NULL`
- New comments: `user=actual_user`
- Backward compatible

## Troubleshooting

### "No changes detected"

```bash
$ python manage.py makemigrations
No changes detected
```

**Causes:**
- No model changes
- App not in INSTALLED_APPS
- Models not in models.py

### Conflicting migrations

```
CommandError: Conflicting migrations detected
```

**Cause:** Multiple migration files with same number

**Fix:**
```bash
# Delete conflicting file
rm blog/migrations/0002_conflicting.py
# Regenerate
python manage.py makemigrations
```

### Database out of sync

```
django.db.migrations.exceptions.InconsistentMigrationHistory
```

**Fix:**
```bash
# Mark migrations as applied without running
python manage.py migrate --fake blog 0002
```

### Reset migrations (development only!)

```bash
# Delete database
rm db.sqlite3

# Delete migrations
rm blog/migrations/0*.py

# Recreate
python manage.py makemigrations
python manage.py migrate
```

**WARNING:** Destroys all data!

## Summary

- **makemigrations** - Creates migration files from model changes
- **migrate** - Applies migrations to database
- Migration files track in version control
- django_migrations table tracks what's applied
- Can migrate forward and backward
- Use RunPython for data migrations
- Always review generated migrations
- Test migrations can rollback
- Nullable fields easier for existing data
