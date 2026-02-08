from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Post, Category, Comment
from .forms import CommentForm

# Create your views here.

# 1. Browser hits URL → personal_blog/urls → blog/urls
# 2. URL pattern matches → TRIGGERS this view function
# 3. View queries Model → passes data to Template  
# 4. render() returns HTML response

# Examples:
# / → blog_index() → blog_index.html (all posts)  
# /post/1/ → blog_detail(pk=1) → blog_detail.html (post #1)

def blog_index(request):
    posts = Post.objects.all() # Get ALL posts
    categories = Category.objects.all()
    context = {
        'posts': posts,
        'categories': categories
        }
    return render(request, 'blog_index.html', context)

def blog_detail(request, pk): #pk from URL pattern
    post = get_object_or_404(Post, pk=pk)
    comments = post.comment_set.all().order_by('-created_on')  # All comments
    
    # Handle comment form - only for authenticated users
    form = None
    if request.user.is_authenticated:  # Check if user is logged in
        if request.method == 'POST':
            form = CommentForm(request.POST)  
            if form.is_valid():  
                comment = form.save(commit=False)  # Don't save yet
                comment.post = post  # Link to current post
                comment.user = request.user  # IMPORTANT: Set the user who wrote comment
                comment.save()  # Now save to database
                return redirect('blog_detail', pk=post.pk)  # Redirect to clear POST data
        else:
            form = CommentForm()  # Empty form for GET request
    
    context = {
        'post': post,
        'comments': comments,
        'form': form  # Will be None if user not logged in
        }
    return render(request, 'blog_detail.html', context)

def blog_category(request, category):
    posts = Post.objects.filter(categories__name__iexact=category).order_by('-created_on')
    context = {
        'category': category,
        'posts': posts
    }
    return render(request, 'blog_category.html', context)

def register(request):
    """
    User registration view.
    - GET: Display empty registration form (UserCreationForm)
    - POST: Validate form, create user, log them in automatically
    
    UserCreationForm provides:
    - username field
    - password1 (password)
    - password2 (password confirmation)
    - Built-in validation (passwords match, strong enough, etc.)
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  # Bind form with submitted data
        if form.is_valid():  # Check validation (passwords match, username unique, etc.)
            user = form.save()  # Create the user in database (password auto-hashed)
            login(request, user)  # Log the user in immediately after registration
            return redirect('blog_index')  # Redirect to homepage
    else:
        form = UserCreationForm()  # Empty form for GET request
    
    return render(request, 'registration/register.html', {'form': form})
