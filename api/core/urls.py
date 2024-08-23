from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AccountViewSet, AccountTypeViewSet, AnnualBalanceViewSet,
    AssetViewSet, AssetTypeViewSet, AuditViewSet,
    CapitalViewSet, CapitalTypeViewSet, ExpenseViewSet, ExpenseTypeViewSet,
    IncomeViewSet, IncomeTypeViewSet, InterestRateTypeViewSet,
    InvestmentViewSet, InvestmentCreditingViewSet, InvestmentTypeViewSet,
    LiabilityViewSet, LiabilityTypeViewSet, LoanViewSet, LoanPaymentViewSet,
    LoanTermsViewSet, LoanTypeViewSet, StatusViewSet, TransactionViewSet,
    TransactionDirectionViewSet, TransactionTypeViewSet
)

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'account-types', AccountTypeViewSet)
router.register(r'annual-balances', AnnualBalanceViewSet)
router.register(r'assets', AssetViewSet)
router.register(r'asset-types', AssetTypeViewSet)
router.register(r'audits', AuditViewSet)
router.register(r'capitals', CapitalViewSet)
router.register(r'capital-types', CapitalTypeViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'expense-types', ExpenseTypeViewSet)
router.register(r'incomes', IncomeViewSet)
router.register(r'income-types', IncomeTypeViewSet)
router.register(r'interest-rate-types', InterestRateTypeViewSet)
router.register(r'investments', InvestmentViewSet)
router.register(r'investment-creditings', InvestmentCreditingViewSet)
router.register(r'investment-types', InvestmentTypeViewSet)
router.register(r'liabilities', LiabilityViewSet)
router.register(r'liability-types', LiabilityTypeViewSet)
router.register(r'loans', LoanViewSet)
router.register(r'loan-payments', LoanPaymentViewSet)
router.register(r'loan-terms', LoanTermsViewSet)
router.register(r'loan-types', LoanTypeViewSet)
router.register(r'statuses', StatusViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'transaction-directions', TransactionDirectionViewSet)
router.register(r'transaction-types', TransactionTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
