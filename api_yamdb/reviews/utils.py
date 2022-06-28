from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils import timezone as tz

from api_yamdb.settings import ALLOWED_SYMBOLS


def validate_username(data):
    RegexValidator(
        regex=ALLOWED_SYMBOLS,
        message="""Имя пользователя может
        содержать буквы, цифры, и @.+-_""",
    )
    if data == 'me':
        raise ValidationError('Имя пользователя не может быть "me"!')
    return data


def validate_date_not_in_future(value):
    if value > tz.now().year:
        raise ValidationError(f'Нельзя указывать будущую дату: {value}!')
    return value
