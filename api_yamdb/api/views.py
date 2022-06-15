from rest_framework import viewsets
from rest_framework.views import APIView

from .serializers import TokenSerializer

from reviews.models import Titles, Genres, Categories
from .serializers import TitlesSerializer, GenrestSerializer, CategoriesSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenrestSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class TokenView(APIView):
    serializer_class = TokenSerializer
