from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Django Models Notes:

# - Definition: Python classes that define database structure/layout
# - class MyModel(models.Model): → Creates table 'appname_mymodel' 
# - Fields = DB columns (CharField=string, TextField=long text, etc.)
# - Relationships: 
#   * ForeignKey = one-to-many (Comment → Post)
#   * ManyToManyField = many-to-many (Post ↔ Category)
# - Workflow: Write model → makemigrations → migrate → Table created
# - __str__(): Returns human-readable name for admin/print/display

class Category (models.Model):
    # CharField: short text, max_length limits size (DB column)
    name = models.CharField(max_length=30)

    class Meta: # Inner class for model metadata/options
        verbose_name_plural = "categories" # Admin plural name (not "Categories")

    def __str__(self): # Human-readable string in admin/Django shell
        # Translates object to human-readable string (title) for admin/shell/print
        # Without this: shows "<Post object (1)>"; With: shows actual title
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255) # Blog post title
    body = models.TextField() # Long text for post content (no length limit)

    # DateTimeField: auto-set timestamps
    created_on = models.DateTimeField(auto_now_add=True) # Set once on create
    last_modified = models.DateTimeField(auto_now=True) # Update every save

    # ManyToManyField: Post can have multiple Categories, Category multiple Posts
    categories = models.ManyToManyField("Category", related_name="posts")

    def __str__(self):
        # Translates object to human-readable string (title) for admin/shell/print
        # Without this: shows "<Post object (1)>"; With: shows actual title
        return self.title
    
class Comment (models.Model):
    # NEW: Link to actual User account (optional for backward compatibility)
    # null=True: database can store NULL
    # blank=True: form validation allows empty
    # on_delete=SET_NULL: if user deleted, keep the comment but clear the user link
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="comments")
    
    # OLD: Keep for existing comments that were made before authentication
    # This can be removed later after migrating old data
    author = models.CharField(max_length=60, blank=True) # Commenter's name (legacy)
    
    body = models.TextField() # Comment text

    created_on = models.DateTimeField(auto_now_add=True) # Timestamp
    # ForeignKey: One-to-many (Comment belongs to one post)
    # on_delete=CASCADE: Delete comments if post deleted
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    def __str__(self):
        # Display username if available, otherwise use legacy author field
        return self.user.username if self.user else self.author
    