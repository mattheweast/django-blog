from django.urls import path
from . import views 

urlpatterns = [
    path('', views.blog_index, name='blog_index'),
    path('post/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('register/', views.register, name='register'),  # Registration page
    path('category/<str:category>/', views.blog_category, name='blog_category'),
]