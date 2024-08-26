from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import (
    Account, Asset, AssetType, CapitalType, Status, Transaction, Audit, Capital, TransactionDirection,
    TransactionType, Loan, LiabilityType, Liability, Income
    )
# Handles account creation
@receiver(post_save, sender=Account)
def handle_account_creation(sender, instance, created, **kwargs):
    if created:
        try:
            created_by = instance.created_by

            # Create an initial transaction for the account
            Transaction.objects.create(
                sender_account=None,  # Assuming no sender for account creation
                recipient_account=instance,
                transaction_type=TransactionType.objects.get(type_name='Account Creation'),
                initiated_by=instance.owner,  # or a default system user
                description=f'Account {instance.account_name} created',
                recipient_account_balance=instance.current_balance,
                sender_account_balance=instance.current_balance,
                transaction_amount=0,  # No amount for creation
                status=Status.objects.get(status_name='Completed'),
                branch=created_by.branch,
                transaction_direction=TransactionDirection.objects.get(direction='External'),
            )

            # Log the creation in the Audit table
            Audit.objects.create(
                action_initiator=created_by,
                action=f"Created an account '{instance.account_number}' for '{instance.account_name}'",
                table_name='Account',
                old_value=None,
                new_value=str(instance),
            )

            # Create a Capital object based on branch and and update branch capital
            last_capital = Capital.objects.filter(branch=created_by.branch).last()
            if last_capital:
                updated_balance = last_capital.updated_balance + instance.current_balance
            else:
                updated_balance = instance.current_balance

            Capital.objects.create(
                name='Bank Capital',  # Assuming a unique entry for the bank's overall capital
                branch=created_by.branch,
                capital_type=CapitalType.objects.get(type_name='Equity Capital'),
                value=instance.current_balance,
                updated_balance=updated_balance,
                status=Status.objects.get(status_name='Completed'),
                description=f"Initial capital from account '{instance.account_name}' creation",
            )

        except Exception as e:
            # Handle exceptions or log errors
            print(f"An error occurred while handling account creation: {e}")
            # Rollback any partial changes if needed
            transaction.set_rollback(True)


@receiver(pre_save, sender=Loan)
def handle_loan_creation(sender, instance, **kwargs):
    if instance.pk is None:  # Check if the instance is being created
        try:
            with transaction.atomic():
                # Fetch the bank's account (assuming you have a unique identifier for it)
                bank_account = Account.objects.get(account_number='4352958644329')

                if instance.from_account != bank_account:
                    raise ValidationError("The 'from_account' must be the bank's account.")

                # Check if sufficient balance is available in the bank account
                if bank_account.current_balance < instance.loan_amount:
                    raise ValidationError("Insufficient funds in the bank account.")

                # Create the transaction to debit the bank's account
                transaction_record = Transaction(
                    sender_account=bank_account,
                    recipient_account=instance.to_account,
                    transaction_type=TransactionType.objects.get(type_name='Loan Disbursement'),
                    initiated_by=instance.from_account.owner,
                    description=f'Loan disbursement of {instance.loan_amount} to {instance.to_account.account_name}',
                    recipient_account_balance=instance.to_account.current_balance + instance.loan_amount,
                    sender_account_balance=bank_account.current_balance - instance.loan_amount,
                    transaction_amount=instance.loan_amount,
                    status=Status.objects.get(status_name='Completed'),
                    branch=instance.from_account.branch,
                    transaction_direction=TransactionDirection.objects.get(direction='Internal')
                )

                transaction_record.save()

                # Update the bank's account balance
                bank_account.current_balance -= instance.loan_amount
                bank_account.save()

                # Update the recipient's account balance
                instance.to_account.current_balance += instance.loan_amount
                instance.to_account.save()

                # Record the loan as an asset (accounts receivable)
                try:
                    asset_type = AssetType.objects.get(type_name='Accounts Receivable')
                except AssetType.DoesNotExist:
                    raise ValidationError("Asset type for accounts receivable not found.")

                # Create or update the bank's receivables
                last_asset = Asset.objects.filter(branch=bank_account.branch, asset_type=asset_type).last()
                if last_asset:
                    updated_balance = last_asset.updated_balance + instance.loan_amount
                else:
                    updated_balance = instance.loan_amount

                Asset.objects.create(
                    branch=bank_account.branch,
                    name=f'Loan Receivable for loan {instance.id}',
                    value=instance.loan_amount,
                    updated_balance=updated_balance,
                    asset_type=asset_type,
                    status=Status.objects.get(status_name='Active'),
                    description=f'Loan receivable for loan {instance.id}'
                )

        except Exception as e:
            print(f"An error occurred while handling loan creation: {e}")
            transaction.set_rollback(True)

@receiver(post_save, sender=Income)
def handle_income_creation(sender, instance, created, **kwargs):
    if created:
        try:
            with transaction.atomic():
                # Fetch the bank's account (assuming you have a unique identifier for it)
                bank_account = Account.objects.get(account_number='4352958644329')

                # Create a transaction to record the income
                Transaction.objects.create(
                    sender_account=None,  # Income might not have a sender
                    recipient_account=bank_account,
                    transaction_type=TransactionType.objects.get(type_name='Income'),
                    initiated_by=None,  # Or use a default system user
                    description=instance.description or f'Income received: {instance.amount}',
                    recipient_account_balance=bank_account.current_balance + instance.amount,
                    sender_account_balance=bank_account.current_balance,  # Sender account might be None
                    transaction_amount=instance.amount,
                    status=Status.objects.get(status_name='Completed'),
                    branch=bank_account.branch,
                    transaction_direction=TransactionDirection.objects.get(direction='Internal'),
                )

                # Update the bank's account balance
                bank_account.current_balance += instance.amount
                bank_account.save()

                # Update the capital
                last_capital = Capital.objects.filter(branch=bank_account.branch).last()
                if last_capital:
                    updated_balance = last_capital.updated_balance + instance.amount
                else:
                    updated_balance = instance.amount

                Capital.objects.create(
                    name='Bank Capital',  # Assuming a unique entry for the bank's overall capital
                    branch=bank_account.branch,
                    capital_type=CapitalType.objects.get(type_name='Equity Capital'),
                    value=instance.amount,
                    updated_balance=updated_balance,
                    status=Status.objects.get(status_name='Completed'),
                    description=f"Capital update from income record '{instance.id}'",
                )

        except Account.DoesNotExist:
            raise ValidationError("Bank account not found.")
        except Exception as e:
            print(f"An error occurred while handling income creation: {e}")
            transaction.set_rollback(True)
