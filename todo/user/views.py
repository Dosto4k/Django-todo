from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import generic
from .forms import LoginForm, RegisterUserForm


class LoginUser(LoginView):
    template_name = 'user/LoginUser.html'
    form_class = LoginForm
    extra_context = {
        'title': 'Авторизация',
        'active': 'login'
    }


class RegisterUser(generic.CreateView):
    form_class = RegisterUserForm
    template_name = 'user/RegistrationUser.html'
    success_url = reverse_lazy('user:login')
    extra_context = {
        'title': 'Регистрация',
        'active': 'register'
    }
