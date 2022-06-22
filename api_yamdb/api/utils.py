from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone as tz

from rest_framework import mixins, viewsets, filters

from api_yamdb.settings import DEFAULT_FROM_EMAIL
import reviews.models


class CurrentTitleDefault:
    requires_context = True

    def __call__(self, serializer_field):
        title_id = serializer_field.context['view'].kwargs.get('title_id')
        return get_object_or_404(reviews.models.Title, id=title_id)

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class OnlyNameSlugModel(models.Model):
    """Абстрактная модель из name и slug."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ('name',)
        abstract = True


class OnlyNameSlugView(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """Абстрактная вьюха из name и slug."""
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    ordering_fields = ('slug',)


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



def validate_date_not_in_future(value):
    if value > tz.now().year:
        raise ValidationError('date is in the future')
