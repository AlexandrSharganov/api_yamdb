from django.core.exceptions import ValidationError
from django.utils import timezone as tz


def validate_username(data):
    if data == 'me':
        raise ValidationError('Имя пользователя не может быть "me"!')
    return data


def validate_date_not_in_future(value):
    if value > tz.now().year:
        raise ValidationError(f'Нельзя указывать будущую дату: {value}!')
    return value


def find_max_len_of_roles(ROLES):
    for i in ROLES:
        return (max(len(j) for j in ROLES[1]))
