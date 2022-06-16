from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


from reviews.models import Titles, Genres, Categories, User


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
