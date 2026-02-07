from django import forms   # type: ignore
from .models import Comment  


class CommentForm(forms.ModelForm):  
    class Meta:  
        model = Comment  
        fields = ('author', 'body')  
