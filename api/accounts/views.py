from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from core.serializers import StatusSerializer
from .models import (
    Employee, EntityType, BaseEntity, Notification, Document,
    Department, Role, Branch
    )
from .serializers import (
    BaseEntitySerializer, DepartmentSerializer, DocumentSerializer,
    EmployeeSerializer, EntityTypeSerializer, NotificationSerializer,
    RoleSerializer, BranchSerializer,
    )

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def test_authentication(request):
#     """
#     A simple view to test authentication. Returns a success message if the user is authenticated.
#     """
#     return Response({"message": "You are authenticated!"})

class EntityTypeViewSet(ModelViewSet):
    """
    A viewset for viewing and editing EntityType instances.

    list:
    Return a list of all EntityType instances.

    retrieve:
    Return a specific EntityType instance by its ID.
    """
    queryset = EntityType.objects.select_related('updated_by').all()
    serializer_class = EntityTypeSerializer
    # permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific EntityType instance and include full details of the 'updated_by' field.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized data including 'updated_by'.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        # The related objects are already fetched with select_related, so serializing them
        data['updated_by'] = BaseEntitySerializer(instance.updated_by).data if instance.updated_by else None

        return Response(data)

    def list(self, request, *args, **kwargs):
        """
        List all EntityType instances and include full details of the 'updated_by' field for each item.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A list of serialized data including 'updated_by' for each item.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        # Iterate through each item to replace updated_by with the full object
        for item, instance in zip(data, queryset):
            item['updated_by'] = BaseEntitySerializer(instance.updated_by).data if instance.updated_by else None

        return Response(data)


class DepartmentViewSet(ModelViewSet):
    """
    A viewset for viewing and editing Department instances.

    list:
    Return a list of all Department instances.

    retrieve:
    Return a specific Department instance by its ID.
    """
    queryset = Department.objects.select_related('head_of_department', 'branch').all()
    serializer_class = DepartmentSerializer
    # permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific Department instance and include full details of the 'head_of_department' and 'branch' fields.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized data including 'head_of_department' and 'branch'.
        """

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        # The related objects are already fetched with select_related, so serializing them
        data['head_of_department'] = EmployeeSerializer(instance.head_of_department).data if instance.head_of_department else None
        data['branch'] = BranchSerializer(instance.branch).data if instance.branch else None

        return Response(data)

    def list(self, request, *args, **kwargs):
        """
        List all Department instances and include full details of the 'head_of_department' and 'branch' fields for each item.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A list of serialized data including 'head_of_department' and 'branch' for each item.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        # Iterate through each item to replace head_of_department and branch with full objects
        for item, instance in zip(data, queryset):
            item['head_of_department'] = EmployeeSerializer(instance.head_of_department).data if instance.head_of_department else None
            item['branch'] = BranchSerializer(instance.branch).data if instance.branch else None

        return Response(data)


class BaseEntityViewSet(ModelViewSet):
    """
    A viewset for viewing and editing BaseEntity instances.

    list:
    Return a list of all BaseEntity instances.

    retrieve:
    Return a specific BaseEntity instance by its ID.
    """

    queryset = BaseEntity.objects.select_related('branch', 'entity_type').all()
    serializer_class = BaseEntitySerializer
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific BaseEntity instance and include full details of the 'branch' and 'entity_type' fields.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized data including 'branch' and 'entity_type'.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        # The related objects are already fetched with select_related, so serializing them
        data['branch'] = BranchSerializer(instance.branch).data if instance.branch else None
        data['entity_type'] = EntityTypeSerializer(instance.entity_type).data if instance.entity_type else None

        return Response(data)

    def list(self, request, *args, **kwargs):
        """
        List all BaseEntity instances and include full details of the 'branch' and 'entity_type' fields for each item.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A list of serialized data including 'branch' and 'entity_type' for each item.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        # Iterate through each item to replace branch and entity_type with full objects
        for item, instance in zip(data, queryset):
            item['branch'] = BranchSerializer(instance.branch).data if instance.branch else None
            item['entity_type'] = EntityTypeSerializer(instance.entity_type).data if instance.entity_type else None

        return Response(data)

