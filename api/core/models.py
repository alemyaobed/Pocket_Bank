import random
from django.db import models
from uuid import uuid4


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
    current_balance = models.FloatField()
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE)
    status = models.ForeignKey('Status', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = self.generate_account_number()
        super().save(*args, **kwargs)

    def generate_account_number(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(13)])

    def __str__(self):
        return self.account_name

# 2. Status
class Status(models.Model):
    status_name = models.CharField(max_length=20)

    def __str__(self):
        return self.status_name


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    sender_account = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='sent_transactions')
    receiver_account = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='received_transactions')
    transaction_type = models.ForeignKey('TransactionType', on_delete=models.CASCADE)
    initiated_by = models.ForeignKey('accounts.BaseEntity', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    receiver_balance = models.FloatField()
    sender_balance = models.FloatField()
    transaction_amount = models.FloatField()
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    external_reference = models.CharField(max_length=100, blank=True, null=True)
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE)
    transaction_direction = models.ForeignKey('TransactionDirection', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Transaction {self.id}'

# 5. Transaction_type
class TransactionType(models.Model):
    type_name = models.CharField(max_length=40)

    def __str__(self):
        return self.type_name

# 6. Branch
class Branch(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    branch_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    manager = models.ForeignKey('accounts.Employee', on_delete=models.SET_NULL, null=True, related_name='managed_branches')

    def __str__(self):
        return self.name

# 7. Loans
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

# 8. Loan_type
class LoanType(models.Model):
    type_name = models.CharField(max_length=40)

    def __str__(self):
        return self.type_name

# 9. Loan_terms
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

# 10. Interest_rate_type
class InterestRateType(models.Model):
    type_name = models.CharField(max_length=40)

    def __str__(self):
        return self.type_name

# 11. Investments
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

# 12. Loan_payments
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

# 13. Investment_crediting
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



# 18. Audits
class Audit(models.Model):
    entity = models.ForeignKey('accounts.BaseEntity', on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    table_name = models.CharField(max_length=50)
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)
    action_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Audit {self.id}'

# 19. Assets
class Asset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.FloatField()
    updated_balance = models.FloatField()
    asset_type = models.ForeignKey('AssetType', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# 20. Capital
class Capital(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.FloatField()
    updated_balance = models.FloatField()
    capital_type = models.ForeignKey('CapitalType', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# 21. Liabilities
class Liability(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.FloatField()
    updated_balance = models.FloatField()
    liability_type = models.ForeignKey('LiabilityType', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# 23. Annual_balances
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
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE)

    def __str__(self):
        return f'Annual Balance for {self.accounting_year}'


# 25. Transaction_direction
class TransactionDirection(models.Model):
    direction_name = models.CharField(max_length=40)

    def __str__(self):
        return self.direction_name

# 26. Account_type
class AccountType(models.Model):
    type_name = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('accounts.BaseEntity', on_delete=models.SET_NULL, null=True, related_name='account_type_updates')

    def __str__(self):
        return self.type_name

# 27. Investment_type
class InvestmentType(models.Model):
    type_name = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('accounts.BaseEntity', on_delete=models.SET_NULL, null=True, related_name='investment_type_updates')

    def __str__(self):
        return self.type_name

# 28. Asset_type
class AssetType(models.Model):
    type_name = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('accounts.BaseEntity', on_delete=models.SET_NULL, null=True, related_name='asset_type_updates')

    def __str__(self):
        return self.type_name

# 29. Capital_type
class CapitalType(models.Model):
    type_name = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('accounts.BaseEntity', on_delete=models.SET_NULL, null=True, related_name='capital_type_updates')

    def __str__(self):
        return self.type_name

# 30. Liability_type
class LiabilityType(models.Model):
    type_name = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('accounts.BaseEntity', on_delete=models.SET_NULL, null=True, related_name='liability_type_updates')

    def __str__(self):
        return self.type_name

# 31. Income
class Income(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    income_type = models.ForeignKey('IncomeType', on_delete=models.CASCADE)
    received_at = models.DateTimeField()
    amount = models.FloatField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Income {self.id}'

# 32. Income_type
class IncomeType(models.Model):
    type_name = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('accounts.BaseEntity', on_delete=models.SET_NULL, null=True, related_name='income_type_updates')

    def __str__(self):
        return self.type_name

# 33. Expenses
class Expense(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    expense_type = models.ForeignKey('ExpenseType', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Expense {self.id}'

# 34. Expense_type
class ExpenseType(models.Model):
    type_name = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('accounts.BaseEntity', on_delete=models.SET_NULL, null=True, related_name='expense_type_updates')

    def __str__(self):
        return self.type_name

