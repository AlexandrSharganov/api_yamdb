from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)


app_name = 'api'

router_v1 = DefaultRouter()

urlpatterns = [
    path('v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('v1/auth/signup/', SignUpViewSet, )
    path('v1/', include(router_v1.urls)),
]
