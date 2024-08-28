from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    EntityTypeViewSet, DepartmentViewSet, BaseEntityViewSet, DocumentViewSet,
    BranchViewSet, EmployeeViewSet, MimicLoginView, RoleViewSet,
    NotificationViewSet, ActivateAccountView, PasswordResetRequestView,
    PasswordResetConfirmView,
)

# Enable custom error handlers only in production
if not settings.DEBUG:
    from .views import custom_400, custom_403, custom_404, custom_500

    handler400 = custom_400
    handler403 = custom_403
    handler404 = custom_404
    handler500 = custom_500


router = DefaultRouter()
router.register(r'entity-types', EntityTypeViewSet)
router.register(r'branches', BranchViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'base-entities', BaseEntityViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'documents', DocumentViewSet)
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate_account'),
    path('auth/password_reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('auth/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    path('mimic-login/', MimicLoginView.as_view(), name='mimic_login'),
    # path('test-auth/', test_authentication, name='test_auth'),
    path('', include(router.urls)),
]
