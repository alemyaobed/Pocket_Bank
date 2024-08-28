from rest_framework.serializers import ModelSerializer
from .models import (
    Account, AccountType, AnnualBalance, AssetType, Asset,
    Audit, Capital, CapitalType, Expense, ExpenseType,
    Income, IncomeType, InterestRateType, Investment, InvestmentCrediting,
    InvestmentType, Liability, LiabilityType, Loan, LoanPayment, LoanTerms,
    LoanType, Status, TransactionDirection, Transaction, TransactionType)


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
    class Meta:
        model = LoanTerms
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class AuditSerializer(ModelSerializer):
    class Meta:
        model = Audit
        fields = '__all__'
        read_only_fields = ['id', 'action_timestamp']


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
        read_only_fields = ['created_at', 'updated_at', 'updated_balance']


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

class IncomeTypeSerializer(ModelSerializer):
    class Meta:
        model = IncomeType
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        read_only_fields = ['id', 'account_number', 'created_at', 'updated_at', 'closed_at']


class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'recipient_account_balance', 'sender_account_balance', 'status']


class LoanSerializer(ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'closed_at', 'fully_paid', 'current_loan_amount']

    def create(self, validated_data):
        loan = Loan.objects.create(**validated_data)
        loan.interest_rate = loan.loan_type.interest_rate
        loan.current_loan_amount = loan.loan_amount
        loan.save()
        return loan



class LoanPaymentSerializer(ModelSerializer):
    class Meta:
        model = LoanPayment
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class InvestmentSerializer(ModelSerializer):
    class Meta:
        model = Investment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'closed_at']


class InvestmentCreditingSerializer(ModelSerializer):
    class Meta:
        model = InvestmentCrediting
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'transaction']

    def create(self, validated_data):
        # Extract investment and status IDs from validated_data
        investment_id = validated_data.pop('investment')
        status_id = validated_data.pop('status')

        # Retrieve the investment and status objects
        investment = Investment.objects.get(id=investment_id)
        status = Status.objects.get(id=status_id)

        if not investment or not status:
            raise ValueError("Invalid investment ID or status ID")

        # Retrieve the from_account and to_account objects from the investment
        from_account = investment.from_account
        to_account = investment.to_account

        # Create the InvestmentCrediting object
        investment_crediting = InvestmentCrediting.objects.create(
            investment=investment,
            status=status,
            **validated_data
        )

        # Calculate the total amount being credited (principal + interest)
        total_credited_amount = investment_crediting.payment_amount + investment_crediting.interest_earned

        # Update the from_account and to_account balances
        from_account.current_balance -= investment_crediting.payment_amount
        to_account.current_balance += total_credited_amount

        from_account.save()
        to_account.save()

        # Create a transaction to reflect the crediting operation
        transaction = Transaction.objects.create(
            transaction_type='credit',  # Customize this based on your system's transaction types
            amount=total_credited_amount,
            sender_account=from_account,
            receiver_account=to_account,
            status=status,
            external_reference=None,  # Assuming this is an internal transaction
            investment=investment  # Link the transaction with the investment
        )

        # Attach the transaction to the investment crediting record
        investment_crediting.transaction = transaction
        investment_crediting.save()

        # Create an audit log for this operation
        Audit.objects.create(
            action_initiator=self.context['request'].user,  # User who performed the action
            action='credit_investment',
            table_name=InvestmentCrediting._meta.db_table,
            old_value=f"From account balance: {from_account.current_balance + investment_crediting.payment_amount}, "
                      f"To account balance: {to_account.current_balance - total_credited_amount}",
            new_value=f"From account balance: {from_account.current_balance}, "
                      f"To account balance: {to_account.current_balance}",
            action_timestamp=investment_crediting.created_at
        )

        return investment_crediting


class AssetSerializer(ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_balance']

    def create(self, validated_data):
        # Create the asset object with the provided data
        asset = Asset.objects.create(**validated_data)

        # Get the last asset in the same branch to calculate the updated balance
        last_asset = Asset.objects.filter(branch=asset.branch).order_by('-created_at').first()

        # Update the balance
        if last_asset:
            old_balance = last_asset.updated_balance
            asset.updated_balance = old_balance + asset.value
        else:
            old_balance = 0
            asset.updated_balance = asset.value

        # Save the asset with the updated balance
        asset.save()

        # Create a detailed audit log for the creation of this asset
        Audit.objects.create(
            action_initiator=self.context['request'].user,  # User who performed the action
            action='create',
            table_name=Asset._meta.db_table,  # The name of the table (model)
            old_value=f"Updated balance before creation: {old_balance}",
            new_value=f"New updated balance: {asset.updated_balance}",
            action_timestamp=asset.created_at  # The timestamp of the action
        )

        return asset



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


class IncomeSerializer(ModelSerializer):
    class Meta:
        model = Income
        fields = '__all__'
        read_only_fields = ['id']


class ExpenseTypeSerializer(ModelSerializer):
    class Meta:
        model = ExpenseType
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class ExpenseSerializer(ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
