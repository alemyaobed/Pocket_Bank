from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import (
    Employee, EntityType, BaseEntity, Notification, Document,
    Department, Role,
    )
from .serializers import (
    BaseEntitySerializer, DepartmentSerializer, DocumentSerializer,
    EmployeeSerializer, EntityTypeSerializer, NotificationSerializer,
    RoleSerializer,
    )

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def test_authentication(request):
#     return Response({"message": "You are authenticated!"})

class EntityTypeViewSet(ModelViewSet):
    queryset = EntityType.objects.all()
    serializer_class = EntityTypeSerializer
    # permission_classes = [IsAuthenticated]

class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    # permission_classes = [IsAuthenticated]

class BaseEntityViewSet(ModelViewSet):
    queryset = BaseEntity.objects.all()
    serializer_class = BaseEntitySerializer
    permission_classes = [AllowAny]

class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    # permission_classes = [IsAuthenticated]

class RoleViewSet(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [AllowAny]

class DocumentViewSet(ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    # permission_classes = [IsAuthenticated]

class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    # permission_classes = [IsAuthenticated]
