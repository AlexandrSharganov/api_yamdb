from django.utils import timezone as tz
from django.core.exceptions import ValidationError

from re import match

from api_yamdb.settings import ALLOWED_SYMBOLS


def validate_username(data):
    if not match(ALLOWED_SYMBOLS, data):
        raise ValidationError(
            ('Имя пользователя может содержать буквы, цифры,'
             'и @.+-_')
        )
    if data == 'me':
        raise ValidationError('Имя пользователя не может быть "me"!')
    return data


def validate_date_not_in_future(value):
    if value > tz.now().year:
        raise ValidationError(f'Нельзя указывать будущую дату: {value}!')
    return value
