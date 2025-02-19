from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from .models import User


class LoginUserForm(AuthenticationForm):
    username = forms.EmailField(label="E-mail",
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label="Пароль",
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))


    class Meta:
        model = get_user_model()
        fields = ['email', 'password']


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'roles', 'email', 'password1', 'password2')
    # password = forms.CharField(label="Пароль", widget=forms.PasswordInput())
    # password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput())
    #
    # class Meta:
    #     model = get_user_model()
    #     fields = ['first_name', 'last_name', 'roles', 'email', 'password', 'password2']
    #     labels = {
    #         'email': 'E-mail',
    #         'first_name': 'Имя',
    #         'last_name': 'Фамилия',
    #     }
    #     # widgets = {
    #     #     'email': forms.TextInput(attrs={'class': 'form-input'}),
    #     #     'first_name': forms.TextInput(attrs={'class': 'form-input'}),
    #     #     'last_name': forms.TextInput(attrs={'class': 'form-input'}),
    #     # }
    #
    # def clean_password2(self):
    #     cd = self.cleaned_data
    #     if cd['password'] != cd['password2']:
    #         raise forms.ValidationError("Пароли не совпадают!")
    #     return cd["password"]
    #
    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if get_user_model().objects.filter(email=email).exists():
    #         raise forms.ValidationError("Такой E-mail уже существует")
    #     return email