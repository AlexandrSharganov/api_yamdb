from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import filters

from .serializers import TokenSerializer
from .paginations import CategoriesPagination, GenresPagination, TitlesPagination

from reviews.models import Titles, Genres, Categories
from .serializers import TitlesSerializer, GenrestSerializer, CategoriesSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = TitlesPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenrestSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = GenresPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = CategoriesPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

class TokenView(APIView):
    serializer_class = TokenSerializer
