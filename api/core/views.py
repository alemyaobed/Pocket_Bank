from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .permissions import IsStaffOrRelated

from accounts.serializers import BaseEntitySerializer, BranchSerializer, EntityTypeSerializer
from accounts.models import BaseEntity, Branch

from .models import (
    Account, AccountType, AnnualBalance, Asset, AssetType, Audit,
    Capital, CapitalType, Expense, ExpenseType, Income, IncomeType,
    InterestRateType, Investment, InvestmentCrediting, InvestmentType,
    Liability, LiabilityType, Loan, LoanPayment, LoanTerms, LoanType,
    Status, Transaction, TransactionDirection, TransactionType
)
from .serializers import (
    AccountSerializer, AccountTypeSerializer, AnnualBalanceSerializer,
    AssetSerializer, AssetTypeSerializer, AuditSerializer,
    CapitalSerializer, CapitalTypeSerializer, ExpenseSerializer, ExpenseTypeSerializer,
    IncomeSerializer, IncomeTypeSerializer, InterestRateTypeSerializer,
    InvestmentSerializer, InvestmentCreditingSerializer, InvestmentTypeSerializer,
    LiabilitySerializer, LiabilityTypeSerializer, LoanSerializer, LoanPaymentSerializer,
    LoanTermsSerializer, LoanTypeSerializer, StatusSerializer, TransactionSerializer,
    TransactionDirectionSerializer, TransactionTypeSerializer
)


class BaseViewSet(ModelViewSet):
    """
    Base ViewSet that provides a standardized delete response.
    """
    def destroy(self, request, *args, **kwargs):
        """
        Handle deletion of an object and return a standardized response.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': f'{self.serializer_class.Meta.model.__name__} deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )

    def perform_destroy(self, instance):
        """
        Perform the actual deletion of the instance.
        """
        instance.delete()


class AccountViewSet(BaseViewSet):
    """
    A viewset for viewing and editing Account instances.

    list:
    Return a list of all Account instances with detailed information including related fields.

    retrieve:
    Return a specific Account instance by its ID with detailed information including related fields.
    """
    queryset = Account.objects.select_related(
        'owner', 'account_type', 'branch', 'status'
    ).all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated, IsStaffOrRelated]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific Account instance and include full details of the related 'owner', 'account_type',
        'branch', and 'status' fields.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized data including 'owner', 'account_type', 'branch', and 'status'.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['owner'] = self.get_base_entity_details(instance.owner)
        data['account_type'] = AccountTypeSerializer(instance.account_type).data if instance.account_type else None
        data['branch'] = BranchSerializer(instance.branch).data if instance.branch else None
        data['status'] = StatusSerializer(instance.status).data if instance.status else None
        data['created_by'] = BaseEntitySerializer(instance.created_by).data if instance.created_by else None
        return Response(data)

    def list(self, request, *args, **kwargs):
        """
        List all Account instances and include full details of the related 'owner', 'account_type',
        'branch', and 'status' fields for each item.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A list of serialized data including 'owner', 'account_type', 'branch', and 'status' for each item.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        for item, instance in zip(data, queryset):
            item['owner'] = self.get_base_entity_details(instance.owner)
            item['account_type'] = AccountTypeSerializer(instance.account_type).data if instance.account_type else None
            item['branch'] = BranchSerializer(instance.branch).data if instance.branch else None
            item['status'] = StatusSerializer(instance.status).data if instance.status else None
            item['created_by'] = BaseEntitySerializer(instance.created_by).data if instance.created_by else None
        return Response(data)

    def get_base_entity_details(self, base_entity):
        """
        Retrieve detailed information of a BaseEntity, including its related fields.

        Args:
            base_entity: The BaseEntity instance to be detailed.

        Returns:
            dict: The serialized data of the BaseEntity including related fields.
        """
        if base_entity:
            serializer = BaseEntitySerializer(base_entity)
            data = serializer.data
            # Assume that BaseEntity has 'branch' and 'entity_type' related fields
            data['branch'] = BranchSerializer(base_entity.branch).data if base_entity.branch else None
            data['entity_type'] = EntityTypeSerializer(base_entity.entity_type).data if base_entity.entity_type else None
            return data
        return None

    def perform_create(self, serializer):
        """
        Perform the creation of the instance and set the 'created_by' field to the current user.

        Args:
            serializer: The serializer instance.
        """
        serializer.save(created_by=self.request.user)

