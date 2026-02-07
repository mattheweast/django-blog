# Django Blog Documentation

Complete documentation for understanding and working with this Django blog project.

## 📚 Documentation Sections

### Getting Started
- **[Getting Started Guide](getting-started.md)** - First-time setup and installation

### Core Features
- **[Blog Basics](blog-basics/)** - Original blog features (Posts, Categories, Comments)
  - [Overview](blog-basics/01-overview.md) - Architecture and request flow
  - [Models](blog-basics/02-models.md) - Database models
  - [Views](blog-basics/03-views.md) - Request handling
  - [Templates](blog-basics/04-templates.md) - HTML rendering
  - [URLs](blog-basics/05-urls.md) - Routing
  - [Admin](blog-basics/06-admin.md) - Admin interface
  - [Queries](blog-basics/07-queries.md) - ORM database queries

### Authentication System
- **[Authentication](authentication/)** - User authentication features
  - [Overview](authentication/01-overview.md) - Authentication concepts
  - [URL Configuration](authentication/02-url-configuration.md) - Auth routing
  - [Settings](authentication/03-settings.md) - Configuration
  - [Models](authentication/04-models.md) - User model
  - [Views](authentication/05-views.md) - Auth views
  - [Templates](authentication/06-templates.md) - Auth templates
  - [Forms](authentication/07-forms.md) - Form handling
  - [Request Flow](authentication/08-request-flow.md) - Complete examples
  - [Security](authentication/09-security.md) - Security features
  - [Migrations](authentication/10-migrations.md) - Database changes

## 🎯 Reading Recommendations

**New to the project?**
1. Start with [Getting Started Guide](getting-started.md)
2. Read [Blog Basics Overview](blog-basics/01-overview.md)
3. Explore specific topics as needed

**Want to understand authentication?**
1. Read [Authentication Overview](authentication/01-overview.md)
2. Follow [Request Flow](authentication/08-request-flow.md)
3. Check [Security](authentication/09-security.md)

**Need database help?**
1. [Models](blog-basics/02-models.md) - Understanding models
2. [Queries](blog-basics/07-queries.md) - Working with data

**Working on templates?**
1. [Templates](blog-basics/04-templates.md) - Django template language
2. [Authentication Templates](authentication/06-templates.md) - Auth-specific templates

## 🔍 Quick Reference

### Project Structure
```
django-blog/
├── manage.py              # Django CLI
├── db.sqlite3            # Database
├── requirements.txt      # Dependencies
├── personal_blog/        # Project settings
│   ├── settings.py       # Configuration
│   ├── urls.py          # Root URL routing
│   └── templates/       # Project-wide templates
└── blog/                # Blog app
    ├── models.py        # Database models
    ├── views.py         # Request handlers
    ├── urls.py          # App URL routing
    ├── forms.py         # Form definitions
    ├── admin.py         # Admin config
    └── templates/       # App templates
```

### Key Technologies
- **Django 6.0.2** - Web framework
- **SQLite3** - Database
- **Django Auth** - User authentication
- **Django ORM** - Database abstraction
- **Django Templates** - HTML rendering
- **Simple.css** - CSS framework

### Common Commands
```bash
# Development server
python manage.py runserver

# Database migrations
python manage.py makemigrations
python manage.py migrate

# Admin user
python manage.py createsuperuser

# Django shell
python manage.py shell
```

### URLs
- `/` - Homepage (all posts)
- `/blog/<id>/` - Post detail
- `/blog/category/<name>/` - Category filter
- `/register/` - User registration
- `/accounts/login/` - Login
- `/accounts/logout/` - Logout
- `/admin/` - Admin interface

## 📖 Documentation Philosophy

Each documentation file is designed to:
- **Explain concepts** - Why things work this way
- **Show examples** - Real code from the project
- **Provide context** - How pieces fit together
- **Include SQL equivalents** - Understanding what Django does
- **Offer best practices** - Django conventions

## 🤝 Contributing to Documentation

Found something unclear? See documentation that could be improved? The docs are part of the project and improvements are welcome!

## 📝 Notes

- This documentation reflects the current state of the project (February 2026)
- All examples use Django 6.0.2 syntax
- Focus is on understanding, not just "how-to"
- Each section can be read independently
