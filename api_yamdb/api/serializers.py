from reviews.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Titles, Genres, Categories



# class TokenSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         token['username'] = user.name
#         token['confirmation_code'] = user.confirmation_code

#         return

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
