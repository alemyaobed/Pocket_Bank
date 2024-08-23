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
    queryset = AnnualBalance.objects.all()
    serializer_class = AnnualBalanceSerializer

class AssetViewSet(ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

class AssetTypeViewSet(ModelViewSet):
    queryset = AssetType.objects.all()
    serializer_class = AssetTypeSerializer

class AuditViewSet(ModelViewSet):
    queryset = Audit.objects.all()
    serializer_class = AuditSerializer

class CapitalViewSet(ModelViewSet):
    queryset = Capital.objects.all()
    serializer_class = CapitalSerializer

class CapitalTypeViewSet(ModelViewSet):
    queryset = CapitalType.objects.all()
    serializer_class = CapitalTypeSerializer

class ExpenseViewSet(ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

class ExpenseTypeViewSet(ModelViewSet):
    queryset = ExpenseType.objects.all()
    serializer_class = ExpenseTypeSerializer

class IncomeViewSet(ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

class IncomeTypeViewSet(ModelViewSet):
    queryset = IncomeType.objects.all()
    serializer_class = IncomeTypeSerializer

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
