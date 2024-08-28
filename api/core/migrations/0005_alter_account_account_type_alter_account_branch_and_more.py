# Generated by Django 4.2.15 on 2024-08-28 16:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_baseentity_is_verified'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0004_alter_transaction_recipient_account_balance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.accounttype'),
        ),
        migrations.AlterField(
            model_name='account',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.branch'),
        ),
        migrations.AlterField(
            model_name='account',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_accounts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='account',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owned_accounts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='account',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.status'),
        ),
        migrations.AlterField(
            model_name='accounttype',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account_type_updates', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='annualbalance',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.branch'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='asset_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.assettype'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.branch'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.status'),
        ),
        migrations.AlterField(
            model_name='assettype',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='asset_type_updates', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='audit',
            name='action_initiator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='capital',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.branch'),
        ),
        migrations.AlterField(
            model_name='capital',
            name='capital_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.capitaltype'),
        ),
        migrations.AlterField(
            model_name='capital',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.status'),
        ),
        migrations.AlterField(
            model_name='capitaltype',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='capital_type_updates', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='expense',
            name='expense_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.expensetype'),
        ),
        migrations.AlterField(
            model_name='expensetype',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='expense_type_updates', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='income',
            name='income_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.incometype'),
        ),
        migrations.AlterField(
            model_name='incometype',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='income_type_updates', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='investment',
            name='from_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='investments_given', to='core.account'),
        ),
        migrations.AlterField(
            model_name='investment',
            name='investment_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.investmenttype'),
        ),
        migrations.AlterField(
            model_name='investment',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.status'),
        ),
        migrations.AlterField(
            model_name='investment',
            name='to_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='investments_received', to='core.account'),
        ),
        migrations.AlterField(
            model_name='investment',
            name='transaction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.transaction'),
        ),
        migrations.AlterField(
            model_name='investmentcrediting',
            name='investment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.investment'),
        ),
        migrations.AlterField(
            model_name='investmentcrediting',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.status'),
        ),
        migrations.AlterField(
            model_name='investmentcrediting',
            name='transaction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.transaction'),
        ),
        migrations.AlterField(
            model_name='investmenttype',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='investment_type_updates', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='liability',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.branch'),
        ),
        migrations.AlterField(
            model_name='liability',
            name='liability_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.liabilitytype'),
        ),
        migrations.AlterField(
            model_name='liability',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.status'),
        ),
        migrations.AlterField(
            model_name='liabilitytype',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='liability_type_updates', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='loan',
            name='from_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='loans_given', to='core.account'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='loan_term',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.loanterms'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='loan_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.loantype'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.status'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='to_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='loans_received', to='core.account'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='transaction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.transaction'),
        ),
        migrations.AlterField(
            model_name='loanpayment',
            name='loan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.loan'),
        ),
        migrations.AlterField(
            model_name='loanpayment',
            name='paid_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='loanpayment',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.status'),
        ),
        migrations.AlterField(
            model_name='loanpayment',
            name='transaction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.transaction'),
        ),
        migrations.AlterField(
            model_name='loanterms',
            name='entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='loanterms',
            name='interest_rate_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.interestratetype'),
        ),
        migrations.AlterField(
            model_name='loanterms',
            name='loan_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.loantype'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.branch'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='initiated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='recipient_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='received_transactions', to='core.account'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='sender_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sent_transactions', to='core.account'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.status'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_direction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.transactiondirection'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.transactiontype'),
        ),
    ]