class AccountTypeViewSet(BaseViewSet):
    """
    A viewset for viewing and editing AccountType instances.

    list:
    Return a list of all AccountType instances with detailed information including the related 'updated_by' field.

    retrieve:
    Return a specific AccountType instance by its ID with detailed information including the related 'updated_by' field.
    """
    queryset = AccountType.objects.select_related('updated_by').all()
    serializer_class = AccountTypeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific AccountType instance and include full details of the related 'updated_by' field.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized data including the 'updated_by' field.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        # Serialize the 'updated_by' field if it exists
        if instance.updated_by:
            data['updated_by'] = self.get_base_entity_details(instance.updated_by)
        else:
            data['updated_by'] = None
        return Response(data)

    def list(self, request, *args, **kwargs):
        """
        List all AccountType instances and include full details of the related 'updated_by' field for each item.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A list of serialized data including the 'updated_by' field for each item.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        # Add full details of 'updated_by' field for each item
        for item, instance in zip(data, queryset):
            if instance.updated_by:
                item['updated_by'] = self.get_base_entity_details(instance.updated_by)
            else:
                item['updated_by'] = None
        return Response(data)

    def get_base_entity_details(self, base_entity):
        """
        Retrieve detailed information of a BaseEntity, including its related fields.

        Args:
            base_entity: The BaseEntity instance to be detailed.

        Returns:
            dict: The serialized data of the BaseEntity including related fields.
        """
        if base_entity:
            serializer = BaseEntitySerializer(base_entity)
            data = serializer.data
            # Assume that BaseEntity has 'branch' and 'entity_type' related fields
            data['branch'] = BranchSerializer(base_entity.branch).data if base_entity.branch else None
            data['entity_type'] = EntityTypeSerializer(base_entity.entity_type).data if base_entity.entity_type else None
            return data
        return None

class AnnualBalanceViewSet(BaseViewSet):
    """
    A viewset for viewing and editing `AnnualBalance` instances.

    list:
    Return a list of all `AnnualBalance` instances with detailed information, including the related `branch` field.

    retrieve:
    Return a specific `AnnualBalance` instance by its ID with detailed information, including the related `branch` field.
    """
    queryset = AnnualBalance.objects.select_related('branch').all()
    serializer_class = AnnualBalanceSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific `AnnualBalance` instance and include full details of the related `branch` field.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized data including the `branch` field.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        # Serialize the 'branch' field if it exists
        if instance.branch:
            data['branch'] = self.get_branch_details(instance.branch)
        else:
            data['branch'] = None
        return Response(data)

    def list(self, request, *args, **kwargs):
        """
        List all `AnnualBalance` instances and include full details of the related `branch` field for each item.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A list of serialized data including the `branch` field for each item.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        # Add full details of `branch` field for each item
        for item, instance in zip(data, queryset):
            if instance.branch:
                item['branch'] = self.get_branch_details(instance.branch)
            else:
                item['branch'] = None
        return Response(data)

    def get_branch_details(self, branch):
        """
        Retrieve detailed information of a `Branch`.

        Args:
            branch: The `Branch` instance to be detailed.

        Returns:
            dict: The serialized data of the `Branch`.
        """
        if branch:
            serializer = BranchSerializer(branch)
            return serializer.data
        return None

class AssetViewSet(BaseViewSet):
    """
    A viewset for viewing and editing `Asset` instances.

    list:
    Return a list of all `Asset` instances with detailed information, including related fields like `branch`, `asset_type`, and `status`.

    retrieve:
    Return a specific `Asset` instance by its ID with detailed information, including related fields like `branch`, `asset_type`, and `status`.
    """
    queryset = Asset.objects.select_related('branch', 'asset_type', 'status').all()
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific `Asset` instance and include full details of related fields like `branch`, `asset_type`, and `status`.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized data including related fields.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        # Serialize related fields if they exist
        data['branch'] = self.get_branch_details(instance.branch)
        data['asset_type'] = self.get_asset_type_details(instance.asset_type)
        data['status'] = self.get_status_details(instance.status)
        return Response(data)

    def list(self, request, *args, **kwargs):
        """
        List all `Asset` instances and include full details of related fields like `branch`, `asset_type`, and `status` for each item.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A list of serialized data including related fields for each item.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        # Add full details of related fields for each item
        for item, instance in zip(data, queryset):
            item['branch'] = self.get_branch_details(instance.branch)
            item['asset_type'] = self.get_asset_type_details(instance.asset_type)
            item['status'] = self.get_status_details(instance.status)
        return Response(data)

    def get_branch_details(self, branch):
        """
        Retrieve detailed information of a `Branch`.

        Args:
            branch: The `Branch` instance to be detailed.

        Returns:
            dict: The serialized data of the `Branch`.
        """
        if branch:
            serializer = BranchSerializer(branch)
            return serializer.data
        return None

    def get_asset_type_details(self, asset_type):
        """
        Retrieve detailed information of an `AssetType`.

        Args:
            asset_type: The `AssetType` instance to be detailed.

        Returns:
            dict: The serialized data of the `AssetType`.
        """
        if asset_type:
            serializer = AssetTypeSerializer(asset_type)
            return serializer.data
        return None

    def get_status_details(self, status):
        """
        Retrieve detailed information of a `Status`.

        Args:
            status: The `Status` instance to be detailed.

        Returns:
            dict: The serialized data of the `Status`.
        """
        if status:
            serializer = StatusSerializer(status)
            return serializer.data
        return None


class AssetTypeViewSet(BaseViewSet):
    """
    A viewset for viewing and editing AssetType instances.

    list:
    Return a list of all AssetType instances with detailed information including the related 'updated_by' field.

    retrieve:
    Return a specific AssetType instance by its ID with detailed information including the related 'updated_by' field.
    """
    queryset = AssetType.objects.select_related('updated_by').all()
    serializer_class = AssetTypeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific AssetType instance and include full details of the related 'updated_by' field.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized data including the 'updated_by' field.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        # Serialize the 'updated_by' field if it exists
        if instance.updated_by:
            data['updated_by'] = self.get_base_entity_details(instance.updated_by)
        else:
            data['updated_by'] = None
        return Response(data)

    def list(self, request, *args, **kwargs):
        """
        List all AssetType instances and include full details of the related 'updated_by' field for each item.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A list of serialized data including the 'updated_by' field for each item.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        # Add full details of 'updated_by' field for each item
        for item, instance in zip(data, queryset):
            if instance.updated_by:
                item['updated_by'] = self.get_base_entity_details(instance.updated_by)
            else:
                item['updated_by'] = None
        return Response(data)

    def get_base_entity_details(self, base_entity):
        """
        Retrieve detailed information of a BaseEntity, including its related fields.

        Args:
            base_entity: The BaseEntity instance to be detailed.

        Returns:
            dict: The serialized data of the BaseEntity including related fields.
        """
        if base_entity:
            serializer = BaseEntitySerializer(base_entity)
            data = serializer.data
            # Assume that BaseEntity has 'branch' and 'entity_type' related fields
            data['branch'] = BranchSerializer(base_entity.branch).data if base_entity.branch else None
            data['entity_type'] = EntityTypeSerializer(base_entity.entity_type).data if base_entity.entity_type else None
            return data
        return None


