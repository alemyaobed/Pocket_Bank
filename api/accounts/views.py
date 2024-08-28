from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from core.serializers import StatusSerializer
from core.views import BaseViewSet
from .models import (
    Employee, EntityType, BaseEntity, Notification, Document,
    Department, Role, Branch
    )
from .serializers import (
    BaseEntitySerializer, DepartmentSerializer, DocumentSerializer,
    EmployeeSerializer, EntityTypeSerializer, NotificationSerializer,
    RoleSerializer, BranchSerializer,
    )
from rest_framework.views import APIView
from rest_framework import status
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse
from .serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import render
from django.views.generic import TemplateView

class ApiRootView(APIView):
    '''A custom API Root View for accessing all enpoints '''
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({
                'entity-types': '/api/v1/entity-types/',
                'branches': '/api/v1/branches/',
                'departments': '/api/v1/departments/',
                'base-entities': '/api/v1/base-entities/',
                'employees': '/api/v1/employees/',
                'roles': '/api/v1/roles/',
                'documents': '/api/v1/documents/',
                'notifications': '/api/v1/notifications/',
                'accounts': '/api/v1/accounts/',
                'account-types': '/api/v1/account-types/',
                'annual-balances': '/api/v1/annual-balances/',
                'assets': '/api/v1/assets/',
                'asset-types': '/api/v1/asset-types/',
                'audits': '/api/v1/audits/',
                'capitals': '/api/v1/capitals/',
                'capital-types': '/api/v1/capital-types/',
                'expenses': '/api/v1/expenses/',
                'expense-types': '/api/v1/expense-types/',
                'incomes': '/api/v1/incomes/',
                'income-types': '/api/v1/income-types/',
                'interest-rate-types': '/api/v1/interest-rate-types/',
                'investments': '/api/v1/investments/',
                'investment-creditings': '/api/v1/investment-creditings/',
                'investment-types': '/api/v1/investment-types/',
                'liabilities': '/api/v1/liabilities/',
                'liability-types': '/api/v1/liability-types/',
                'loans': '/api/v1/loans/',
                'loan-payments': '/api/v1/loan-payments/',
                'loan-terms': '/api/v1/loan-terms/',
                'loan-types': '/api/v1/loan-types/',
                'statuses': '/api/v1/statuses/',
                'transactions': '/api/v1/transactions/',
                'transaction-directions': '/api/v1/transaction-directions/',
                'transaction-types': '/api/v1/transaction-types/',
                'auth-login': '/api/v1/auth/login/',
                'auth-login-refresh': '/api/v1/auth/login/refresh/',
                'auth-activate': '/api/v1/auth/activate/<uidb64>/<token>/',
                'auth-password-reset': '/api/v1/auth/password_reset/',
                'auth-reset-password-confirm': '/api/v1/auth/reset/<uidb64>/<token>/',
                'mimic-login': '/api/v1/mimic-login/',
            })
        else:
            return Response({
                'message': 'Welcome to the Pocket Bank API. Please log in to view all endpoints.',
                'login': '/api/v1/auth/login/',
            }, status=status.HTTP_401_UNAUTHORIZED)

#####################################################################
## Custom error handlers in production
#####################################################################
def custom_400(request, exception):
    return render(request, '400.html', status=400)

def custom_403(request, exception):
    return render(request, '403.html', status=403)

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)


