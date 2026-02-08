from django.contrib import admin
from .models import Category, Post, Comment # Import your models

# Register each model in admin interface (shows as sectiopns)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
