from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.utils import timezone as tz

from api_yamdb.settings import DEFAULT_FROM_EMAIL
import reviews.models


class CurrentTitleDefault:
    requires_context = True

    def __call__(self, serializer_field):
        title_id = serializer_field.context['view'].kwargs.get('title_id')
        return get_object_or_404(reviews.models.Title, id=title_id)


def send_verification_mail(email, confirmation_code):
    subject = 'Регистрация на сайте'
    message = f'Ваш код для подтверждения регистрации: {confirmation_code}'
    from_email = DEFAULT_FROM_EMAIL
    recipient_list = [email, ]
    send_mail(subject, message, from_email, recipient_list)


def validate_date_not_in_future(value):
    if value > tz.now().year:
        raise ValidationError(f'Нельзя указывать будущую дату: {value}!')
    return value
