from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.crypto import get_random_string
from rest_framework import viewsets, status, permissions, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import mixins, viewsets, filters
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view

from .permissions import (
    IsModerOrAdminOrReadOnly, IsAdminOrReadOnly, IsAdmin
)
from .paginations import (
    GenresAndCategoriesPagination,
    TitlesPagination
)
from .utils import (
    send_verification_mail
)
from reviews.models import Title, Genres, Categories, Review, User
from .serializers import (
    TitleSerializer, GenreSerializer,
    CategorySerializer, TokenSerializer,
    SignUpSerializer, UserSerializer, ReviewSerializer,
    CommentSerializer, TitlePostSerializer
)
from .filters import GenreFilter


class OnlyNameSlugViewSet(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    """Абстрактная вьюха из name и slug."""
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    ordering_fields = ('slug',)
    pagination_class = GenresAndCategoriesPagination
    permission_classes = (IsAdminOrReadOnly,)


@api_view(['POST'])
@action(
    detail=False,
    permission_classes=(AllowAny,)
)
def signup(request):
    confirmation_code = get_random_string(length=10)
    serializer = SignUpSerializer(
        data=request.data,
        context={'confirmation_code': confirmation_code},
    )
    if serializer.is_valid(raise_exception=True):
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        if (User.objects.filter(email=email).exists()
                or User.objects.filter(username=username).exists()):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer.validated_data['confirmation_code'] = confirmation_code
        User.objects.get_or_create(**serializer.validated_data)
        send_verification_mail(
            email=email,
            confirmation_code=confirmation_code,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
@action(
    detail=False,
    permission_classes=(AllowAny,)
)
def token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
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
    return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
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
            return Response(
                UserSerializer(user).data,
                status=status.HTTP_200_OK
            )

        serializer = UserSerializer(
            instance=user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    serializer_class = TitlePostSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = TitlesPagination
    filter_backends = (filters.SearchFilter, DjangoFilterBackend,
                       filters.OrderingFilter)
    search_fields = ('name',)
    filterset_class = GenreFilter
    ordering_fields = ('name',)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializer
        return TitlePostSerializer


class GenresViewSet(OnlyNameSlugViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer


class CategoriesViewSet(OnlyNameSlugViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsModerOrAdminOrReadOnly]

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
        IsModerOrAdminOrReadOnly]

    def review_object(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'),
                                 title=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.review_object().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.review_object())
