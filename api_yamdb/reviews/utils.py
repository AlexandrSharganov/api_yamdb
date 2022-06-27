from django.core.exceptions import ValidationError


def validate_username(data):
    if data == 'me':
        raise ValidationError('Имя пользователя не может быть "me"!')
    return data
