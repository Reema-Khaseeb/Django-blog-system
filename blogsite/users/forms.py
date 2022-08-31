from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    class Meta:
        # Change the User model whenever we save something in this form
        model = User
        fields = ("username", "email", "password1", "password2", )
