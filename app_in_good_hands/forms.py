
# Django
from django import forms
from django.contrib.auth.models import User
from django.shortcuts import redirect

# local Django
from .validators import validate_password

# Create your forms here.


class RegisterForm(forms.ModelForm):
    """Form take username as na email and validates passwords (correctness and recurrence)."""
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'type': "text",
            'name': "first_name",
            'placeholder': "Imię"
        }
    ))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'type': "text",
            'name': "last_name",
            'placeholder': "Nazwisko"
        }
    ))
    username = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'type': "email",
            'name': "username",
            'placeholder': "Email"
        }
    ), help_text='Email musi mieć format: abc@abc.abc')
    password1 = forms.CharField(validators=[validate_password], widget=forms.PasswordInput(
        attrs={
            'type': "password",
            'name': "password1",
            'placeholder': "Hasło"
        }
    ), help_text='Hasło musi mieć minimum 8 znaków. W tym przynajmniej jedną cyfrę i jeden znak specjalny.')
    password2 = forms.CharField(validators=[validate_password], widget=forms.PasswordInput(
        attrs={
            'type': "password",
            'name': "password2",
            'placeholder': "Powtórz hasło"
        }
    ), help_text='Hasło musi być taakie samo jak powyżej.')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')

    def clean_password2(self):
        """Check if two passwords match."""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Hasła nie pasują!")
        return password2

    def save(self, commit=True):
        """Sets password for new user."""
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(forms.ModelForm):
    """Simple login form based on Model."""
    username = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'type': "email",
            'name': "username",
            'placeholder': "Email"
        }
    ), help_text='Email musi mieć format: abc@abc.abc')
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput(
        attrs={
            'type': "password",
            'name': "password",
            'placeholder': "Hasło"
        }
    ), help_text='Hasło musi mieć minimum 8 znaków. W tym przynajmniej jedną cyfrę i jeden znak specjalny.')

    class Meta:
        model = User
        fields = ('username', 'password')