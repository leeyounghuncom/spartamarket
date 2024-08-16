from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.urls import reverse
from django import forms
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ()


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = [
            "first_name",
            "email",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.fields.get("password"):
            password_help_text = (
                "You can change the password " '<a href="{}">here</a>.'
            ).format(f"{reverse('accounts:change_password')}")
            self.fields["password"].help_text = password_help_text

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image']