class BranchViewSet(ModelViewSet):
    """
    A viewset for viewing and editing Branch instances.

    list:
    Return a list of all Branch instances.

    retrieve:
    Return a specific Branch instance by its ID.
    """

    queryset = Branch.objects.select_related('manager').all()
    serializer_class = BranchSerializer
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific Branch instance and include full details of the 'manager' field.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized data including 'manager'.
        """

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        # Extract manager object if it exists
        if instance.manager:
            data['manager'] = EmployeeSerializer(instance.manager).data
        else:
            data['manager'] = None

        return Response(data)

    def list(self, request, *args, **kwargs):
        """
        List all Branch instances and include full details of the 'manager' field for each item.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A list of serialized data including 'manager' for each item.
        """

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        # Iterate through each item to replace manager with full object
        for item, instance in zip(data, queryset):
            if instance.manager:
                item['manager'] = EmployeeSerializer(instance.manager).data
            else:
                item['manager'] = None

        return Response(data)

class EmployeeViewSet(ModelViewSet):
    """
    A viewset for viewing and editing Employee instances.

    list:
    Return a list of all Employee instances.

    retrieve:
    Return a specific Employee instance by its ID.
    """
    queryset = Employee.objects.select_related('branch', 'entity_type', 'role', 'department').all()
    serializer_class = EmployeeSerializer
    # permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific Employee instance and include full details of the 'branch', 'entity_type', 'role', and 'department' fields.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized data including 'branch', 'entity_type', 'role', and 'department'.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        # The related objects are already fetched with select_related, so serializing them
        data['branch'] = BranchSerializer(instance.branch).data if instance.branch else None
        data['entity_type'] = EntityTypeSerializer(instance.entity_type).data if instance.entity_type else None
        data['role'] = RoleSerializer(instance.role).data if instance.role else None
        data['department'] = DepartmentSerializer(instance.department).data if instance.department else None

        return Response(data)

    def list(self, request, *args, **kwargs):
        """
        List all Employee instances and include full details of the 'branch', 'entity_type', 'role', and 'department' fields for each item.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A list of serialized data including 'branch', 'entity_type', 'role', and 'department' for each item.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        # Iterate through each item to replace branch, entity_type, role and department with full objects
        for item, instance in zip(data, queryset):
            item['role'] = RoleSerializer(instance.role).data if instance.role else None
            item['department'] = DepartmentSerializer(instance.department).data if instance.department else None
            item['branch'] = BranchSerializer(instance.branch).data if instance.branch else None
            item['entity_type'] = EntityTypeSerializer(instance.entity_type).data if instance.entity_type else None


        return Response(data)

class RoleViewSet(ModelViewSet):
    """
    A viewset for viewing and editing Role instances.

    list:
    Return a list of all Role instances.

    retrieve:
    Return a specific Role instance by its ID.
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [AllowAny]


class DocumentViewSet(ModelViewSet):
    """
    A viewset for viewing and editing Document instances.

    list:
    Return a list of all Document instances.

    retrieve:
    Return a specific Document instance by its ID.
    """
    queryset = Document.objects.select_related('owner').all()
    serializer_class = DocumentSerializer
    # permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific Document instance and include full details of the 'owner' field.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized data including 'owner'.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        # The related objects are already fetched with select_related, so serializing them
        data['owner'] = BaseEntitySerializer(instance.owner).data if instance.owner else None

        return Response(data)

    def list(self, request, *args, **kwargs):
        """
        List all Document instances and include full details of the 'owner' field for each item.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A list of serialized data including 'owner' for each item.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        # Iterate through each item to replace owner with full object
        for item, instance in zip(data, queryset):
            item['owner'] = BaseEntitySerializer(instance.owner).data if instance.owner else None

        return Response(data)


class NotificationViewSet(ModelViewSet):
    """
    A viewset for viewing and editing Notification instances.

    list:
    Return a list of all Notification instances.

    retrieve:
    Return a specific Notification instance by its ID.
    """
    queryset = Notification.objects.select_related('recipient', 'status').all()
    serializer_class = NotificationSerializer
    # permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific Notification instance and include full details of the 'recipient' and 'status' fields.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized data including 'recipient' and 'status'.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        # The related objects are already fetched with select_related, so serializing them
        data['recipient'] = BaseEntitySerializer(instance.recipient).data if instance.recipient else None
        data['status'] = StatusSerializer(instance.status).data if instance.status else None

        return Response(data)

    def list(self, request, *args, **kwargs):
        """
        List all Notification instances and include full details of the 'recipient' and 'status' fields for each item.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A list of serialized data including 'recipient' and 'status' for each item.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        # Iterate through each item to replace recipient and status with full objects
        for item, instance in zip(data, queryset):
            item['recipient'] = BaseEntitySerializer(instance.recipient).data if instance.recipient else None
            item['status'] = StatusSerializer(instance.status).data if instance.status else None

        return Response(data)
