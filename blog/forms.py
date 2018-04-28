from django import forms

from .models import Post,Tag

class ArticlePostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields = ['title', 'body', 'category', 'tags','author','views']



class TagForm(forms.ModelForm):
    class Meta:
        model=Tag
        fields = ['name']