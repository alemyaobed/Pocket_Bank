from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import test_authentication, RoleSerializer


router = DefaultRouter()
router.register(r'roles', RoleSerializer)

urlpatterns = [
    path('login/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('test-auth/', test_authentication, name='test_auth'),
    path('', include(router.urls)),
]
