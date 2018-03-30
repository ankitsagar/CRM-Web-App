from django.contrib.auth.forms import UserChangeForm
from django import forms

from .models import User


class UserForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class SignUpForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'mobile', 'email']


class ResetPasswordForm(forms.Form):
    username = forms.CharField(label='User Name', max_length=100)