class AuditViewSet(BaseViewSet):
    queryset = Audit.objects.all()
    serializer_class = AuditSerializer
    pagination_class = [IsAuthenticated, IsAdminUser]

class CapitalViewSet(BaseViewSet):
    """
    A viewset for viewing and editing Capital instances.

    list:
    Return a list of all Capital instances with detailed information including related fields.

    retrieve:
    Return a specific Capital instance by its ID with detailed information including related fields.
    """
    queryset = Capital.objects.select_related('branch', 'capital_type', 'status').all()
    serializer_class = CapitalSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific Capital instance and include full details of the related fields.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized data including the related fields.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        # Add full details of related fields
        data['branch'] = BranchSerializer(instance.branch).data if instance.branch else None
        data['capital_type'] = CapitalTypeSerializer(instance.capital_type).data if instance.capital_type else None
        data['status'] = StatusSerializer(instance.status).data if instance.status else None
        return Response(data)

    def list(self, request, *args, **kwargs):
        """
        List all Capital instances and include full details of the related fields for each item.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A list of serialized data including the related fields for each item.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        # Add full details of related fields for each item
        for item, instance in zip(data, queryset):
            item['branch'] = BranchSerializer(instance.branch).data if instance.branch else None
            item['capital_type'] = CapitalTypeSerializer(instance.capital_type).data if instance.capital_type else None
            item['status'] = StatusSerializer(instance.status).data if instance.status else None
        return Response(data)


class CapitalTypeViewSet(BaseViewSet):
    """
    A viewset for viewing and editing CapitalType instances.

    list:
    Return a list of all CapitalType instances with detailed information including the related 'updated_by' field.

    retrieve:
    Return a specific CapitalType instance by its ID with detailed information including the related 'updated_by' field.
    """
    queryset = CapitalType.objects.select_related('updated_by').all()
    serializer_class = CapitalTypeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific CapitalType instance and include full details of the related 'updated_by' field.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized data including the 'updated_by' field.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        # Serialize the 'updated_by' field if it exists
        if instance.updated_by:
            data['updated_by'] = self.get_base_entity_details(instance.updated_by)
        else:
            data['updated_by'] = None
        return Response(data)

    def list(self, request, *args, **kwargs):
        """
        List all CapitalType instances and include full details of the related 'updated_by' field for each item.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A list of serialized data including the 'updated_by' field for each item.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        # Add full details of 'updated_by' field for each item
        for item, instance in zip(data, queryset):
            if instance.updated_by:
                item['updated_by'] = self.get_base_entity_details(instance.updated_by)
            else:
                item['updated_by'] = None
        return Response(data)

    def get_base_entity_details(self, base_entity):
        """
        Retrieve detailed information of a BaseEntity, including its related fields.

        Args:
            base_entity: The BaseEntity instance to be detailed.

        Returns:
            dict: The serialized data of the BaseEntity including related fields.
        """
        if base_entity:
            serializer = BaseEntitySerializer(base_entity)
            data = serializer.data
            # Assume that BaseEntity has 'branch' and 'entity_type' related fields
            data['branch'] = BranchSerializer(base_entity.branch).data if base_entity.branch else None
            data['entity_type'] = EntityTypeSerializer(base_entity.entity_type).data if base_entity.entity_type else None
            return data
        return None


