from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomSignupForm(UserCreationForm):
    full_name = forms.CharField(required=True)
    username = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.full_name = self.cleaned_data.get('full_name')
        user.username = self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    current_password = forms.CharField(required=False, widget=forms.PasswordInput)
    new_password = forms.CharField(required=False, widget=forms.PasswordInput)
    confirm_password = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["full_name", "username", "email"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username and User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean(self):
        cleaned = super().clean()
        new_password = cleaned.get("new_password")
        confirm = cleaned.get("confirm_password")
        current = cleaned.get("current_password")

        if new_password or confirm:
            if not current:
                self.add_error("current_password", "Please enter your current password.")
            if new_password != confirm:
                self.add_error("confirm_password", "Passwords do not match.")
            if self.user and current and not self.user.check_password(current):
                self.add_error("current_password", "Current password is incorrect.")
        return cleaned
