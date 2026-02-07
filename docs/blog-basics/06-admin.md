# Django Admin Interface

## What is Django Admin?

Django's admin is a built-in web interface for managing database content. It's automatically generated from your models.

**Features:**
- Create, read, update, delete (CRUD) operations
- Search and filtering
- Bulk actions
- User permissions
- Customizable interface

**Access:** `http://localhost:8000/admin/`

**Login:** Superuser account only

## Admin Configuration

**Location:** `blog/admin.py`

```python
from django.contrib import admin
from blog.models import Category, Post, Comment

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
```

**What this does:**
- Makes models visible in admin
- Provides default CRUD interface
- Uses model's `__str__()` for display

**Without registration:**
- Models won't appear in admin
- Can't manage via web interface

## Creating a Superuser

**Command:**
```bash
python manage.py createsuperuser
```

**Prompts:**
```
Username: admin
Email: admin@example.com
Password: ********
Password (again): ********
```

**Result:**
- User with full admin access
- Can access admin interface
- Can manage all models

**Check existing superusers:**
```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User

# List all superusers
User.objects.filter(is_superuser=True)

# Check specific user
user = User.objects.get(username='admin')
print(user.is_superuser)  # True
print(user.is_staff)      # True
```

## Admin Interface Tour

### Login Page

**URL:** `/admin/`

**Credentials:** Superuser username + password

### Dashboard

**After login, you see:**
- List of installed apps
- Models for each app
- Add/Change buttons

**Example:**
```
Django administration

AUTHENTICATION AND AUTHORIZATION
  Groups      + Add | Change
  Users       + Add | Change

BLOG
  Categories  + Add | Change
  Comments    + Add | Change
  Posts       + Add | Change
```

### Model List View

**Click "Posts" → See all posts**

**Features:**
- Table of all objects
- Columns from model fields
- Actions (delete selected)
- Search box (if configured)
- Filters (if configured)

**Default columns:**
- Uses `__str__()` method
- Example: Post title, Comment author

### Add/Edit View

**Click "Add post" or edit existing**

**Features:**
- Form for all model fields
- Field validation
- Save, Save and continue, Save and add another
- Delete button (on edit)

**Field types:**
- CharField → Text input
- TextField → Textarea
- DateTimeField → Date/time picker
- ForeignKey → Dropdown
- ManyToManyField → Multi-select

## Customizing Admin

### Basic Customization

**Instead of:**
```python
admin.site.register(Post)
```

**Use ModelAdmin class:**
```python
from django.contrib import admin
from blog.models import Post

class PostAdmin(admin.ModelAdmin):
    pass

admin.site.register(Post, PostAdmin)
```

**Or decorator:**
```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass
```

### List Display

**Show multiple columns:**

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_on', 'last_modified')
```

**Result:**
```
Title                    | Created on           | Last modified
Getting Started Django   | Jan. 15, 2024, 2 p.m.| Jan. 16, 2024, 3 p.m.
Python Best Practices    | Jan. 10, 2024, 1 p.m.| Jan. 10, 2024, 1 p.m.
```

**Custom methods:**
```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_on', 'comment_count')
    
    def comment_count(self, obj):
        return obj.comment_set.count()
    
    comment_count.short_description = 'Comments'
```

### List Filters

**Add sidebar filters:**

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_on')
    list_filter = ('created_on', 'categories')
```

**Result:**
- Sidebar appears
- Filter by date (Today, Past 7 days, This month, etc.)
- Filter by category

### Search

**Add search box:**

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_on')
    search_fields = ('title', 'body')
```

**Behavior:**
- Search box at top
- Searches title AND body
- Case-insensitive
- Partial matches

**Advanced search:**
```python
search_fields = (
    'title',           # Contains
    '=title',          # Exact match
    '^title',          # Starts with
    '@title',          # Full-text (MySQL/PostgreSQL)
)
```

### Ordering

**Default sorting:**

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    ordering = ('-created_on',)  # Newest first
```

**Click column headers to sort in interface**

### Prepopulated Fields

**Auto-fill slug from title:**

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
```

**Example:**
- Type title: "Hello World"
- Slug auto-fills: "hello-world"

### Date Hierarchy

**Add date navigation:**

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
```

**Result:**
- Date breadcrumbs at top
- Navigate by year → month → day

### Readonly Fields

**Prevent editing:**

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('created_on', 'last_modified')
```

**Use for:**
- Auto-generated fields
- Timestamps
- Calculated values

### Fieldsets

**Organize form layout:**

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Content', {
            'fields': ('title', 'body', 'categories')
        }),
        ('Metadata', {
            'fields': ('created_on', 'last_modified'),
            'classes': ('collapse',)  # Initially collapsed
        }),
    )
    readonly_fields = ('created_on', 'last_modified')
```

**Result:**
- Grouped fields with headers
- Collapsible sections

### Inline Editing

**Edit related objects on same page:**

```python
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1  # Number of empty forms
    fields = ('user', 'body', 'created_on')
    readonly_fields = ('created_on',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
```

**Result:**
- Edit post
- See all comments below
- Add/edit/delete comments without leaving page

**Inline types:**
- **TabularInline** - Table layout (compact)
- **StackedInline** - Stacked layout (one per row)

## Complete Example

**blog/admin.py:**

