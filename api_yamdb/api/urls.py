from django.urls import path, include


from .views import (TitlesViewSet, GenresViewSet,
                    CategoriesViewSet, TokenViewSet, SignUpViewSet,
                    UsersViewSet, ReviewViewSet, CommentViewSet)

from rest_framework.routers import DefaultRouter

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('titles', TitlesViewSet, basename='titles')
router_v1.register('genres', GenresViewSet, basename='genres')
router_v1.register('categories', CategoriesViewSet, basename='categories')

router_v1.register(
    # r'^titles/(?P<title_id>\d+)/reviews',
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review')
router_v1.register(
    # r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    # r'titles/(?P<title_id>\d+)/reviews/('
    # r'?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')

router_v1.register('users', UsersViewSet, basename='users')


urlpatterns = [
    path('v1/auth/token/', TokenViewSet.as_view(), name='obtain_token'),
    path('v1/auth/signup/', SignUpViewSet.as_view(), name='signup'),
    path('v1/', include(router_v1.urls)),
]
