# Blog Basics Documentation

This folder contains documentation for the core blog features - posts, categories, and comments.

## Quick Links

1. [Overview - Blog Architecture](01-overview.md)
2. [Models - Post, Category, Comment](02-models.md)
3. [Views - Index, Detail, Category](03-views.md)
4. [Templates - Displaying Content](04-templates.md)
5. [URL Routing](05-urls.md)
6. [Admin Interface](06-admin.md)
7. [Django ORM Queries](07-queries.md)

## What's Included

### Core Features
- ✅ Blog posts with title, body, timestamps
- ✅ Categories for organizing posts
- ✅ Comments on posts
- ✅ Admin interface for content management
- ✅ Category filtering
- ✅ Chronological ordering

### Models
- **Post** - Blog articles with categories
- **Category** - Tags/topics for posts
- **Comment** - User comments (now linked to auth)

### Views
- **blog_index** - Homepage showing all posts
- **blog_detail** - Individual post with comments
- **blog_category** - Filter posts by category

### Templates
- **base.html** - Base layout with navigation
- **blog_index.html** - List of posts
- **blog_detail.html** - Post detail page
- **blog_category.html** - Category-filtered posts

## Reading Order

**For beginners:**
Start with [01-overview.md](01-overview.md) to understand the structure, then read in order.

**For Django developers:**
Jump to specific topics as needed.

**Quick reference:**
Use [07-queries.md](07-queries.md) for ORM examples.

## Related Documentation

- [Authentication System](../authentication/README.md) - User login, registration, sessions
- [ARCHITECTURE.md](../../ARCHITECTURE.md) - Overall request flow
