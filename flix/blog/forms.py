from django import forms
from .models import TVComment , MovieComment
from django.forms import TextInput , EmailInput ,Textarea, NumberInput


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
        widgets = {
            'text': Textarea(attrs={
                'class': "form-control rounded-xl pt-4",
                'style': 'max-width: 500px; ',
                'placeholder': 'Your comment',
                'rows' : 2,
                }),
            'user_email': EmailInput(attrs={
                'class': "form-control rounded-xl pt-4", 
                'style': 'max-width: 300px;',
                'placeholder': 'Your Email'
                }),
            'user_name': TextInput(attrs={
                'class': "form-control rounded-xl pt-4", 
                'style': 'max-width: 300px;',
                'placeholder': 'Your Name'
                }),
            'season': NumberInput(attrs={
                'class': "form-control rounded-xl pt-4", 
                'style': 'width: 400px;',
                'placeholder': 'Enter the Season'
                })
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
        widgets = {
            'text': Textarea(attrs={
                'class': "form-control rounded-xl pt-4",
                'style': 'max-width: 500px; ',
                'placeholder': 'Your comment',
                'rows' : 2,
                }),
            'user_email': EmailInput(attrs={
                'class': "form-control rounded-xl pt-4", 
                'style': 'max-width: 300px;',
                'placeholder': 'Your Email'
                }),
            'user_name': TextInput(attrs={
                'class': "form-control rounded-xl pt-4", 
                'style': 'max-width: 300px;',
                'placeholder': 'Your Name'
                }),

        }
