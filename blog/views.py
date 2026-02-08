from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Post, Category, Comment
from .forms import CommentForm, PostForm


def blog_index(request):
    posts = Post.objects.all().order_by('-created_on')
    categories = Category.objects.all()
    context = {
        'posts': posts,
        'categories': categories
    }
    return render(request, 'blog_index.html', context)


def blog_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {'post': post}
    return render(request, 'blog_detail.html', context)

def blog_category(request, category):
    posts = Post.objects.filter(categories__name__iexact=category).order_by('-created_on')
    context = {
        'category': category,
        'posts': posts
    }
    return render(request, 'blog_category.html', context)

@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect('blog_detail', pk=post.pk)
    else:
        form = PostForm()
    
    return render(request, 'post_new.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('blog_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'post_edit.html', {'form': form, 'post': post})
