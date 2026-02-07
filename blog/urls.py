from django.urls import path  # type: ignore
from . import views 

urlpatterns = [
    path('', views.blog_index, name='blog_index'),
    path('post/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('category/<str:category>/', views.blog_category, name='blog_category'),
]