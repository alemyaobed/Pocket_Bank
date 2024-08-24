from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from accounts.serializers import BaseEntitySerializer, BranchSerializer, EntityTypeSerializer
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

class AccountViewSet(ModelViewSet):
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
    # permission_classes = [IsAuthenticated]

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

class AccountTypeViewSet(ModelViewSet):
    """
    A viewset for viewing and editing AccountType instances.

    list:
    Return a list of all AccountType instances with detailed information including the related 'updated_by' field.

    retrieve:
    Return a specific AccountType instance by its ID with detailed information including the related 'updated_by' field.
    """
    queryset = AccountType.objects.select_related('updated_by').all()
    serializer_class = AccountTypeSerializer
    # permission_classes = [IsAuthenticated]

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

class AnnualBalanceViewSet(ModelViewSet):
    """
    A viewset for viewing and editing `AnnualBalance` instances.

    list:
    Return a list of all `AnnualBalance` instances with detailed information, including the related `branch` field.

    retrieve:
    Return a specific `AnnualBalance` instance by its ID with detailed information, including the related `branch` field.
    """
    queryset = AnnualBalance.objects.select_related('branch').all()
    serializer_class = AnnualBalanceSerializer
    # permission_classes = [IsAuthenticated]

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

class AssetViewSet(ModelViewSet):
    """
    A viewset for viewing and editing `Asset` instances.

    list:
    Return a list of all `Asset` instances with detailed information, including related fields like `branch`, `asset_type`, and `status`.

    retrieve:
    Return a specific `Asset` instance by its ID with detailed information, including related fields like `branch`, `asset_type`, and `status`.
    """
    queryset = Asset.objects.select_related('branch', 'asset_type', 'status').all()
    serializer_class = AssetSerializer
    # permission_classes = [IsAuthenticated]

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


class AssetTypeViewSet(ModelViewSet):
    """
    A viewset for viewing and editing AssetType instances.

    list:
    Return a list of all AssetType instances with detailed information including the related 'updated_by' field.

    retrieve:
    Return a specific AssetType instance by its ID with detailed information including the related 'updated_by' field.
    """
    queryset = AssetType.objects.select_related('updated_by').all()
    serializer_class = AssetTypeSerializer
    # permission_classes = [IsAuthenticated]

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


class AuditViewSet(ModelViewSet):
    queryset = Audit.objects.all()
    serializer_class = AuditSerializer

class CapitalViewSet(ModelViewSet):
    """
    A viewset for viewing and editing Capital instances.

    list:
    Return a list of all Capital instances with detailed information including related fields.

    retrieve:
    Return a specific Capital instance by its ID with detailed information including related fields.
    """
    queryset = Capital.objects.select_related('branch', 'capital_type', 'status').all()
    serializer_class = CapitalSerializer
    # permission_classes = [IsAuthenticated]

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


class CapitalTypeViewSet(ModelViewSet):
    """
    A viewset for viewing and editing CapitalType instances.

    list:
    Return a list of all CapitalType instances with detailed information including the related 'updated_by' field.

    retrieve:
    Return a specific CapitalType instance by its ID with detailed information including the related 'updated_by' field.
    """
    queryset = CapitalType.objects.select_related('updated_by').all()
    serializer_class = CapitalTypeSerializer
    # permission_classes = [IsAuthenticated]

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


class ExpenseViewSet(ModelViewSet):
    """
    A viewset for viewing and editing Expense instances.

    list:
    Return a list of all Expense instances with detailed information including the related 'expense_type' field.

    retrieve:
    Return a specific Expense instance by its ID with detailed information including the related 'expense_type' field.
    """
    queryset = Expense.objects.select_related('expense_type').all()
    serializer_class = ExpenseSerializer
    # permission_classes = [IsAuthenticated]

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


class ExpenseTypeViewSet(ModelViewSet):
    """
    A viewset for viewing and editing ExpenseType instances.

    list:
    Return a list of all ExpenseType instances with detailed information including the related 'updated_by' field.

    retrieve:
    Return a specific ExpenseType instance by its ID with detailed information including the related 'updated_by' field.
    """
    queryset = ExpenseType.objects.select_related('updated_by').all()
    serializer_class = ExpenseTypeSerializer
    # permission_classes = [IsAuthenticated]

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


class IncomeViewSet(ModelViewSet):
    """
    A viewset for viewing and editing Income instances.

    list:
    Return a list of all Income instances with detailed information about the related 'income_type'.

    retrieve:
    Return a specific Income instance by its ID with detailed information about the related 'income_type'.
    """
    queryset = Income.objects.select_related('income_type').all()
    serializer_class = IncomeSerializer
    # permission_classes = [IsAuthenticated]

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


class IncomeTypeViewSet(ModelViewSet):
    """
    A viewset for viewing and editing IncomeType instances.

    list:
    Return a list of all IncomeType instances with detailed information about the related 'updated_by' field.

    retrieve:
    Return a specific IncomeType instance by its ID with detailed information about the related 'updated_by' field.
    """
    queryset = IncomeType.objects.select_related('updated_by').all()
    serializer_class = IncomeTypeSerializer
    # permission_classes = [IsAuthenticated]

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

class InterestRateTypeViewSet(ModelViewSet):
    queryset = InterestRateType.objects.all()
    serializer_class = InterestRateTypeSerializer

class InvestmentViewSet(ModelViewSet):
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer

class InvestmentCreditingViewSet(ModelViewSet):
    queryset = InvestmentCrediting.objects.all()
    serializer_class = InvestmentCreditingSerializer

class InvestmentTypeViewSet(ModelViewSet):
    queryset = InvestmentType.objects.all()
    serializer_class = InvestmentTypeSerializer

class LiabilityViewSet(ModelViewSet):
    queryset = Liability.objects.all()
    serializer_class = LiabilitySerializer

class LiabilityTypeViewSet(ModelViewSet):
    queryset = LiabilityType.objects.all()
    serializer_class = LiabilityTypeSerializer

class LoanViewSet(ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

class LoanPaymentViewSet(ModelViewSet):
    queryset = LoanPayment.objects.all()
    serializer_class = LoanPaymentSerializer

class LoanTermsViewSet(ModelViewSet):
    queryset = LoanTerms.objects.all()
    serializer_class = LoanTermsSerializer

class LoanTypeViewSet(ModelViewSet):
    queryset = LoanType.objects.all()
    serializer_class = LoanTypeSerializer

class StatusViewSet(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class TransactionDirectionViewSet(ModelViewSet):
    queryset = TransactionDirection.objects.all()
    serializer_class = TransactionDirectionSerializer

class TransactionTypeViewSet(ModelViewSet):
    queryset = TransactionType.objects.all()
    serializer_class = TransactionTypeSerializer
