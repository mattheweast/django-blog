from django.shortcuts import render # type: ignore
from .models import Post

# Create your views here.

# 1. Browser hits URL → personal_blog/urls → blog/urls
# 2. URL pattern matches → TRIGGERS this view function
# 3. View queries Model → passes data to Template  
# 4. render() returns HTML response

# Examples:
# / → blog_index() → blog_index.html (all posts)  
# /post/1/ → blog_detail(pk=1) → blog_detail.html (post #1)

def blog_index(request):
    posts = Post.object.all() # Get ALL posts
    context = {'posts': posts}
    return render(request, 'blog_index.html', context)

def blog_details(request, pk): #pk from URL pattern
    post = Post.objects.get(pk=pk)
    context = {'post': post}
    return render(request, 'blog_detail.html', context)

def blog_category(request, category):
    posts = Post.objects.filter(category__iexact=category).order_by('-created_on')
    context = {
        'category': category,
        'posts': posts
    }
    return render(request, 'blog_category.html', context)