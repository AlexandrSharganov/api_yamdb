from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from .utils import CurrentTitleDefault


from reviews.models import Titles, Genres, Categories, User, Review, Comment, GenreTitle


User = get_user_model()


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=256)

    class Meta:
        model = User
        fields = ('confirmation_code', 'username', )
        required_fields = ('username', 'confirmation_code')


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

    class Meta:
        model = Titles
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
    class Meta:
        model = Titles
        fields = '__all__'



    # def create(self, validated_data):
        # if ('genres' in self.initial_data
        #      and self.initial_data['genres'] is 'string'):
        #      slug = self.initial_data['genres']
        #      genre_object = get_object_or_404(Genres, slug=slug)
        #      genre_name = genre_object.name
        #      self.initial_data['genres'] = {
        #         'name': genre_name,
        #         'slug': slug,
        #      }
        # genres = validated_data.pop('genres')
        # title = Titles.objects.create(**validated_data)

        # for genre in genres:
        #     current_genre, status = Genres.objects.get_or_create(
        #         **genre)
        #     GenreTitle.objects.create(
        #         genre=current_genre, title=title)
        # return title 











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
