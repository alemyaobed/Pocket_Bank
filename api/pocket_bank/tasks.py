from celery import shared_task
from django.utils import timezone
from django.db.models import Sum
from core.models import Asset, Liability, Capital, AnnualBalance
from accounts.models import Branch

@shared_task
def calculate_annual_balance():
    current_year = timezone.now().year
    branches = Branch.objects.all()

    for branch in branches:
        assets_opening_balance = Asset.objects.filter(branch=branch, created_at__year=current_year).aggregate(Sum('value'))['value__sum'] or 0
        assets_closing_balance = Asset.objects.filter(branch=branch, created_at__year=current_year).aggregate(Sum('updated_balance'))['updated_balance__sum'] or 0

        liabilities_opening_balance = Liability.objects.filter(branch=branch, created_at__year=current_year).aggregate(Sum('value'))['value__sum'] or 0
        liabilities_closing_balance = Liability.objects.filter(branch=branch, created_at__year=current_year).aggregate(Sum('updated_balance'))['updated_balance__sum'] or 0

        capital_opening_balance = Capital.objects.filter(branch=branch, created_at__year=current_year).aggregate(Sum('value'))['value__sum'] or 0
        capital_closing_balance = Capital.objects.filter(branch=branch, created_at__year=current_year).aggregate(Sum('updated_balance'))['updated_balance__sum'] or 0

        AnnualBalance.objects.create(
            branch=branch,
            assets_opening_balance=assets_opening_balance,
            assets_closing_balance=assets_closing_balance,
            liability_opening_balance=liabilities_opening_balance,
            liability_closing_balance=liabilities_closing_balance,
            capital_opening_balance=capital_opening_balance,
            capital_closing_balance=capital_closing_balance,
            accounting_year=str(current_year)
        )


@shared_task
def add(x, y):
    return x + y

@shared_task
def print_hello():
    print("Hello, world!")

