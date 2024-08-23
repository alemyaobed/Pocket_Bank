from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
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
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class AccountTypeViewSet(ModelViewSet):
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer

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
