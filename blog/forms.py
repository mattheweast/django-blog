from django import forms   # type: ignore
from .models import Comment  


class CommentForm(forms.ModelForm):  
    class Meta:  
        model = Comment  
        fields = ('body',)  # Only body field - user comes from request.user
        # We removed 'author' because logged-in users don't need to type their name
