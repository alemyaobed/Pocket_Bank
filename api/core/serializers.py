from rest_framework.serializers import ModelSerializer
from .models import (
    Account, AccountType, AnnualBalance, AssetType, Asset,
    Audit, Capital, CapitalType, Expense, ExpenseType,
    Income, IncomeType, InterestRateType, Investment, InvestmentCrediting,
    InvestmentType, Liability, LiabilityType, Loan, LoanPayment, LoanTerms,
    LoanType, Status, TransactionDirection, Transaction, TransactionType)
from accounts.serializers import BaseEntitySerializer, BranchSerializer



class StatusSerializer(ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class TransactionTypeSerializer(ModelSerializer):
    class Meta:
        model = TransactionType
        fields = '__all__'


class LoanTypeSerializer(ModelSerializer):
    class Meta:
        model = LoanType
        fields = '__all__'


class InterestRateTypeSerializer(ModelSerializer):
    class Meta:
        model = InterestRateType
        fields = '__all__'


class LoanTermsSerializer(ModelSerializer):
    entity = BaseEntitySerializer()
    loan_type = LoanTypeSerializer()
    interest_rate_type = InterestRateTypeSerializer()
    class Meta:
        model = LoanTerms
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class AuditSerializer(ModelSerializer):
    entity = BaseEntitySerializer()
    class Meta:
        model = Audit
        fields = '__all__'
        read_only_fields = ['id', 'action_timestamp']


class AnnualBalanceSerializer(ModelSerializer):
    branch = BranchSerializer()

    class Meta:
        model = AnnualBalance
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class TransactionDirectionSerializer(ModelSerializer):
    class Meta:
        model = TransactionDirection
        fields = '__all__'


class AccountTypeSerializer(ModelSerializer):
    updated_by = BaseEntitySerializer()

    class Meta:
        model = AccountType
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class InvestmentTypeSerializer(ModelSerializer):
    updated_by = BaseEntitySerializer()

    class Meta:
        model = InvestmentType
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class AssetTypeSerializer(ModelSerializer):
    updated_by = BaseEntitySerializer()

    class Meta:
        model = AssetType
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class CapitalTypeSerializer(ModelSerializer):
    updated_by = BaseEntitySerializer()

    class Meta:
        model = CapitalType
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class LiabilityTypeSerializer(ModelSerializer):
    updated_by = BaseEntitySerializer()

    class Meta:
        model = LiabilityType
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class IncomeTypeSerializer(ModelSerializer):
    updated_by = BaseEntitySerializer()

    class Meta:
        model = IncomeType
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class AccountSerializer(ModelSerializer):
    owner = BaseEntitySerializer()
    account_type = AccountTypeSerializer()
    branch = BranchSerializer()
    status = StatusSerializer()

    class Meta:
        model = Account
        fields = '__all__'
        read_only_fields = ['id', 'account_number', 'created_at', 'updated_at', 'closed_at']


class TransactionSerializer(ModelSerializer):
    sender_account = AccountSerializer()
    receiver_account = AccountSerializer()
    transaction_type = TransactionTypeSerializer()
    initiated_by = BaseEntitySerializer()
    status = StatusSerializer()
    branch = BranchSerializer()
    transaction_direction = TransactionDirectionSerializer()

    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class LoanSerializer(ModelSerializer):
    from_account = AccountSerializer()
    to_account = AccountSerializer()
    loan_type = LoanTypeSerializer()
    status = StatusSerializer()
    loan_term = LoanTermsSerializer()
    transaction = TransactionSerializer()

    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'closed_at', 'fully_paid', 'current_loan_amount']


class LoanPaymentSerializer(ModelSerializer):
    paid_by = BaseEntitySerializer()
    transaction = TransactionSerializer()
    status = StatusSerializer()
    loan = LoanSerializer()

    class Meta:
        model = LoanPayment
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class InvestmentSerializer(ModelSerializer):
    from_account =  AccountSerializer()
    to_account = AccountSerializer()
    investment_type = InvestmentTypeSerializer()
    status = StatusSerializer()
    transaction = TransactionSerializer()

    class Meta:
        model = Investment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'closed_at']


class InvestmentCreditingSerializer(ModelSerializer):
    transaction = TransactionSerializer()
    status = StatusSerializer()
    investment = InvestmentSerializer()
    class Meta:
        model = InvestmentCrediting
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class AssetSerializer(ModelSerializer):
    branch = BranchSerializer()
    asset_type = AssetTypeSerializer()
    status = StatusSerializer()
    class Meta:
        model = Asset
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class CapitalSerializer(ModelSerializer):
    branch = BranchSerializer()
    capital_type = CapitalTypeSerializer()
    status = StatusSerializer()
    class Meta:
        model = Capital
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class LiabilitySerializer(ModelSerializer):
    branch = BranchSerializer()
    liability_type = LiabilityTypeSerializer()
    class Meta:
        model = Liability
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class IncomeSerializer(ModelSerializer):
    income_type = IncomeTypeSerializer()

    class Meta:
        model = Income
        fields = '__all__'
        read_only_fields = ['id']


class ExpenseTypeSerializer(ModelSerializer):
    updated_by = BaseEntitySerializer()

    class Meta:
        model = ExpenseType
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class ExpenseSerializer(ModelSerializer):
    expense_type = ExpenseTypeSerializer()

    class Meta:
        model = Expense
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
