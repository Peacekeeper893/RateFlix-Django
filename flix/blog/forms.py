from django import forms
from .models import TVComment , MovieComment


class TVCommentForm(forms.ModelForm):
    
    class Meta:
        model = TVComment
        exclude = ["tv"]
        labels = {
            "user_name" : "Your Name",
            "user_email": "Your Email",
            "text": "Your Comment",
            "season": "Enter the Season(Optional)"
        }

class MovieCommentForm(forms.ModelForm):
    
    class Meta:
        model = MovieComment
        exclude = ["movie"]
        labels = {
            "user_name" : "Your Name",
            "user_email": "Your Email",
            "text": "Your Comment"
        }
