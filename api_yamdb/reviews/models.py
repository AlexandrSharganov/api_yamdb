from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import RegexValidator

from api.utils import OnlyNameSlugModel, validate_date_not_in_future


class User(AbstractUser):

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]

    role = models.CharField(
        max_length=9,
        choices=ROLES,
        default=USER,
    )

    bio = models.TextField(
        'Биография',
        blank=True,
    )

    email = models.EmailField(
        verbose_name='электронная почта',
        max_length=254,
        unique=True,
    )

    confirmation_code = models.CharField(
        verbose_name='код подтверждения',
        max_length=10,
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=(r'^[a-zA-Z0-9@.+-_]*$'),
                message='Username must contain letters, numbers and @.+-_',
            )
        ]
    )

    def is_administrator(self):
        return (self.role == self.ADMIN
                or self.is_staff
                or self.is_superuser)

    def is_moderator(self):
        return (self.role == self.MODERATOR
                or self.role == self.ADMIN
                or self.is_staff
                or self.is_superuser)

    def __str__(self):
        return self.username


class Categories(OnlyNameSlugModel):
    pass


class Genres(OnlyNameSlugModel):
    pass


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


class ReviewComment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name="%(app_label)s_%(class)s_related"
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
        verbose_name = 'Текст'

    def __str__(self):
        return self.text[:15]


class Review(ReviewComment):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    score = models.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
        verbose_name='Оценка'
    )

    class Meta(ReviewComment.Meta):
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
        related_name='comments',
        verbose_name='Отзыв'
    )