class MimicLoginView(TemplateView):
    template_name = 'mimic_login.html'


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=PasswordResetRequestSerializer,
        responses={
            200: openapi.Response(description="Password reset link sent to your email."),
            400: openapi.Response(description="User with this email does not exist or invalid request."),
        },
    )
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = BaseEntity.objects.get(email=email)
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = request.build_absolute_uri(reverse('reset_password_confirm', args=[uid, token]))

                # Send password reset email
                subject = "Password Reset"
                message = f"Hi {user.username},\n\nPlease click the link below to reset your password:\n{reset_link}\n\nThank you!"
                send_mail(subject, message, 'noreply@example.com', [user.email])

                return Response({"message": "Password reset link sent to your email."}, status=status.HTTP_200_OK)
            except BaseEntity.DoesNotExist:
                return Response({"message": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=PasswordResetConfirmSerializer,
        responses={
            200: openapi.Response(description="Password reset successfully!"),
            400: openapi.Response(description="Invalid password reset link or missing new password."),
        },
    )
    def post(self, request, uidb64, token):
        serializer = PasswordResetConfirmSerializer(data=request.data)

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = BaseEntity.objects.get(pk=uid)

            if user is not None and default_token_generator.check_token(user, token):
                if not serializer.is_valid():
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                new_password = serializer.validated_data['new_password']

                user.set_password(new_password)
                user.save()

                mimic_login_url = reverse('mimic_login')
                return render(request, 'password_reset_success.html', {'mimic_login_url': mimic_login_url})
            else:
                return render(request, 'password_reset_error.html', status=400)
        except (TypeError, ValueError, OverflowError, BaseEntity.DoesNotExist):
            user = None
            return render(request, 'password_reset_error.html', status=400)



class ActivateAccountView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = BaseEntity.objects.get(pk=uid)

            if user is not None and default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                mimic_login_url = reverse('mimic_login')
                return render(request, 'activation_success.html', {'mimic_login_url': mimic_login_url})
            else:
                return render(request, 'activation_error.html', status=400)
        except (TypeError, ValueError, OverflowError, BaseEntity.DoesNotExist):
            user = None
            return render(request, 'activation_error.html', status=400)


class EntityTypeViewSet(BaseViewSet):
    """
    A viewset for viewing and editing EntityType instances.

    list:
    Return a list of all EntityType instances.

    retrieve:
    Return a specific EntityType instance by its ID.
    """
    queryset = EntityType.objects.select_related('updated_by').all()
    serializer_class = EntityTypeSerializer
    permission_classes = [IsAuthenticated]

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


class DepartmentViewSet(BaseViewSet):
    """
    A viewset for viewing and editing Department instances.

    list:
    Return a list of all Department instances.

    retrieve:
    Return a specific Department instance by its ID.
    """
    queryset = Department.objects.select_related('head_of_department', 'branch').all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

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


class BaseEntityViewSet(BaseViewSet):
    """
    A viewset for viewing and editing BaseEntity instances.

    list:
    Return a list of all BaseEntity instances.

    retrieve:
    Return a specific BaseEntity instance by its ID.
    """

    queryset = BaseEntity.objects.select_related('branch', 'entity_type').all()
    serializer_class = BaseEntitySerializer
    permission_classes = [IsAuthenticated]

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

class BranchViewSet(BaseViewSet):
    """
    A viewset for viewing and editing Branch instances.

    list:
    Return a list of all Branch instances.

    retrieve:
    Return a specific Branch instance by its ID.
    """

    queryset = Branch.objects.select_related('manager').all()
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated]

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

class EmployeeViewSet(BaseViewSet):
    """
    A viewset for viewing and editing Employee instances.

    list:
    Return a list of all Employee instances.

    retrieve:
    Return a specific Employee instance by its ID.
    """
    queryset = Employee.objects.select_related('branch', 'entity_type', 'role', 'department').all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

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

class RoleViewSet(BaseViewSet):
    """
    A viewset for viewing and editing Role instances.

    list:
    Return a list of all Role instances.

    retrieve:
    Return a specific Role instance by its ID.
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]


class DocumentViewSet(BaseViewSet):
    """
    A viewset for viewing and editing Document instances.

    list:
    Return a list of all Document instances.

    retrieve:
    Return a specific Document instance by its ID.
    """
    queryset = Document.objects.select_related('owner').all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

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


class NotificationViewSet(BaseViewSet):
    """
    A viewset for viewing and editing Notification instances.

    list:
    Return a list of all Notification instances.

    retrieve:
    Return a specific Notification instance by its ID.
    """
    queryset = Notification.objects.select_related('recipient', 'status').all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

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
