
# Django
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

# Create your validators here.


def validate_password(password):
    """Password validator: at lest 8 characters = 6 letters, 1 digit and 1 special character."""
    special_characters = r"""[~!@#$%^&*()_+{}":;'\[]]"""
    if not any(char.isdigit() for char in password):
        raise ValidationError(_('Hasło musi zawierać przynajmniej %(min_length)d cyfrę.') % {'min_length': 1})
    if not any(char.isalpha() for char in password):
        raise ValidationError(_('Hasło musi zawierać przynajmniej %(min_length)d literę.') % {'min_length': 6})
    if not any(char in special_characters for char in password):
        raise ValidationError(_('Hasło musi zawierać przynajmniej %(min_length)d znak specjalny.') % {'min_length': 1})
