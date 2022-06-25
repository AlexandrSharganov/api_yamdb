from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as django_filters

from rest_framework import mixins
from rest_framework import viewsets, status, permissions, filters
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination


from .permissions import (
    IsModerator, IsAdminOrReadOnly,
    IsAdmin
)
from .paginations import (
    CategoriesPagination,
    GenresPagination, TitlesPagination
)
from .utils import confirmation_code_generator, send_verification_mail
from reviews.models import Title, Genres, Categories, Review, User
from .serializers import (
    TitlesSerializer, GenrestSerializer,
    CategoriesSerializer, TokenSerializer,
    SignUpSerializer, UsersSerializer, ReviewSerializer,
    CommentSerializer, TitlesPostSerializer
)


class SignUpViewSet(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get('email')
            confirmation_code = confirmation_code_generator()
            if User.objects.filter(email=email).exists():
                send_verification_mail(email, request=request)
            serializer.save(confirmation_code=confirmation_code)
            send_verification_mail(email, request=request)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenViewSet(APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.initial_data['username']
        confirmation_code = serializer.initial_data['confirmation_code']
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


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'username',
        'first_name',
        'last_name',
        'role',
    )
    pagination_class = LimitOffsetPagination

    @action(
        detail=False,
        methods=['PATCH', 'GET'],
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        user = get_object_or_404(User, username=request.user.username)
        if request.method == 'GET':
            serializer = UsersSerializer(
                instance=user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = UsersSerializer(
            instance=user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        if request.user.is_superuser or request.user.role == 'admin':
            serializer.save()
        else:
            serializer.save(role=user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GenreFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(field_name='genre__slug')
    category = django_filters.CharFilter(field_name='category__slug')
    year = django_filters.NumberFilter(field_name='year')
    name = django_filters.CharFilter(field_name='name',
                                     lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ('genre', 'category', 'year', 'name')


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    serializer_class = TitlesPostSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = TitlesPagination
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('name',)
    filterset_class = GenreFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitlesSerializer
        return TitlesPostSerializer


class GenresViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenrestSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = GenresPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    ordering_fields = ('slug',)
    lookup_field = 'slug'


class CategoriesViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = CategoriesPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsModerator]

    def title_object(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.title_object().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.title_object())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsModerator]

    def review_object(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'),
                                 title=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.review_object().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.review_object())
