from django.forms import ValidationError
from django.utils import timezone as tz

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from .utils import CurrentTitleDefault
from reviews.models import Title, Genres, Categories, User, Review, Comment


class TokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[a-zA-Z0-9@.+-_]*$',
        max_length=150,
    )
    confirmation_code = serializers.CharField()

    def validate_username_for_me(self, data):
        if self.initial_data['username'] == 'me':
            raise ValidationError('Юзернейм не может быть "me"!')
        return data

    class Meta:
        required_fields = ('username', 'confirmation_code',)


class SignUpSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[a-zA-Z0-9@.+-_]*$',
        max_length=150,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    def validate_username(self, data):
        if self.initial_data['username'] == 'me':
            raise ValidationError('Юзернейм не может быть "me"!')
        return data

    def create(self, validated_data):
        validated_data['confirmation_code'] = self.context.get(
            'confirmation_code'
        )
        return User.objects.create(**validated_data)

    class Meta:
        required_fields = ('email', 'username',)


class UsersSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[a-zA-Z0-9@.+-_]*$',
        max_length=150,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    def validate_username_for_me(self, data):
        if self.initial_data['username'] == 'me':
            raise ValidationError('Юзернейм не может быть "me"!')
        return data

    class Meta:
        model = User
        fields = (
            'email', 'username', 'first_name',
            'last_name', 'bio', 'role',
        )


class GenrestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('name', 'slug')


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        exclude = ('id',)


class TitlesSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(required=False)
    genre = GenrestSerializer(
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
        read_only_fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )


class TitlesPostSerializer(serializers.ModelSerializer):
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

    def validate_year(self, value):
        if value > tz.now().year:
            raise serializers.ValidationError(
                'Нельзя указывать будущую дату!'
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
        slug_field='username'
    )
    title = serializers.HiddenField(
        default=CurrentTitleDefault()
    )

    class Meta:
        model = Review
        fields = ('id', 'author', 'title', 'text', 'score', 'pub_date')
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title')
            )
        ]

    def validate_score(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                'Оценка от 1 до 10!')
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'pub_date')