class ExpenseViewSet(BaseViewSet):
    """
    A viewset for viewing and editing Expense instances.

    list:
    Return a list of all Expense instances with detailed information including the related 'expense_type' field.

    retrieve:
    Return a specific Expense instance by its ID with detailed information including the related 'expense_type' field.
    """
    queryset = Expense.objects.select_related('expense_type').all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific Expense instance and include full details of the related 'expense_type' field.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized data including the 'expense_type' field.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        # Serialize the 'expense_type' field
        if instance.expense_type:
            data['expense_type'] = self.get_expense_type_details(instance.expense_type)
        else:
            data['expense_type'] = None
        return Response(data)

    def list(self, request, *args, **kwargs):
        """
        List all Expense instances and include full details of the related 'expense_type' field for each item.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A list of serialized data including the 'expense_type' field for each item.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        # Add full details of 'expense_type' field for each item
        for item, instance in zip(data, queryset):
            if instance.expense_type:
                item['expense_type'] = self.get_expense_type_details(instance.expense_type)
            else:
                item['expense_type'] = None
        return Response(data)

    def get_expense_type_details(self, expense_type):
        """
        Retrieve detailed information of an ExpenseType.

        Args:
            expense_type: The ExpenseType instance to be detailed.

        Returns:
            dict: The serialized data of the ExpenseType.
        """
        serializer = ExpenseTypeSerializer(expense_type)
        return serializer.data


class ExpenseTypeViewSet(BaseViewSet):
    """
    A viewset for viewing and editing ExpenseType instances.

    list:
    Return a list of all ExpenseType instances with detailed information including the related 'updated_by' field.

    retrieve:
    Return a specific ExpenseType instance by its ID with detailed information including the related 'updated_by' field.
    """
    queryset = ExpenseType.objects.select_related('updated_by').all()
    serializer_class = ExpenseTypeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific ExpenseType instance and include full details of the related 'updated_by' field.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized data including the 'updated_by' field.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        # Serialize the 'updated_by' field if it exists
        if instance.updated_by:
            data['updated_by'] = self.get_base_entity_details(instance.updated_by)
        else:
            data['updated_by'] = None
        return Response(data)

    def list(self, request, *args, **kwargs):
        """
        List all ExpenseType instances and include full details of the related 'updated_by' field for each item.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A list of serialized data including the 'updated_by' field for each item.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        # Add full details of 'updated_by' field for each item
        for item, instance in zip(data, queryset):
            if instance.updated_by:
                item['updated_by'] = self.get_base_entity_details(instance.updated_by)
            else:
                item['updated_by'] = None
        return Response(data)

    def get_base_entity_details(self, base_entity):
        """
        Retrieve detailed information of a BaseEntity, including its related fields.

        Args:
            base_entity: The BaseEntity instance to be detailed.

        Returns:
            dict: The serialized data of the BaseEntity including related fields.
        """
        if base_entity:
            serializer = BaseEntitySerializer(base_entity)
            data = serializer.data
            # Assume that BaseEntity has 'branch' and 'entity_type' related fields
            data['branch'] = BranchSerializer(base_entity.branch).data if base_entity.branch else None
            data['entity_type'] = EntityTypeSerializer(base_entity.entity_type).data if base_entity.entity_type else None
            return data
        return None


class IncomeViewSet(BaseViewSet):
    """
    A viewset for viewing and editing Income instances.

    list:
    Return a list of all Income instances with detailed information about the related 'income_type'.

    retrieve:
    Return a specific Income instance by its ID with detailed information about the related 'income_type'.
    """
    queryset = Income.objects.select_related('income_type').all()
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific Income instance and include full details of the related 'income_type'.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized data of the Income instance including 'income_type'.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        if instance.income_type:
            data['income_type'] = IncomeTypeSerializer(instance.income_type).data
        else:
            data['income_type'] = None

        return Response(data)

    def list(self, request, *args, **kwargs):
        """
        List all Income instances and include full details of the related 'income_type' for each item.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A list of serialized data including 'income_type' for each item.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        # Add full details of 'income_type' field for each item
        for item, instance in zip(data, queryset):
            if instance.income_type:
                item['income_type'] = IncomeTypeSerializer(instance.income_type).data
            else:
                item['income_type'] = None
        return Response(data)


class IncomeTypeViewSet(BaseViewSet):
    """
    A viewset for viewing and editing IncomeType instances.

    list:
    Return a list of all IncomeType instances with detailed information about the related 'updated_by' field.

    retrieve:
    Return a specific IncomeType instance by its ID with detailed information about the related 'updated_by' field.
    """
    queryset = IncomeType.objects.select_related('updated_by').all()
    serializer_class = IncomeTypeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific IncomeType instance and include full details of the related 'updated_by' field.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized data of the IncomeType instance including 'updated_by'.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        if instance.updated_by:
            data['updated_by'] = BaseEntitySerializer(instance.updated_by).data
        else:
            data['updated_by'] = None

        return Response(data)

    def list(self, request, *args, **kwargs):
        """
        List all IncomeType instances and include full details of the related 'updated_by' field for each item.

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
        # Add full details of 'updated_by' field for each item
        for item, instance in zip(data, queryset):
            if instance.updated_by:
                item['updated_by'] = BaseEntitySerializer(instance.updated_by).data
            else:
                item['updated_by'] = None
        return Response(data)

