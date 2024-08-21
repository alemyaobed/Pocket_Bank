from rest_framework.serializers import ModelSerializer
from .models import (
    Account, AccountType, AnnualBalance, AssetType, Asset,
    Audit, Branch, Capital, CapitalType, Expense, ExpenseType,
    Income, IncomeType, InterestRateType, Investment, InvestmentCrediting,
    InvestmentType, Liability, LiabilityType, Loan, LoanPayment, LoanTerms,
    LoanType, Status, TransactionDirection, Transaction, TransactionType)

class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        read_only_fields = ['id', 'account_number', 'created_at', 'updated_at', 'closed_at']


class StatusSerializer(ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class TransactionTypeSerializer(ModelSerializer):
    class Meta:
        model = TransactionType
        fields = '__all__'


class BranchSerializer(ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'


class LoanSerializer(ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'closed_at', 'fully_paid', 'current_loan_amount']


class LoanTypeSerializer(ModelSerializer):
    class Meta:
        model = LoanType
        fields = '__all__'


class LoanTermsSerializer(ModelSerializer):
    class Meta:
        model = LoanTerms
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class InterestRateTypeSerializer(ModelSerializer):
    class Meta:
        model = InterestRateType
        fields = '__all__'


class InvestmentSerializer(ModelSerializer):
    class Meta:
        model = Investment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'closed_at']


class LoanPaymentSerializer(ModelSerializer):
    class Meta:
        model = LoanPayment
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class InvestmentCreditingSerializer(ModelSerializer):
    class Meta:
        model = InvestmentCrediting
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class AuditSerializer(ModelSerializer):
    class Meta:
        model = Audit
        fields = '__all__'
        read_only_fields = ['id', 'action_timestamp']


class AssetSerializer(ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class CapitalSerializer(ModelSerializer):
    class Meta:
        model = Capital
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class LiabilitySerializer(ModelSerializer):
    class Meta:
        model = Liability
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class AnnualBalanceSerializer(ModelSerializer):
    class Meta:
        model = AnnualBalance
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class TransactionDirectionSerializer(ModelSerializer):
    class Meta:
        model = TransactionDirection
        fields = '__all__'


class AccountTypeSerializer(ModelSerializer):
    class Meta:
        model = AccountType
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class InvestmentTypeSerializer(ModelSerializer):
    class Meta:
        model = InvestmentType
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class AssetTypeSerializer(ModelSerializer):
    class Meta:
        model = AssetType
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class CapitalTypeSerializer(ModelSerializer):
    class Meta:
        model = CapitalType
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class LiabilityTypeSerializer(ModelSerializer):
    class Meta:
        model = LiabilityType
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class IncomeSerializer(ModelSerializer):
    class Meta:
        model = Income
        fields = '__all__'
        read_only_fields = ['id']


class IncomeTypeSerializer(ModelSerializer):
    class Meta:
        model = IncomeType
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class ExpenseSerializer(ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class ExpenseTypeSerializer(ModelSerializer):
    class Meta:
        model = ExpenseType
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

