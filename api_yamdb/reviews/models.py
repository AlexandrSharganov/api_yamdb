from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MaxValueValidator, MinValueValidator,
)
from django.db import models

from .utils import (
    validate_username, validate_date_not_in_future
)
from api_yamdb.settings import (
    USERNAME_MAX_LENGTH, EMAIL_MAX_LENGTH, CONFIRMATION_CODE_LENGTH,
    FIRST_NAME_MAX_LENGTH, LAST_NAME_MAX_LENGTH
)


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


class User(AbstractUser):

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = [
        (USER, 'пользователь'),
        (MODERATOR, 'важный пользователь, модератор'),
        (ADMIN, 'самый важный пользователь, администратор'),
    ]

    role = models.CharField(
        max_length=max(len(role) for role, _ in ROLES),
        choices=ROLES,
        default=USER,
    )

    bio = models.TextField(
        'Биография',
        blank=True,
    )

    email = models.EmailField(
        verbose_name='электронная почта',
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
    )

    confirmation_code = models.CharField(
        verbose_name='код подтверждения',
        max_length=CONFIRMATION_CODE_LENGTH,
    )
    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        blank=True,
    )
    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        blank=True,
    )
    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        validators=[
            validate_username,
        ]
    )

    def is_administrator(self):
        return (self.role == self.ADMIN
                or self.is_staff
                )

    def is_moderator(self):
        return (self.role == self.MODERATOR)

    def __str__(self):
        return self.username


class Categories(OnlyNameSlugModel):

    class Meta(OnlyNameSlugModel.Meta):
        verbose_name = ('категория')
        verbose_name_plural = ('категории')


class Genres(OnlyNameSlugModel):

    class Meta(OnlyNameSlugModel.Meta):
        verbose_name = ('жанр')
        verbose_name_plural = ('жанры')


class Title(models.Model):
    name = models.TextField()
    year = models.IntegerField(
        validators=[validate_date_not_in_future]
    )
    category = models.ForeignKey(
        Categories, on_delete=models.SET_NULL,
        related_name='titles', blank=True, null=True
    )
    genre = models.ManyToManyField(Genres, through='GenreTitle')
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = ('произведение')
        verbose_name_plural = ('произведения')


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
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
        verbose_name = ('произведения по жанрам')
        verbose_name_plural = ('произведения по жанрам')


class ReviewComment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    text = models.TextField(
        verbose_name='Текст',
        help_text='Введите текст',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]


class Review(ReviewComment):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )
    score = models.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
        verbose_name='Оценка'
    )

    class Meta(ReviewComment.Meta):
        verbose_name = ('отзыв')
        verbose_name_plural = ('отзывы')
        default_related_name = "reviews"
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author'
            )
        ]


class Comment(ReviewComment):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )

    class Meta(ReviewComment.Meta):
        verbose_name = ('комментарий')
        verbose_name_plural = ('комментарии')
        default_related_name = "comments"
