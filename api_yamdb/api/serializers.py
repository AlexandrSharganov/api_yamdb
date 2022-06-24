from django.contrib.auth import get_user_model
from django.forms import ValidationError

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from .utils import CurrentTitleDefault, confirmation_code_generator
from reviews.models import Title, Genres, Categories, User, Review, Comment


User = get_user_model()


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=256)
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('confirmation_code', 'username', )
        required_fields = ('username', 'confirmation_code')


class SignUpSerializer(serializers.ModelSerializer):
    def validate_username(self, data):
        if self.initial_data['username'] == 'me':
            raise ValidationError('Username can not be "me"')
        return data
    
    class Meta:
        model = User
        fields = ('email', 'username',)


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email', 'username', 'first_name',
            'last_name', 'bio', 'role',
        )
        required_fields = ('email', 'username',)


class GenrestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('name', 'slug')


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        exclude = ('id',)


class TitlesSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(required=False,)
    genre = GenrestSerializer(
        many=True,
        required=False,
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


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
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
        slug_field='username'
    )
    title = serializers.HiddenField(
        default=CurrentTitleDefault())

    class Meta:
        model = Review
        fields = ('id', 'author', 'title', 'text', 'score', 'pub_date')

        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title')
            )
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
