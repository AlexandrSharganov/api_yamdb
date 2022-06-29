from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from api_yamdb.settings import DEFAULT_FROM_EMAIL
from reviews.models import Title


class CurrentTitleDefault:
    requires_context = True

    def __call__(self, serializer_field):
        title_id = serializer_field.context['view'].kwargs.get('title_id')
        return get_object_or_404(Title, id=title_id)


def send_verification_mail(email, confirmation_code):
    subject = 'Регистрация на сайте'
    message = f'Ваш код для подтверждения регистрации: {confirmation_code}'
    from_email = DEFAULT_FROM_EMAIL
    recipient_list = [email, ]
    return send_mail(subject, message, from_email, recipient_list)
