from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True,
                             help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class EmailAuthenticationForm(AuthenticationForm):
    # Replace the username field with an email field
    username = forms.EmailField(
        label="Email",
        widget=forms.TextInput(attrs={'autofocus': True}),
    )
