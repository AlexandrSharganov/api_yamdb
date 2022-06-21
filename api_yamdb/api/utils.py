from api_yamdb.settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from reviews.models import Titles

User = get_user_model()

class CurrentTitleDefault:
    requires_context = True

    def __call__(self, serializer_field):
        title_id = serializer_field.context['view'].kwargs.get('title_id')
        return get_object_or_404(Titles, id=title_id)

    def __repr__(self):
        return '%s()' % self.__class__.__name__


def send_verification_mail(email, request):
    confirmation_code = (
        User.objects.get(username=request.data.get('username'))
        .confirmation_code
    )
    subject = 'Регистрация на сайте'
    message = f'Ваш код для подтверждения регистрации: {confirmation_code}'
    from_email = DEFAULT_FROM_EMAIL
    recipient_list = [email, ]
    send_mail(subject, message, from_email, recipient_list)