class InterestRateTypeViewSet(BaseViewSet):
    queryset = InterestRateType.objects.all()
    serializer_class = InterestRateTypeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class InvestmentViewSet(BaseViewSet):
    """
    A viewset for viewing and editing Investment instances.

    list:
    Return a list of all Investment instances with detailed information about the related 'from_account', 'to_account', and 'investment_type' fields.

    retrieve:
    Return a specific Investment instance by its ID with detailed information about the related 'from_account', 'to_account', and 'investment_type' fields.
    """
    queryset = Investment.objects.select_related(
        'from_account', 'to_account', 'investment_type', 'status', 'transaction'
    ).all()
    serializer_class = InvestmentSerializer
    permission_classes = [IsAuthenticated, IsStaffOrRelated]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific Investment instance and include full details of the related 'from_account', 'to_account', 'investment_type', 'status', and 'transaction' fields.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized data including the related fields.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        # Serialize related fields with full details
        data['from_account'] = self.get_account_details(instance.from_account)
        data['to_account'] = self.get_account_details(instance.to_account)
        data['investment_type'] = InvestmentTypeSerializer(instance.investment_type).data
        data['status'] = StatusSerializer(instance.status).data
        data['transaction'] = TransactionSerializer(instance.transaction).data if instance.transaction else None
        return Response(data)

    def list(self, request, *args, **kwargs):
        """
        List all Investment instances and include full details of the related 'from_account', 'to_account', 'investment_type', 'status', and 'transaction' fields for each item.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A list of serialized data including the related fields for each item.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        # Add full details of related fields for each item
        for item, instance in zip(data, queryset):
            item['from_account'] = self.get_account_details(instance.from_account)
            item['to_account'] = self.get_account_details(instance.to_account)
            item['investment_type'] = InvestmentTypeSerializer(instance.investment_type).data
            item['status'] = StatusSerializer(instance.status).data
            item['transaction'] = TransactionSerializer(instance.transaction).data if instance.transaction else None
        return Response(data)

    def get_account_details(self, account):
        """
        Retrieve detailed information of an Account, including its related fields.

        Args:
            account: The Account instance to be detailed.

        Returns:
            dict: The serialized data of the Account including related fields.
        """
        if account:
            serializer = AccountSerializer(account)
            data = serializer.data
            # Assume that Account has related fields 'owner', 'account_type', 'branch', and 'status'
            data['owner'] = BaseEntitySerializer(account.owner).data if account.owner else None
            data['account_type'] = AccountTypeSerializer(account.account_type).data if account.account_type else None
            data['branch'] = BranchSerializer(account.branch).data if account.branch else None
            data['status'] = StatusSerializer(account.status).data if account.status else None
            return data
        return None


class InvestmentCreditingViewSet(BaseViewSet):
    """
    A viewset for viewing and editing InvestmentCrediting instances.

    list:
    Return a list of all InvestmentCrediting instances with detailed information about the related 'transaction', 'status', and 'investment' fields.

    retrieve:
    Return a specific InvestmentCrediting instance by its ID with detailed information about the related 'transaction', 'status', and 'investment' fields.
    """
    queryset = InvestmentCrediting.objects.select_related(
        'transaction', 'status', 'investment'
    ).all()
    serializer_class = InvestmentCreditingSerializer
    permission_classes = [IsAuthenticated, IsStaffOrRelated]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific InvestmentCrediting instance and include full details of the related 'transaction', 'status', and 'investment' fields.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized data including the related fields.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        # Serialize related fields with full details
        data['transaction'] = TransactionSerializer(instance.transaction).data
        data['status'] = StatusSerializer(instance.status).data
        data['investment'] = self.get_investment_details(instance.investment)
        return Response(data)

    def list(self, request, *args, **kwargs):
        """
        List all InvestmentCrediting instances and include full details of the related 'transaction', 'status', and 'investment' fields for each item.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A list of serialized data including the related fields for each item.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        # Add full details of related fields for each item
        for item, instance in zip(data, queryset):
            item['transaction'] = TransactionSerializer(instance.transaction).data
            item['status'] = StatusSerializer(instance.status).data
            item['investment'] = self.get_investment_details(instance.investment)
        return Response(data)

    def get_investment_details(self, investment):
        """
        Retrieve detailed information of an Investment, including its related fields.

        Args:
            investment: The Investment instance to be detailed.

        Returns:
            dict: The serialized data of the Investment including related fields.
        """
        if investment:
            serializer = InvestmentSerializer(investment)
            data = serializer.data
            # Assume that Investment has related fields 'from_account', 'to_account', 'investment_type', and 'status'
            data['from_account'] = AccountSerializer(investment.from_account).data if investment.from_account else None
            data['to_account'] = AccountSerializer(investment.to_account).data if investment.to_account else None
            data['investment_type'] = InvestmentTypeSerializer(investment.investment_type).data if investment.investment_type else None
            data['status'] = StatusSerializer(investment.status).data if investment.status else None
            return data
        return None


