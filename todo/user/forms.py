from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.validators import MaxLengthValidator


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={
        'class': 'auth-field',
        'placeholder': 'Login'
    }))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'auth-field',
        'placeholder': 'Password'
    }))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={
        'class': 'auth-field',
        'placeholder': 'Login'
    }), validators=[MaxLengthValidator(50)])
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'auth-field',
        'placeholder': 'Password',
    }))
    password2 = forms.CharField(label='Повтор Пароля', widget=forms.PasswordInput(attrs={
        'class': 'auth-field',
        'placeholder': 'Repeat password',
    }))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2']
