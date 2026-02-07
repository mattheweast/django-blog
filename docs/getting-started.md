# Getting Started

First-time setup guide for the Django blog project.

## Prerequisites

- **Python 3.8+** installed
- **pip** package manager
- **Git** (optional, for version control)
- Basic command line knowledge

## Initial Setup

### 1. Clone/Download Project

```bash
# If using git
git clone <repository-url>
cd django-blog

# Or download and extract ZIP, then navigate to folder
cd django-blog
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# You should see (venv) in your prompt
```

**Why?** Isolates project dependencies from your system Python.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Installs:**
- Django 6.0.2
- python-dotenv 1.2.1

### 4. Environment Variables

Create `.env` file in project root:

```bash
# Create .env file
touch .env

# Add your secret key
echo "SECRET_KEY=your-secret-key-here" >> .env
```

**Generate a secret key:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Your .env should look like:**
```
SECRET_KEY=django-insecure-abc123xyz...
```

### 5. Database Setup

```bash
# Create database tables
python manage.py migrate
```

**This creates:**
- User authentication tables
- Blog tables (Post, Category, Comment)
- Session tables
- Admin tables

### 6. Create Admin Account

```bash
python manage.py createsuperuser
```

**You'll be prompted for:**
- Username (e.g., "admin")
- Email (optional, can leave blank)
- Password (type carefully, won't show characters)

### 7. Run Development Server

```bash
python manage.py runserver
```

**Visit:**
- **Homepage:** http://localhost:8000/
- **Admin:** http://localhost:8000/admin/

**Stop server:** Press `Ctrl+C`

## Verify Setup

### Check Homepage
Visit http://localhost:8000/ - should see "Welcome to My Blog" (may be empty of posts)

### Check Admin
1. Visit http://localhost:8000/admin/
2. Log in with superuser credentials
3. Should see Blog section with Posts, Categories, Comments

### Check Authentication
1. Visit http://localhost:8000/register/
2. Should see registration form
3. Visit http://localhost:8000/accounts/login/
4. Should see login form

## Next Steps

### Add Sample Data

**Via Admin Interface:**
1. Go to http://localhost:8000/admin/
2. Add some Categories (Python, Django, Tutorial)
3. Add a Post (select categories)
4. View post on homepage

**Via Django Shell:**
```bash
python manage.py shell
```

```python
from blog.models import Category, Post

# Create categories
python = Category.objects.create(name="Python")
django = Category.objects.create(name="Django")

# Create post
post = Post.objects.create(
    title="Getting Started with Django",
    body="Django is a powerful web framework..."
)
post.categories.add(python, django)

# Verify
print(Post.objects.count())  # Should show 1
```

Exit shell: `exit()` or `Ctrl+D`

### Create Regular User

1. Visit http://localhost:8000/register/
2. Create a test account
3. Log in
4. Try commenting on a post

## Common Issues

### "No module named 'django'"
**Fix:** Activate virtual environment
```bash
source venv/bin/activate
```

### "SECRET_KEY not found"
**Fix:** Create `.env` file with SECRET_KEY (see step 4)

### Port 8000 already in use
**Fix:** Use different port
```bash
python manage.py runserver 8080
```

### Database locked
**Fix:** Make sure only one runserver is running

### Static files not loading
**Fix:** In development, Django serves them automatically. Make sure `DEBUG=True` in settings.

## Development Workflow

**Daily workflow:**
```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Start development server
python manage.py runserver

# 3. Make changes to code
# Server auto-reloads on file changes

# 4. If you change models:
python manage.py makemigrations
python manage.py migrate

# 5. Stop server when done
# Ctrl+C
```

## Project Structure

```
django-blog/
├── manage.py              # Django CLI tool
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (create this)
├── db.sqlite3            # Database (created by migrate)
├── venv/                 # Virtual environment (create this)
│
├── personal_blog/        # Project configuration
│   ├── settings.py       # Main settings
│   ├── urls.py          # Root URL routing
│   └── templates/       # Project-wide templates
│       ├── base.html    # Base template
│       └── registration/ # Auth templates
│
├── blog/                # Blog app
│   ├── models.py        # Database models
│   ├── views.py         # View functions
│   ├── urls.py          # Blog URLs
│   ├── forms.py         # Form classes
│   ├── admin.py         # Admin configuration
│   ├── templates/       # Blog templates
│   └── migrations/      # Database migrations
│
└── docs/                # Documentation
    ├── README.md        # Documentation index
    ├── blog-basics/     # Core features docs
    └── authentication/  # Auth system docs
```

## Learning Path

After setup, explore the documentation:

1. **[Blog Basics Overview](blog-basics/01-overview.md)** - Understand the architecture
2. **[Models](blog-basics/02-models.md)** - Learn about database structure
3. **[Views](blog-basics/03-views.md)** - Understand request handling
4. **[Templates](blog-basics/04-templates.md)** - Learn template language
5. **[Authentication](authentication/01-overview.md)** - Understand auth system

## Quick Commands Reference

```bash
# Virtual environment
source venv/bin/activate        # Activate
deactivate                      # Deactivate

# Development
python manage.py runserver      # Start server
python manage.py runserver 8080 # Custom port

# Database
python manage.py makemigrations # Create migrations
python manage.py migrate        # Apply migrations
python manage.py showmigrations # List migrations

# Users
python manage.py createsuperuser # Create admin
python manage.py changepassword <username> # Change password

# Utilities
python manage.py shell          # Django shell
python manage.py check          # Check for issues
python manage.py dbshell        # Database shell

# Testing
python manage.py test           # Run tests
```

## Git Workflow (Optional)

If using version control:

```bash
# Initial commit
git init
git add .
git commit -m "Initial Django blog setup"

# Make sure .env and other sensitive files are ignored
# Check .gitignore includes:
# .env
# db.sqlite3
# venv/
# __pycache__/
# *.pyc
```

## Getting Help

- **Django Documentation:** https://docs.djangoproject.com/
- **Project Documentation:** See [docs/README.md](README.md)
- **Django Tutorial:** https://docs.djangoproject.com/en/stable/intro/tutorial01/

## What's Next?

You now have a working Django blog! Here's what you can do:

**Explore the admin:**
- Add posts, categories, and manage users
- See how Django's admin auto-generates interfaces

**Try the features:**
- Register a new user
- Log in and add comments
- Browse posts by category

**Read the documentation:**
- Understand how each component works
- Learn Django concepts and patterns
- See how authentication is implemented

**Customize the project:**
- Modify templates (in `blog/templates/`)
- Add new features
- Experiment with the code

Happy coding! 🚀
