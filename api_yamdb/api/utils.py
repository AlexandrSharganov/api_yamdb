from api_yamdb.settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

User = get_user_model()


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
