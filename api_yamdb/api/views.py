from django.forms import ModelChoiceField
from django.shortcuts import get_object_or_404

from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as django_filters
# from django_filters import ModelChoiceFilter, FilterSet
from rest_framework import viewsets, status, permissions
from rest_framework.views import APIView
from rest_framework import filters
from rest_framework import mixins

from .paginations import CategoriesPagination, GenresPagination, TitlesPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsAuthorOrModeratorPermission, AdminPermission

from .utils import send_verification_mail
from reviews.models import Titles, Genres, Categories, Comment, Review
from .serializers import (TitlesSerializer, GenrestSerializer,
                          CategoriesSerializer, TokenSerializer,
                          SignUpSerializer, UsersSerializer, ReviewSerializer, CommentSerializer, TitlesPostSerializer)


User = get_user_model()


class SignUpViewSet(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            # Хардкод, пока так
            if request.data.get('username') == 'me':
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()
            send_verification_mail(email, request=request)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenViewSet(APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data['username']
        confirmation_code = serializer.data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if user.confirmation_code != confirmation_code:
            return Response(
                {
                    'confirmation_code': 'Код подтверждения неверный',
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'token': str(refresh.access_token)
            },
            status=status.HTTP_200_OK
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      

class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    get_queryset = User.objects.all()


class GenreFilter(django_filters.FilterSet):
# # class GenreFilter(filters.BaseFilterBackend):
# #     def filter_queryset(self, request, queryset, view):
# #         return queryset.filter(genre=request.titles.genre)
#     genre = ModelChoiceFilter(

#     )
    genre = django_filters.CharFilter(field_name='genre__slug')
    category = django_filters.CharFilter(field_name='category__slug')
    year = django_filters.NumberFilter(field_name='year')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    class Meta:
        model = Titles
        fields = ('genre', 'category', 'year', 'name')


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesPostSerializer
    permission_classes = (AdminPermission,)
    pagination_class = TitlesPagination
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('name',)
    filterset_class  = GenreFilter

    # def get_queryset(self):
    #     genre = self.request.kwargs()
    #     return super().get_queryset()

    def get_serializer_class(self):
        if self.action == 'list':
            return TitlesSerializer
        return TitlesPostSerializer 

    
class GenresViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenrestSerializer
    permission_classes = (AdminPermission,)
    pagination_class = GenresPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    ordering_fields = ('slug',)
    lookup_field = 'slug'


class CategoriesViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (AdminPermission,)
    pagination_class = CategoriesPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrModeratorPermission]

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, id=title_id)
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, id=title_id)
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrModeratorPermission]

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, id=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title)
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, id=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title)
        return Comment.objects.filter(review=review)

