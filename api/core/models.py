import random
from django.db import models
from uuid import uuid4

from django.core.exceptions import ValidationError


class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    account_name = models.CharField(max_length=40)
    account_number = models.CharField(max_length=20, unique=True)
    owner = models.ForeignKey('accounts.BaseEntity', on_delete=models.CASCADE, null=False)
    account_type = models.ForeignKey('AccountType', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(blank=True, null=True)
    current_balance = models.FloatField(default=80)
    branch = models.ForeignKey('accounts.Branch', on_delete=models.CASCADE)
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    created_by = models.ForeignKey('accounts.BaseEntity', on_delete=models.CASCADE, related_name='created_accounts')

    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = self.generate_account_number()
        super().save(*args, **kwargs)

    def generate_account_number(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(13)])

    def __str__(self):
        return self.account_name


class Status(models.Model):
    status_name = models.CharField(max_length=20)

    def __str__(self):
        return self.status_name


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    sender_account = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='sent_transactions', null=True)
    recipient_account = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='received_transactions', null=True)
    transaction_type = models.ForeignKey('TransactionType', on_delete=models.CASCADE)
    initiated_by = models.ForeignKey('accounts.BaseEntity', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    recipient_account_balance = models.FloatField(null=True, blank=True)
    sender_account_balance = models.FloatField(null=True, blank=True)
    transaction_amount = models.FloatField()
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    external_reference = models.CharField(max_length=100, blank=True, null=True)
    branch = models.ForeignKey('accounts.Branch', on_delete=models.CASCADE)
    transaction_direction = models.ForeignKey('TransactionDirection', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.transaction_direction.direction == 'Internal':
            if not self.sender_account or not self.recipient_account:
                raise ValidationError("Both sender and receiver accounts must be set for internal transactions.")
            if self.sender_account.current_balance - self.transaction_amount < 80:
                raise ValidationError("Insufficient funds in sender account.")
            if self.sender_account == self.recipient_account:
                raise ValidationError("Sender and receiver accounts cannot be the same.")

        elif self.transaction_direction.direction == 'External':
            if self.sender_account and self.recipient_account:
                raise ValidationError("Only one of sender or receiver account should be set for external transactions.")
            if not self.external_reference:
                raise ValidationError("External reference must be provided for external transactions.")
            if self.sender_account:
                if self.sender_account.current_balance - self.transaction_amount < 80:
                    raise ValidationError("Insufficient funds in account.")
            if self.receiver_account:
                if self.recipient_account.current_balance - self.transaction_amount < 80:
                    raise ValidationError("Insufficient funds in account.")
        else:
            raise ValidationError("Invalid transaction direction.")

    def __str__(self):
        return f'Transaction {self.id}'


class TransactionType(models.Model):
    type_name = models.CharField(max_length=40)

    def __str__(self):
        return self.type_name


class Loan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    from_account = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='loans_given')
    to_account = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='loans_received')
    loan_type = models.ForeignKey('LoanType', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(blank=True, null=True)
    interest_rate = models.FloatField()
    disbursement_date = models.DateField()
    loan_amount = models.FloatField()
    fully_paid = models.BooleanField(default=False)
    current_loan_amount = models.FloatField()
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    loan_term = models.ForeignKey('LoanTerms', on_delete=models.CASCADE)
    transaction = models.ForeignKey('Transaction', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Loan {self.id}'


class LoanType(models.Model):
    type_name = models.CharField(max_length=40)

    def __str__(self):
        return self.type_name


class LoanTerms(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    entity = models.ForeignKey('accounts.BaseEntity', on_delete=models.CASCADE)
    loan_type = models.ForeignKey('LoanType', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    interest_rate_type = models.ForeignKey('InterestRateType', on_delete=models.CASCADE)
    term_duration = models.IntegerField()  # Duration in months or years
    payment_frequency = models.CharField(max_length=20)  # E.g., Monthly, Quarterly
    late_fee = models.FloatField()
    prepayment_penalty = models.FloatField()
    collateral = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Terms for {self.loan_type}'


class InterestRateType(models.Model):
    type_name = models.CharField(max_length=40)

    def __str__(self):
        return self.type_name

class Investment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    from_account = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='investments_given')
    to_account = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='investments_received')
    investment_type = models.ForeignKey('InvestmentType', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(blank=True, null=True)
    interest_rate = models.FloatField()
    principal = models.FloatField()
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    transaction = models.ForeignKey('Transaction', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Investment {self.id}'


class LoanPayment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    paid_by = models.ForeignKey('accounts.BaseEntity', on_delete=models.CASCADE)
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_amount = models.FloatField()
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    loan = models.ForeignKey('Loan', on_delete=models.CASCADE)
    interest_paid = models.FloatField()
    principal_paid = models.FloatField()

    def __str__(self):
        return f'Loan Payment {self.id}'


class InvestmentCrediting(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_amount = models.FloatField()
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    investment = models.ForeignKey('Investment', on_delete=models.CASCADE)
    interest_earned = models.FloatField()

    def __str__(self):
        return f'Investment Crediting {self.id}'


class Audit(models.Model):
    action_initiator = models.ForeignKey('accounts.BaseEntity', on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    table_name = models.CharField(max_length=50)
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)
    action_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Audit {self.id}'


class Asset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    branch = models.ForeignKey('accounts.Branch', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.FloatField()
    updated_balance = models.FloatField()
    asset_type = models.ForeignKey('AssetType', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Capital(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    branch = models.ForeignKey('accounts.Branch', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.FloatField()
    updated_balance = models.FloatField()
    capital_type = models.ForeignKey('CapitalType', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Liability(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    branch = models.ForeignKey('accounts.Branch', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.FloatField()
    updated_balance = models.FloatField()
    liability_type = models.ForeignKey('LiabilityType', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class AnnualBalance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    assets_opening_balance = models.FloatField()
    assets_closing_balance = models.FloatField()
    capital_opening_balance = models.FloatField()
    capital_closing_balance = models.FloatField()
    liability_opening_balance = models.FloatField()
    liability_closing_balance = models.FloatField()
    accounting_year = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    branch = models.ForeignKey('accounts.Branch', on_delete=models.CASCADE)

    def __str__(self):
        return f'Annual Balance for {self.accounting_year}'


class TransactionDirection(models.Model):
    direction = models.CharField(max_length=10, choices=[('Internal', 'Internal'), ('External', 'External')])

    def __str__(self):
        return self.direction_name


class AccountType(models.Model):
    type_name = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('accounts.BaseEntity', on_delete=models.SET_NULL, null=True, related_name='account_type_updates')

    def __str__(self):
        return self.type_name


class InvestmentType(models.Model):
    type_name = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('accounts.BaseEntity', on_delete=models.SET_NULL, null=True, related_name='investment_type_updates')

    def __str__(self):
        return self.type_name


class AssetType(models.Model):
    type_name = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('accounts.BaseEntity', on_delete=models.SET_NULL, null=True, related_name='asset_type_updates')

    def __str__(self):
        return self.type_name


class CapitalType(models.Model):
    type_name = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('accounts.BaseEntity', on_delete=models.SET_NULL, null=True, related_name='capital_type_updates')

    def __str__(self):
        return self.type_name


class LiabilityType(models.Model):
    type_name = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('accounts.BaseEntity', on_delete=models.SET_NULL, null=True, related_name='liability_type_updates')

    def __str__(self):
        return self.type_name


class Income(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    income_type = models.ForeignKey('IncomeType', on_delete=models.CASCADE)
    received_at = models.DateTimeField()
    amount = models.FloatField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Income {self.id}'


class IncomeType(models.Model):
    type_name = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('accounts.BaseEntity', on_delete=models.SET_NULL, null=True, related_name='income_type_updates')

    def __str__(self):
        return self.type_name


class Expense(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    expense_type = models.ForeignKey('ExpenseType', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Expense {self.id}'


class ExpenseType(models.Model):
    type_name = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('accounts.BaseEntity', on_delete=models.SET_NULL, null=True, related_name='expense_type_updates')

    def __str__(self):
        return self.type_name

