from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()

class CustomSignupForm(UserCreationForm):
    full_name = forms.CharField()

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password1', 'password2']

