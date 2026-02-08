from django.contrib import admin
from .models import Category, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_on', 'last_modified')
    list_filter = ('created_on', 'last_modified', 'categories')
    search_fields = ('title', 'body')
    filter_horizontal = ('categories',)
    date_hierarchy = 'created_on'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('get_author', 'post', 'created_on')
    list_filter = ('created_on',)
    search_fields = ('body', 'author', 'user__username')
    raw_id_fields = ('post', 'user')
    
    def get_author(self, obj):
        return obj.user.username if obj.user else obj.author
    get_author.short_description = 'Author'
