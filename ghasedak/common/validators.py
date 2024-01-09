import re

import phonenumbers
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from phonenumbers import is_possible_number, NumberParseException, is_valid_number


@deconstructible
class DigitValidator(validators.RegexValidator):
    regex = r'^\d+$'
    message = _('should only be comprised of digits.')
    flags = re.ASCII


@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = r'^\w{3,}$'
    message = _(
        'Enter a valid username. This value may contain only English letters, '
        'numbers, and _ character'
    )
    flags = re.ASCII


def phone_number_validator(value: str) -> None:
    try:
        phone_number = phonenumbers.parse(value, 'IR')
    except NumberParseException:
        raise ValidationError(_('Phone number is not valid for Iran'))

    if not is_possible_number(phone_number):
        raise ValidationError(_('This phone number is not possible'))
    if not is_valid_number(phone_number):
        raise ValidationError(_('This phone number is not valid'))