class InvestmentTypeViewSet(BaseViewSet):
    """
    A viewset for viewing and editing InvestmentType instances.

    list:
    Return a list of all InvestmentType instances with detailed information including the related 'updated_by' field.

    retrieve:
    Return a specific InvestmentType instance by its ID with detailed information including the related 'updated_by' field.
    """
    queryset = InvestmentType.objects.select_related('updated_by').all()
    serializer_class = InvestmentTypeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific InvestmentType instance and include full details of the related 'updated_by' field.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized data including the 'updated_by' field.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        # Serialize the 'updated_by' field if it exists
        if instance.updated_by:
            data['updated_by'] = self.get_base_entity_details(instance.updated_by)
        else:
            data['updated_by'] = None
        return Response(data)

    def list(self, request, *args, **kwargs):
        """
        List all InvestmentType instances and include full details of the related 'updated_by' field for each item.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A list of serialized data including the 'updated_by' field for each item.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        # Add full details of 'updated_by' field for each item
        for item, instance in zip(data, queryset):
            if instance.updated_by:
                item['updated_by'] = self.get_base_entity_details(instance.updated_by)
            else:
                item['updated_by'] = None
        return Response(data)

    def get_base_entity_details(self, base_entity):
        """
        Retrieve detailed information of a BaseEntity, including its related fields.

        Args:
            base_entity: The BaseEntity instance to be detailed.

        Returns:
            dict: The serialized data of the BaseEntity including related fields.
        """
        if base_entity:
            serializer = BaseEntitySerializer(base_entity)
            data = serializer.data
            # Assume that BaseEntity has 'branch' and 'entity_type' related fields
            data['branch'] = BranchSerializer(base_entity.branch).data if base_entity.branch else None
            data['entity_type'] = EntityTypeSerializer(base_entity.entity_type).data if base_entity.entity_type else None
            return data
        return None


class LiabilityViewSet(BaseViewSet):
    """
    A viewset for viewing and editing Liability instances.

    list:
    Return a list of all Liability instances with detailed information including related fields.

    retrieve:
    Return a specific Liability instance by its ID with detailed information including related fields.
    """
    queryset = Liability.objects.select_related('branch', 'liability_type', 'status').all()
    serializer_class = LiabilitySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific Liability instance and include full details of the related fields.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized data including related fields.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        # Serialize related fields
        data['branch'] = BranchSerializer(instance.branch).data
        data['liability_type'] = LiabilityTypeSerializer(instance.liability_type).data
        data['status'] = StatusSerializer(instance.status).data
        return Response(data)

    def list(self, request, *args, **kwargs):
        """
        List all Liability instances and include full details of the related fields for each item.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A list of serialized data including related fields for each item.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        # Add full details of related fields for each item
        for item, instance in zip(data, queryset):
            item['branch'] = BranchSerializer(instance.branch).data
            item['liability_type'] = LiabilityTypeSerializer(instance.liability_type).data
            item['status'] = StatusSerializer(instance.status).data
        return Response(data)


class LiabilityTypeViewSet(BaseViewSet):
    """
    A viewset for viewing and editing LiabilityType instances.

    list:
    Return a list of all LiabilityType instances with detailed information including the related 'updated_by' field.

    retrieve:
    Return a specific LiabilityType instance by its ID with detailed information including the related 'updated_by' field.
    """
    queryset = LiabilityType.objects.select_related('updated_by').all()
    serializer_class = LiabilityTypeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific LiabilityType instance and include full details of the related 'updated_by' field.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized data including the 'updated_by' field.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        # Serialize the 'updated_by' field if it exists
        if instance.updated_by:
            data['updated_by'] = self.get_base_entity_details(instance.updated_by)
        else:
            data['updated_by'] = None
        return Response(data)

    def list(self, request, *args, **kwargs):
        """
        List all LiabilityType instances and include full details of the related 'updated_by' field for each item.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A list of serialized data including the 'updated_by' field for each item.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        # Add full details of 'updated_by' field for each item
        for item, instance in zip(data, queryset):
            if instance.updated_by:
                item['updated_by'] = self.get_base_entity_details(instance.updated_by)
            else:
                item['updated_by'] = None
        return Response(data)

    def get_base_entity_details(self, base_entity):
        """
        Retrieve detailed information of a BaseEntity, including its related fields.

        Args:
            base_entity: The BaseEntity instance to be detailed.

        Returns:
            dict: The serialized data of the BaseEntity including related fields.
        """
        if base_entity:
            serializer = BaseEntitySerializer(base_entity)
            data = serializer.data
            data['branch'] = BranchSerializer(base_entity.branch).data if base_entity.branch else None
            data['entity_type'] = EntityTypeSerializer(base_entity.entity_type).data if base_entity.entity_type else None
            return data
        return None


class LoanViewSet(BaseViewSet):
    """
    A viewset for viewing and editing Loan instances.

    list:
    Return a list of all Loan instances with detailed information including related fields.

    retrieve:
    Return a specific Loan instance by its ID with detailed information including related fields.
    """
    queryset = Loan.objects.select_related('from_account', 'to_account', 'loan_type', 'status', 'loan_term', 'transaction').all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated, IsStaffOrRelated]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific Loan instance and include full details of the related fields.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized data including related fields.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        # Serialize related fields
        data['from_account'] = AccountSerializer(instance.from_account).data
        data['to_account'] = AccountSerializer(instance.to_account).data
        data['loan_type'] = LoanTypeSerializer(instance.loan_type).data
        data['status'] = StatusSerializer(instance.status).data
        data['loan_term'] = LoanTermsSerializer(instance.loan_term).data
        data['transaction'] = TransactionSerializer(instance.transaction).data if instance.transaction else None
        return Response(data)

    def list(self, request, *args, **kwargs):
        """
        List all Loan instances and include full details of the related fields for each item.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A list of serialized data including related fields for each item.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        # Add full details of related fields for each item
        for item, instance in zip(data, queryset):
            item['from_account'] = AccountSerializer(instance.from_account).data
            item['to_account'] = AccountSerializer(instance.to_account).data
            item['loan_type'] = LoanTypeSerializer(instance.loan_type).data
            item['status'] = StatusSerializer(instance.status).data
            item['loan_term'] = LoanTermsSerializer(instance.loan_term).data
            item['transaction'] = TransactionSerializer(instance.transaction).data if instance.transaction else None
        return Response(data)


