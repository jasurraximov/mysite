from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class CreateUserForm(UserCreationForm):
    username = forms.CharField(max_length=255, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control from-icon-input', 'pe'
                'placeholder': 'username'}                           
    ))
    first_name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control from-icon-input', 
               'placeholder': 'Ism', 'type': 'text'}                           
    ))
    last_name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control from-icon-input', 
               'placeholder': 'Familiya', 'type': 'text'}                           
    )) 
    password1 = forms.CharField(max_length=255, required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control from-icon-input', 
               'placeholder': 'Parol', 'type': 'password'}                           
    ))     
    password2 = forms.CharField(max_length=255, required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control from-icon-input', 
               'placeholder': 'Parolni tasdiqlash', 'type': 'password'}                           
    )) 

    class Meta:
        model = User
        fields = ['username', 'first_name', 
                  'last_name', 'password1', 'password2']
        

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control from-icon-input', 
               'placeholder': 'user', 'type': 'text'}                      
    ))
    password = forms.CharField(max_length=255, required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control from-icon-input', 
               'placeholder': 'Parol', 'type': 'password'}                           
    )) 

