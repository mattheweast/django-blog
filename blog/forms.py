from django import forms
from .models import Comment  


class CommentForm(forms.ModelForm):  
    class Meta:  
        model = Comment  
        fields = ("body",)  # Only body field - user comes from request.user
        widgets = {
            "body": forms.Textarea(attrs={"rows": 3}),
        }