class LoanPaymentViewSet(BaseViewSet):
    """
    A viewset for viewing and editing LoanPayment instances.

    list:
    Return a list of all LoanPayment instances with detailed information including related fields.

    retrieve:
    Return a specific LoanPayment instance by its ID with detailed information including related fields.
    """
    queryset = LoanPayment.objects.select_related('paid_by', 'transaction', 'status', 'loan').all()
    serializer_class = LoanPaymentSerializer
    permission_classes = [IsAuthenticated, IsStaffOrRelated]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific LoanPayment instance and include full details of the related fields.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized data including related fields.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['paid_by'] = BaseEntitySerializer(instance.paid_by).data
        data['transaction'] = TransactionSerializer(instance.transaction).data
        data['status'] = StatusSerializer(instance.status).data
        data['loan'] = LoanSerializer(instance.loan).data
        return Response(data)

    def list(self, request, *args, **kwargs):
        """
        List all LoanPayment instances and include full details of the related fields for each item.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A list of serialized data including related fields for each item.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        for item, instance in zip(data, queryset):
            item['paid_by'] = BaseEntitySerializer(instance.paid_by).data
            item['transaction'] = TransactionSerializer(instance.transaction).data
            item['status'] = StatusSerializer(instance.status).data
            item['loan'] = LoanSerializer(instance.loan).data
        return Response(data)


class LoanTermsViewSet(BaseViewSet):
    """
    A viewset for viewing and editing LoanTerms instances.

    list:
    Return a list of all LoanTerms instances with detailed information including related fields.

    retrieve:
    Return a specific LoanTerms instance by its ID with detailed information including related fields.
    """
    queryset = LoanTerms.objects.select_related('entity', 'loan_type', 'interest_rate_type').all()
    serializer_class = LoanTermsSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific LoanTerms instance and include full details of the related fields.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized data including related fields.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['entity'] = BaseEntitySerializer(instance.entity).data
        data['loan_type'] = LoanTypeSerializer(instance.loan_type).data
        data['interest_rate_type'] = InterestRateTypeSerializer(instance.interest_rate_type).data
        return Response(data)

    def list(self, request, *args, **kwargs):
        """
        List all LoanTerms instances and include full details of the related fields for each item.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A list of serialized data including related fields for each item.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        for item, instance in zip(data, queryset):
            item['entity'] = BaseEntitySerializer(instance.entity).data
            item['loan_type'] = LoanTypeSerializer(instance.loan_type).data
            item['interest_rate_type'] = InterestRateTypeSerializer(instance.interest_rate_type).data
        return Response(data)


