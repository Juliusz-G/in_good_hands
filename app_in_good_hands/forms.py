
# Django
from django import forms
from django.contrib.auth.models import User

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


class ProfileEditForm(forms.ModelForm):
    """User profile update form with password confirmation."""
    first_name = forms.CharField(label='Imię', widget=forms.TextInput())
    last_name = forms.CharField(label='Nazwisko', widget=forms.TextInput())
    username = forms.EmailField(label='Email', widget=forms.EmailInput())
    password = forms.CharField(label='Potwierdź zmiany (hasło)', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

    def clean_password(self):
        """Check that password is correct."""
        password = self.cleaned_data['password']
        assert self.instance is not None
        if not self.instance.check_password(password):
            raise forms.ValidationError("Hasło jest błędne!")

        return password


class UpdatePasswordForm(forms.Form):
    """Change password form, checks current password and two new ones. (validation)"""
    password1 = forms.CharField(validators=[validate_password], label='Nowe hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(validators=[validate_password], label='Powtórz nowe hasło', widget=forms.PasswordInput)
    current = forms.CharField(label='Obecne hasło', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        assert self.instance is not None
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)

    def clean_current(self):
        """Check that current password is correct."""
        password = self.cleaned_data['current']
        assert self.instance is not None
        if not self.instance.check_password(password):
            raise forms.ValidationError("Obecne hasło jest błędne!")

        return password

    def clean(self):
        """Check that new passwords match."""
        cleaned_data = super(UpdatePasswordForm, self).clean()
        if cleaned_data['password1'] != cleaned_data['password2']:
            raise forms.ValidationError("Hasła nie pasują!")
        return cleaned_data

    def save(self, commit=True):
        """If everything is validated, saves a new one."""
        assert self.instance is not None
        self.instance.set_password(self.cleaned_data['password1'])
        if commit:
            self.instance.save()
        return self.instance
