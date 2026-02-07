from django.shortcuts import render, get_object_or_404, redirect # type: ignore
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
    post = Post.objects.get(pk=pk)
    comments = post.comment_set.all().order_by('-created_on')  # All comments  
    form = CommentForm(request.POST or None)  # Handle form  
    if form.is_valid():  
        comment = form.save(commit=False)  
        comment.post = post  
        comment.save()  
        return redirect('blog_detail', pk=post.pk)  
    context = {
        'post': post,
        'comments': comments,
        'form': form
        }
    return render(request, 'blog_detail.html', context)

def blog_category(request, category):
    posts = Post.objects.filter(category__name__iexact=category).order_by('-created_on')
    context = {
        'category': category,
        'posts': posts
    }
    return render(request, 'blog_category.html', context)