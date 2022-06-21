from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from .utils import CurrentTitleDefault


from reviews.models import Titles, Genres, Categories, User, Review, Comment


User = get_user_model()


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=256)

    class Meta:
        model = User
        fields = ('confirmation_code', 'username', )


class SignUpSerializer(serializers.ModelSerializer):
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


class TitlesSerializer(serializers.ModelSerializer):
    genre = SlugRelatedField(
        slug_field='slug',
        queryset=Genres.objects.all(),
    )
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all(),
    )

    class Meta:
        model = Titles
        fields = '__all__'


class GenrestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
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

    def validate(self, data):
        if not 1 <= data['score'] <= 10:
            raise serializers.ValidationError(
                'Оценка от 1 до 10!')
        return data

# class ReviewsSerializer(serializers.ModelSerializer):
    # author = serializers.SlugRelatedField(slug_field='username',
    #                                       read_only=True)
    # score = serializers.IntegerField(min_value=1, max_value=10)

    # def validate(self, data):
    #     title_id = self.context['view'].kwargs.get('title_id')
    #     user = self.context['request'].user
    #     if self.context['request'].method == 'PATCH':
    #         return data
    #     is_review_exists = Review.objects.filter(title=title_id,
    #                                              author=user).exists()
    #     if is_review_exists:
    #         raise serializers.ValidationError('Вы уже оставили отзыв.')
    #     return data

    # class Meta:
    #     model = Review
    #     fields = ('id', 'pub_date', 'author', 'text', 'score')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'review', 'text', 'pub_date')