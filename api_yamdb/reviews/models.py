from tabnanny import verbose
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.db import models

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator


from .utils import confirmation_code_generator



class User(AbstractUser):

    ANONYMOUS = 'anonymous'
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = [
        (ANONYMOUS, 'anonymous'),
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),

    ]

    role = models.CharField(
        max_length=10,
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
    category = models.ForeignKey(
        Categories, on_delete=models.SET_NULL,
        related_name='titles', blank=True, null=True
    )
    genre = models.ManyToManyField(Genres, through='GenreTitle')
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('name',)


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        Genres,
        on_delete=models.CASCADE,
    )

    class Meta():
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'genre'],
                name='unique_title_genre'
            ),
        ]


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Введите текст отзыва'
    )
    score = models.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        ordering = ('-pub_date',)
        # verbose_name = 'Отзыв'
        # verbose_name_plural = 'Отзывы'
        verbose_name = 'Текст'
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_review'
            )
        ]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(
        verbose_name='Текст коментария',
        help_text='Введите текст комментария',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        ordering = ('-pub_date',)
        # verbose_name = 'Комментарий'
        # verbose_name_plural = 'Комментарий к отзыву'
        verbose_name = 'Текст'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.text[:15]