```python
from django.contrib import admin
from blog.models import Category, Post, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'post_count')
    search_fields = ('name',)
    
    def post_count(self, obj):
        return obj.posts.count()
    
    post_count.short_description = 'Number of Posts'


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ('user', 'author', 'body', 'created_on')
    readonly_fields = ('created_on',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_on', 'last_modified', 'comment_count')
    list_filter = ('created_on', 'categories')
    search_fields = ('title', 'body')
    date_hierarchy = 'created_on'
    ordering = ('-created_on',)
    filter_horizontal = ('categories',)  # Better many-to-many widget
    readonly_fields = ('created_on', 'last_modified')
    inlines = [CommentInline]
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'body')
        }),
        ('Organization', {
            'fields': ('categories',)
        }),
        ('Timestamps', {
            'fields': ('created_on', 'last_modified'),
            'classes': ('collapse',)
        }),
    )
    
    def comment_count(self, obj):
        return obj.comment_set.count()
    
    comment_count.short_description = 'Comments'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('get_author', 'post', 'created_on', 'body_preview')
    list_filter = ('created_on', 'post')
    search_fields = ('body', 'user__username', 'author')
    readonly_fields = ('created_on',)
    
    def get_author(self, obj):
        return obj.user.username if obj.user else obj.author
    
    get_author.short_description = 'Author'
    
    def body_preview(self, obj):
        return obj.body[:50] + '...' if len(obj.body) > 50 else obj.body
    
    body_preview.short_description = 'Preview'
```

## Admin Actions

**Bulk operations on selected items:**

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_on')
    actions = ['make_published', 'make_draft']
    
    def make_published(self, request, queryset):
        updated = queryset.update(status='published')
        self.message_user(request, f'{updated} posts published.')
    
    make_published.short_description = 'Mark selected as published'
    
    def make_draft(self, request, queryset):
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} posts marked as draft.')
    
    make_draft.short_description = 'Mark selected as draft'
```

**How it works:**
1. Select multiple posts
2. Choose action from dropdown
3. Click "Go"
4. Action executes on all selected

**Built-in actions:**
- Delete selected objects

## Permissions

**Django admin respects permissions:**

**Superuser:**
- Full access to everything

**Staff user (is_staff=True):**
- Can access admin
- Permissions controlled by groups

**Regular user:**
- Cannot access admin

**Model permissions (auto-created):**
- `blog.add_post` - Can add posts
- `blog.change_post` - Can edit posts
- `blog.delete_post` - Can delete posts
- `blog.view_post` - Can view posts

**Assign permissions:**
```python
from django.contrib.auth.models import User, Permission

user = User.objects.get(username='editor')
user.is_staff = True  # Required for admin access
user.save()

# Add specific permission
permission = Permission.objects.get(codename='add_post')
user.user_permissions.add(permission)
```

**In admin:**
1. Users → Select user
2. Check "Staff status"
3. Select permissions
4. Save

## Customizing Admin Site

**Change admin site header:**

```python
# blog/admin.py or personal_blog/admin.py
from django.contrib import admin

admin.site.site_header = "My Blog Administration"
admin.site.site_title = "My Blog Admin"
admin.site.index_title = "Welcome to My Blog Admin"
```

**Change admin URL:**

```python
# personal_blog/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("secret-admin/", admin.site.urls),  # Changed from "admin/"
    path("", include("blog.urls")),
]
```

## Shell Management

**Alternative to admin interface:**

```bash
python manage.py shell
```

```python
from blog.models import Post, Category, Comment

# Create post
post = Post.objects.create(
    title="New Post",
    body="Content here"
)

# Add categories
python_cat = Category.objects.get(name="Python")
post.categories.add(python_cat)

# Update post
post.title = "Updated Title"
post.save()

# Delete post
post.delete()

# Bulk operations
Post.objects.filter(created_on__year=2020).delete()
Post.objects.filter(title__contains='draft').update(title='Published')
```

## Admin Best Practices

**1. Always customize list_display:**
```python
list_display = ('title', 'created_on', 'status')  # Good
# Default: Just __str__()  # Basic
```

**2. Add search for text fields:**
```python
search_fields = ('title', 'body')
```

**3. Add filters for dates and foreign keys:**
```python
list_filter = ('created_on', 'categories', 'status')
```

**4. Use readonly_fields for auto fields:**
```python
readonly_fields = ('created_on', 'last_modified', 'id')
```

**5. Use inlines for related objects:**
```python
inlines = [CommentInline]  # Edit comments on post page
```

**6. Organize with fieldsets:**
```python
fieldsets = (
    ('Main', {'fields': ('title', 'body')}),
    ('Meta', {'fields': ('created_on',), 'classes': ('collapse',)}),
)
```

**7. Add custom methods for calculated fields:**
```python
def comment_count(self, obj):
    return obj.comment_set.count()
```

## Debugging Admin

**Model not showing:**
- Check `admin.site.register(Model)`
- Check model is imported
- Check no errors in admin.py

**Can't log in:**
- Verify superuser exists
- Check password
- Ensure `is_staff=True` and `is_superuser=True`

**Changes not appearing:**
- Restart development server
- Clear browser cache
- Check for Python errors

**Foreign key dropdown empty:**
- Check related model has objects
- Check related model has `__str__()` method

## Summary

- Admin provides auto-generated CRUD interface
- Register models with `admin.site.register()`
- Superuser required for access
- Customize with ModelAdmin classes
- `list_display` - Table columns
- `list_filter` - Sidebar filters
- `search_fields` - Search box
- `inlines` - Edit related objects together
- `readonly_fields` - Prevent editing
- `fieldsets` - Organize form layout
- Permissions control access
- Great for data management, not for end users

**The admin is for site administrators to manage content, not for public users.**
