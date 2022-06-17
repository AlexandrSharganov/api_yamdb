from django.urls import path, include

from .views import TitlesViewSet, GenresViewSet, CategoriesViewSet, ReviewViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)


app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('titles', TitlesViewSet, basename='titles')
router_v1.register('genres', GenresViewSet, basename='genres')
router_v1.register('categories', CategoriesViewSet, basename='categories')
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review')
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')

urlpatterns = [
    path('v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('v1/auth/signup/', SignUpViewSet, )
    path('v1/', include(router_v1.urls)),
]
