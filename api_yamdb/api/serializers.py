from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from .utils import CurrentTitleDefault
from api_yamdb.settings import (CONFIRMATION_CODE_LENGTH, EMAIL_MAX_LENGTH,
                                USERNAME_MAX_LENGTH)
from reviews.models import Categories, Comment, Genres, Review, Title, User
from reviews.utils import validate_date_not_in_future, validate_username


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH,
        validators=[validate_username]
    )
    confirmation_code = serializers.CharField(
        max_length=CONFIRMATION_CODE_LENGTH
    )

    class Meta:
        required_fields = ('username', 'confirmation_code',)


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH,
        validators=[validate_username]
    )

    email = serializers.EmailField(
        max_length=EMAIL_MAX_LENGTH,
    )

    class Meta:
        required_fields = ('email', 'username',)


class UserSerializer(serializers.ModelSerializer):
    def validate_username(self, data):
        return validate_username(data)

    class Meta:
        model = User
        fields = (
            'email', 'username', 'first_name',
            'last_name', 'bio', 'role',
        )


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=False)
    genre = GenreSerializer(
        many=True,
        required=False,
    )
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        read_only_fields = ('__all__',)


class TitlePostSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all(),
        required=False
    )
    genre = SlugRelatedField(
        slug_field='slug',
        queryset=Genres.objects.all(),
        many=True,
        required=False
    )
    year = serializers.IntegerField(
        validators=[validate_date_not_in_future]
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
        slug_field='username'
    )
    title = serializers.HiddenField(
        default=CurrentTitleDefault()
    )
    score = serializers.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1),
        ]
    )

    class Meta:
        model = Review
        fields = ('id', 'author', 'title', 'text', 'score', 'pub_date')
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title')
            ),
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'pub_date')
