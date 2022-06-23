from api_yamdb.settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
import reviews.models
from django.utils.crypto import get_random_string


class CurrentTitleDefault:
    requires_context = True

    def __call__(self, serializer_field):
        title_id = serializer_field.context['view'].kwargs.get('title_id')
        return get_object_or_404(reviews.models.Title, id=title_id)

    def __repr__(self):
        return self.__class__.__name__


def confirmation_code_generator():
    return get_random_string(length=10)


def send_verification_mail(email, request):
    confirmation_code = (
        reviews.models.User.objects.get(username=request.data.get('username'))
        .confirmation_code
    )
    subject = 'Регистрация на сайте'
    message = f'Ваш код для подтверждения регистрации: {confirmation_code}'
    from_email = DEFAULT_FROM_EMAIL
    recipient_list = [email, ]
    send_mail(subject, message, from_email, recipient_list)
