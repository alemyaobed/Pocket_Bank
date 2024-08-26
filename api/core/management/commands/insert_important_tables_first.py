from django.core.management.base import BaseCommand
from core.models import (Status, TransactionType, LoanType, InterestRateType,
                         TransactionDirection, AccountType, InvestmentType, AssetType,
                         CapitalType, LiabilityType, IncomeType, ExpenseType,)

import faker

class Command(BaseCommand):
    help = 'Insert random data into the database'

    def handle(self, *args, **kwargs):
        fake = faker.Faker()

        # Definition of meaningful choices for each model
        loan_types = ['Personal Loan', 'Home Loan', 'Car Loan', 'Education Loan', 'Business Loan']
        interest_rate_types = ['Fixed', 'Variable', 'Hybrid', 'Promotional', 'Introductory']
        transaction_directions = ['Internal', 'External']
        account_types = ['Savings', 'Current','Checking', 'Business', 'Investment', 'Retirement']
        investment_types = ['Stocks', 'Bonds', 'Real Estate', 'Mutual Funds', 'Commodities']
        asset_types = ['Real Estate', 'Vehicles', 'Equipment', 'Intellectual Property', 'Cash']
        capital_types = ['Equity Capital', 'Debt Capital', 'Working Capital', 'Venture Capital', 'Fixed Capital']
        liability_types = ['Short-term Debt', 'Long-term Debt', 'Accounts Payable', 'Accrued Expenses', 'Deferred Tax']
        income_types = ['Fee charges', 'Business Income', 'Interest Income', 'Rental Income', 'Investment Income']
        expense_types = ['Utilities', 'Salaries', 'Rent', 'Office Supplies', 'Travel']


        # Define a list of statuses
        statuses = [
            'Active',
            'Inactive',
            'Pending',
            'Approved',
            'Rejected',
            'Completed',
            'Failed',
            'Cancelled',
            'Under Review',
            'Processed',
            'Sent',
            'Delivered',
            'Read',
            'Acknowledged'
        ]

        transaction_types = [
            'Deposit',
            'Withdrawal',
            'Transfer',
            'Payment',
            'Refund',
            'Charge',
            'Fee',
            'Interest',
            'Adjustment',
            'Settlement'
        ]

        # Clear existing data if needed
        Status.objects.all().delete()

        # Insert statuses
        for status_name in statuses:
            Status.objects.create(status_name=status_name)

        # Clear existing data if needed
        TransactionType.objects.all().delete()

        # Insert transaction types
        for type_name in transaction_types:
            TransactionType.objects.create(type_name=type_name)

        # Insert data into LoanType
        for type_name in loan_types:
            LoanType.objects.create(type_name=type_name)

        # Insert data into InterestRateType
        for type_name in interest_rate_types:
            InterestRateType.objects.create(type_name=type_name)

        # Insert data into TransactionDirection
        for direction_name in transaction_directions:
            TransactionDirection.objects.create(direction_name=direction_name)

        # Insert data into AccountType
        for type_name in account_types:
            AccountType.objects.create(type_name=type_name)

        # Insert data into InvestmentType
        for type_name in investment_types:
            InvestmentType.objects.create(type_name=type_name)

        # Insert data into AssetType
        for type_name in asset_types:
            AssetType.objects.create(type_name=type_name)

        # Insert data into CapitalType
        for type_name in capital_types:
            CapitalType.objects.create(type_name=type_name)

        # Insert data into LiabilityType
        for type_name in liability_types:
            LiabilityType.objects.create(type_name=type_name)

        # Insert data into IncomeType
        for type_name in income_types:
            IncomeType.objects.create(type_name=type_name)

        # Insert data into ExpenseType
        for type_name in expense_types:
            ExpenseType.objects.create(type_name=type_name)

        self.stdout.write(self.style.SUCCESS('Successfully inserted random data'))