class LoanTypeViewSet(BaseViewSet):
    queryset = LoanType.objects.all()
    serializer_class = LoanTypeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class StatusViewSet(BaseViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class TransactionViewSet(BaseViewSet):
    """
    A viewset for viewing and editing Transaction instances.

    list:
    Return a list of all Transaction instances with detailed information including related fields.

    retrieve:
    Return a specific Transaction instance by its ID with detailed information including related fields.
    """
    queryset = Transaction.objects.select_related('sender_account', 'recipient_account', 'transaction_type', 'initiated_by', 'status', 'branch', 'transaction_direction').all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, IsStaffOrRelated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset
        else:
            return self.queryset.filter(
                sender_account__owner=user
            ) | self.queryset.filter(
                recipient_account__owner=user
            )

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific Transaction instance and include full details of the related fields.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized data including related fields.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['sender_account'] = AccountSerializer(instance.sender_account).data
        data['recipient_account'] = AccountSerializer(instance.receiver_account).data
        data['transaction_type'] = TransactionTypeSerializer(instance.transaction_type).data
        data['initiated_by'] = BaseEntitySerializer(instance.initiated_by).data
        data['status'] = StatusSerializer(instance.status).data
        data['branch'] = BranchSerializer(instance.branch).data
        data['transaction_direction'] = TransactionDirectionSerializer(instance.transaction_direction).data
        return Response(data)

    def list(self, request, *args, **kwargs):
        """
        List all Transaction instances and include full details of the related fields for each item.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A list of serialized data including related fields for each item.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        for item, instance in zip(data, queryset):
            item['sender_account'] = AccountSerializer(instance.sender_account).data
            item['recipient_account'] = AccountSerializer(instance.receiver_account).data
            item['transaction_type'] = TransactionTypeSerializer(instance.transaction_type).data
            item['initiated_by'] = BaseEntitySerializer(instance.initiated_by).data
            item['status'] = StatusSerializer(instance.status).data
            item['branch'] = BranchSerializer(instance.branch).data
            item['transaction_direction'] = TransactionDirectionSerializer(instance.transaction_direction).data
        return Response(data)

    def create(self, request, *args, **kwargs):
        """
        Create a new Transaction instance and update the sender and recipient account balances.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized data of the new Transaction instance.
        """
        data = request.data
        sender_account = Account.objects.get(account_number=data['sender_account'])
        recipient_account = Account.objects.get(account_number=data['recipient_account'])
        amount = data['amount']
        transaction_direction = TransactionDirection.objects.get(id=data['transaction_direction'])
        user = request.user
        transaction_type = TransactionType.objects.get(id=data['transaction_type'])
        initiated_by = BaseEntity.objects.get(id=data['initiated_by'])
        branch = Branch.objects.get(id=data['branch'])
        transaction_status = Status.objects.get(status_name='Completed')

        # Check if the transaction direction is internal or external
        if transaction_direction.direction == 'Internal':
            # Check if both sender and receiver accounts are set
            if not sender_account or not recipient_account:
                return Response(
                    {"error": "Both sender and receiver accounts must be set for internal transactions."},
                    status=status.HTTP_400_BAD_REQUEST)
            # Check if the sender account has enough balance to make the transaction
            if sender_account.current_balance - amount < 80:
                return Response(
                    {"error": "Insufficient funds in sender account."},
                    status=status.HTTP_400_BAD_REQUEST)
            # Check if the sender and receiver accounts are the same
            if sender_account == recipient_account:
                return Response (
                    {"error": "Sender and receiver accounts cannot be the same."},
                    status=status.HTTP_400_BAD_REQUEST)

            if user.entity_type.name == 'Individual':
                if sender_account.owner != user:
                    return Response(
                        {"error": "You are not authorized to make transactions from this account."},
                        status=status.HTTP_403_FORBIDDEN)
                initiated_by = BaseEntity.objects.get(id=user.id)
        elif transaction_direction.direction == 'External':
            # Check if only one of sender or receiver account is set
            if sender_account and recipient_account:
                return Response(
                    {"error": "Only one of sender or receiver account should be set for external transactions."},
                    status=status.HTTP_400_BAD_REQUEST)
            # Check if the sender or receiver account has enough balance to make the transaction
            if sender_account:
                if sender_account.current_balance - amount < 80:
                    return Response(
                        {"error": "Insufficient funds in sender account."},
                        status=status.HTTP_400_BAD_REQUEST)
                if user.entity_type.name == 'Individual':
                    if sender_account.owner != transaction_type.type_name == 'Withdrawal':
                        return Response(
                            {"error": "You are not authorized to make transactions from this account."},
                            status=status.HTTP_403_FORBIDDEN)
                    initiated_by = BaseEntity.objects.get(id=user.id)
            if recipient_account:
                if recipient_account.current_balance - amount < 80:
                    return Response(
                        {"error": "Insufficient funds in receiver account."},
                        status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"error": "Invalid transaction direction."},
                status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # Update the sender and receiver account balances
                sender_account.current_balance -= amount
                recipient_account.current_balance += amount
                sender_account.save()
                recipient_account.save()
                # Create a new Transaction instance
                transaction = Transaction.objects.create(
                    sender_account=sender_account,
                    receiver_account=recipient_account,
                    transaction_amount=amount,
                    transaction_type=transaction_type,
                    initiated_by=initiated_by,
                    status=transaction_status,
                    branch=branch,
                    transaction_direction_id=data['transaction_direction']
                )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(transaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TransactionDirectionViewSet(BaseViewSet):
    queryset = TransactionDirection.objects.all()
    serializer_class = TransactionDirectionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class TransactionTypeViewSet(BaseViewSet):
    queryset = TransactionType.objects.all()
    serializer_class = TransactionTypeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
