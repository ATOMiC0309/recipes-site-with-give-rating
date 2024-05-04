from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Recipe, Category, Comment


class RecipeForm(forms.ModelForm):
    """this class is a form for creating and updating a recipe"""
    class Meta:
        model = Recipe
        fields = ["name", "content", "category", "photo", "published"]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Recipe title...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write recipe contents...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'published': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }

        class Meta:
            model = User
            fields = ['username', 'email']


class CategoryForm(forms.ModelForm):
    """this class is a form for creating and updating a category"""

    class Meta:
        model = Category
        fields = ["name", "published"]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Category...'
            }),
            'published': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class LoginForm(AuthenticationForm):
    """this class for login form """

    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'form3Example3'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'form3Example4'
    }))


class RegisterForm(UserCreationForm):
    """this class for register form """

    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'form3Example3'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ['username', 'email']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Comment..'
            })
        }


