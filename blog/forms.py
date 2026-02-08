from django import forms
from .models import Comment, Post, Category


class CommentForm(forms.ModelForm):  
    class Meta:  
        model = Comment  
        fields = ("body",)  # Only body field - user comes from request.user
        widgets = {
            "body": forms.Textarea(attrs={"rows": 3}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "body", "categories")
        widgets = {
            "body": forms.Textarea(attrs={"rows": 10}),
            "categories": forms.CheckboxSelectMultiple(),
        }
