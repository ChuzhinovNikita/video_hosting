from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .bulma_mixin import BulmaMixin


class RegisterForm(BulmaMixin, UserCreationForm):
    username = forms.CharField(label='Придумайте никнейм')
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Придумайте пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Пароль повторно')
    email = forms.EmailField(label='Введите адрес почты')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(BulmaMixin, AuthenticationForm):
    username = forms.CharField(label='Никнейм')
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')

    class Meta:
        model = User
        fields = ['username', 'password']


class EditProfileForm(BulmaMixin, forms.ModelForm):
    image = forms.ImageField(label='Аватар')
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    username = forms.CharField(label='Никнейм')
    email = forms.EmailField(label='Адрес почты')

    class Meta:
        model = User
        fields = ['image', 'first_name', 'last_name', 'username', 'email']
