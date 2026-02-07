# Django Blog

A simple personal blog built with Django, featuring user authentication, post management, and a commenting system. Great for learning Django or as a starting point for small personal sites.

## Features

- 🔐 **User Authentication** - Registration, login, logout
- 📝 **Blog Posts** - Create and organize posts with categories
- 💬 **Comments** - Authenticated users can comment on posts
- ⚙️ **Admin Interface** - Manage all content via Django admin
- 🎨 **Clean UI** - Styled with Simple.css

## Quick Start

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
echo "SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')" > .env

# Set up database
python manage.py migrate

# Create admin account
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

Visit http://localhost:8000/ to see your blog!

## Documentation

📚 **[Complete Documentation](docs/README.md)** - Comprehensive guides covering all aspects of the project

**Quick Links:**
- [Getting Started Guide](docs/getting-started.md) - Detailed setup instructions
- [Blog Basics](docs/blog-basics/) - Understanding core features (Models, Views, Templates, URLs)
- [Authentication System](docs/authentication/) - How user authentication works
- [Admin Interface](docs/blog-basics/06-admin.md) - Managing content
- [Database Queries](docs/blog-basics/07-queries.md) - Working with the ORM

## Project Structure

```
django-blog/
├── manage.py                    # Django CLI
├── personal_blog/              # Project settings
│   ├── settings.py            # Configuration
│   ├── urls.py                # Root routing
│   └── templates/             # Base templates
├── blog/                       # Blog application
│   ├── models.py              # Database models
│   ├── views.py               # Request handlers
│   ├── urls.py                # Blog routing
│   ├── forms.py               # Form definitions
│   └── templates/             # Blog templates
└── docs/                       # Documentation
```

## Technology Stack

- **Django 6.0.2** - Web framework
- **SQLite3** - Database
- **Python 3.8+** - Programming language
- **Django Auth** - Built-in authentication
- **Simple.css** - CSS framework

## Usage

### Admin Interface
Access at http://localhost:8000/admin/ with your superuser credentials to:
- Create and edit blog posts
- Manage categories
- Moderate comments
- Manage users

### User Features
- **Register:** http://localhost:8000/register/
- **Login:** http://localhost:8000/accounts/login/
- **Browse Posts:** http://localhost:8000/
- **Comment:** Available on post detail pages (requires login)

## Development

**Run development server:**
```bash
python manage.py runserver
```

**Apply database migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

**Access Django shell:**
```bash
python manage.py shell
```

**Run tests:**
```bash
python manage.py test
```

## Learning Resources

This project is designed as a learning resource. The documentation includes:
- Step-by-step explanations of Django concepts
- Code walkthroughs with comments
- SQL equivalents for ORM queries
- Request flow diagrams
- Best practices and conventions

Start with the [Getting Started Guide](docs/getting-started.md) and explore the documentation!

## Security Notes

⚠️ **Important for production:**
- Generate a new `SECRET_KEY` and never commit it
- Set `DEBUG = False` in production
- Configure proper database (PostgreSQL, MySQL)
- Set up HTTPS
- Configure allowed hosts in settings
- Use secure session cookies

## Contributing

This is an educational project, but improvements to documentation and code are welcome! Feel free to:
- Report issues
- Suggest improvements
- Submit pull requests
- Use as a learning resource

## License

This project is intended for educational purposes. Feel free to use it as a starting point for your own projects.

## Support

- 📖 [Project Documentation](docs/README.md)
- 🐛 Issues: Use GitHub issues for bugs and questions
- 💡 Django Docs: https://docs.djangoproject.com/ 
