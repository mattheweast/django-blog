from django.urls import path
from . import views 

urlpatterns = [
    path('', views.blog_index, name='blog_index'),
    path('post/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('category/<str:category>/', views.blog_category, name='blog_category'),
]