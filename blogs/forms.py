from django import forms
from .models import Blog, Comment
from django.contrib.auth import get_user_model
from django_ckeditor_5.widgets import CKEditor5Widget

class BlogCreateForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'summary', 'featured_image', 'content', 'status']
    widgets = {
        'content':CKEditor5Widget(
            config_name='default'
        )
    }


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
    widgets = {
        'content': forms.Textarea(attrs={
            'required': True,
            'placeholder': 'Share your thoughts… (must be logged in to comment)',
            'class':'w-full px-6 py-5 border border-ink-light rounded-xl focus:outline-none focus:ring-2 focus:ring-ink-accent/30 focus:border-ink-accent min-h-[140px] resize-y placeholder-ink-gray/60'
        })
    }