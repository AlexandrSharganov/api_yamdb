from tabnanny import verbose
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.db import models

from .utils import confirmation_code_generator


class User(AbstractUser):
    ANONYMOUS = 'ANON'
    USER = 'USER'
    MODERATOR = 'MOD'
    ADMIN = 'ADM'
    ROLES = [ 
        (ANONYMOUS, 'Anonymous'),
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin'),
    ]
    
    role = models.CharField(
        max_length=4,
        choices=ROLES,
        default=USER,
    )

    bio = models.TextField(
        'Биография',
        blank=True,
    )

    email = models.EmailField(
        verbose_name='электронная почта',
        max_length=255,
        unique=True,
    )
    
    confirmation_code = models.CharField(
        verbose_name='код подтверждения',
        max_length=10,
        default=confirmation_code_generator(),
    )

    def __str__(self):
        return self.username


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ('name',)


class Genres(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ('name',)


class Titles(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ForeignKey(
        Genres, on_delete=models.SET_NULL,
        related_name='titles', blank=True, null=True
    )
    category = models.ForeignKey(
        Categories, on_delete=models.SET_NULL,
        related_name='titles', blank=True, null=True
    )

    class Meta:
        ordering = ('name',)
