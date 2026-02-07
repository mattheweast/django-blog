from django.db import models

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
    author = models.CharField(max_length=60) # Commenter's name
    body = models.TextField() # Comment text

    created_on = models.DateTimeField(auto_now_add=True) # Timestamp
    # ForeignKey: One-to-many (Comment belongs to one post)
    # on_delete=CASCADE: Delete comments if post deleted
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    def __str__(self):
        # Translates object to human-readable string (title) for admin/shell/print
        # Without this: shows "<Post object (1)>"; With: shows actual title
        return self.author