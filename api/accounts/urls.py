from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    EntityTypeViewSet, DepartmentViewSet, BaseEntityViewSet, BranchViewSet,
    EmployeeViewSet, RoleViewSet, DocumentViewSet, NotificationViewSet
)

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
    # path('test-auth/', test_authentication, name='test_auth'),
    path('', include(router.urls)),
]
