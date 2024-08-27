from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import (
    Account, Asset, AssetType, CapitalType, Expense, Status, Transaction, Audit, Capital, TransactionDirection,
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
                table_name='Account, Capital, Asset, Transaction',
                old_value=None,
                new_value=str(instance),
            )

            # Create or update Capital object
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

            # Create or update Asset object
            asset_type = AssetType.objects.get(type_name='Cash')  # Adjust as necessary
            last_asset = Asset.objects.filter(branch=created_by.branch, asset_type=asset_type).last()
            if last_asset:
                updated_balance = last_asset.updated_balance + instance.current_balance
            else:
                updated_balance = instance.current_balance

            Asset.objects.create(
                branch=created_by.branch,
                name=f'Asset from account {instance.id} in the form of cash',
                value=instance.current_balance,
                updated_balance=updated_balance,
                asset_type=asset_type,
                status=Status.objects.get(status_name='Active'),
                description=f'Asset created for account {instance.id}'
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

                # Create an audit entry for loan creation
                Audit.objects.create(
                    action_initiator=instance.from_account.owner,
                    action=f"Loan created: Loan ID {instance.id}, Amount: {instance.loan_amount}, To Account: {instance.to_account.account_name}",
                    table_name='Loan',
                    old_value=None,
                    new_value=str(instance),
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
                transaction_record = Transaction(
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

                transaction_record.save()

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

                # Create an audit entry for income creation
                Audit.objects.create(
                    action_initiator=None,  # Assuming no specific user initiated this action
                    action=f"Income recorded: Income ID {instance.id}, Amount: {instance.amount}, Description: {instance.description}",
                    table_name='Income, Transaction, Capital',
                    old_value=None,
                    new_value=str(instance),
                )

        except Account.DoesNotExist:
            raise ValidationError("Bank account not found.")
        except Exception as e:
            print(f"An error occurred while handling income creation: {e}")
            transaction.set_rollback(True)

@receiver(post_save, sender=Transaction)
def handle_transaction_creation(sender, instance, created, **kwargs):
    if created:
        try:
            with transaction.atomic():
                affected_tables = []
                if instance.transaction_type.type_name == 'Deposit':

                    created_by = instance.initiated_by
                    # Update recipient account balance
                    instance.recipient_account.current_balance += instance.transaction_amount
                    instance.recipient_account.save()
                    instance.recipient_account_balance = instance.recipient_account.current_balance
                    instance.save()

                    # Update capital if necessary
                    last_capital = Capital.objects.filter(branch=instance.branch).last()
                    if last_capital:
                        updated_balance = last_capital.updated_balance + instance.transaction_amount
                    else:
                        updated_balance = instance.transaction_amount

                    Capital.objects.create(
                        branch=instance.branch,
                        name='Bank Capital',
                        capital_type=CapitalType.objects.get(type_name='Equity Capital'),
                        value=instance.transaction_amount,
                        updated_balance=updated_balance,
                        status=Status.objects.get(status_name='Completed'),
                        description=f"Capital update from deposit transaction '{instance.id}'",
                    )

                    # Create or update Asset object
                    asset_type = AssetType.objects.get(type_name='Cash')  # Adjust as necessary
                    last_asset = Asset.objects.filter(branch=created_by.branch, asset_type=asset_type).last()
                    if last_asset:
                        updated_balance = last_asset.updated_balance + instance.current_balance
                    else:
                        updated_balance = instance.current_balance

                    Asset.objects.create(
                        branch=created_by.branch,
                        name=f'Asset from account {instance.id} in the form of cash as deposit',
                        value=instance.current_balance,
                        updated_balance=updated_balance,
                        asset_type=asset_type,
                        status=Status.objects.get(status_name='Active'),
                        description=f'Asset created for account {instance.id}'
                    )

                    affected_tables.extend(['Transaction', 'Capital', 'Asset'])

                elif instance.transaction_type.type_name == 'Withdrawal':
                    # Update account balance
                    instance.sender_account.current_balance -= instance.transaction_amount
                    instance.sender_account.save()
                    instance.sender_account_balance = instance.sender_account.current_balance
                    instance.save()

                    # Update capital if necessary
                    last_capital = Capital.objects.filter(branch=instance.branch).last()
                    if last_capital:
                        updated_balance = last_capital.updated_balance - instance.transaction_amount
                    else:
                        updated_balance = -instance.transaction_amount

                    Capital.objects.create(
                        branch=instance.branch,
                        name='Bank Capital',
                        capital_type=CapitalType.objects.get(type_name='Equity Capital'),
                        value=-instance.transaction_amount,
                        updated_balance=updated_balance,
                        status=Status.objects.get(status_name='Completed'),
                        description=f"Capital update from withdrawal transaction '{instance.id}'",
                    )

                    # Create or update Asset object
                    asset_type = AssetType.objects.get(type_name='Cash')  # Adjust as necessary
                    last_asset = Asset.objects.filter(branch=created_by.branch, asset_type=asset_type).last()
                    if last_asset:
                        updated_balance = last_asset.updated_balance - instance.current_balance
                    else:
                        updated_balance = -instance.current_balance

                    Asset.objects.create(
                        branch=created_by.branch,
                        name=f'Asset from account {instance.id} in the form of cash as deposit',
                        value=instance.current_balance,
                        updated_balance=updated_balance,
                        asset_type=asset_type,
                        status=Status.objects.get(status_name='Active'),
                        description=f'Asset created for account {instance.id}'
                    )

                    affected_tables.extend(['Transaction', 'Capital', 'Asset'])

                elif instance.transaction_type.type_name in ['Transfer', 'Charge', 'Refund', 'Fee', 'Interest Crediting', 'Adjustment', 'Loan Disbursement']:
                    # Update sender and recipient account balances
                    instance.sender_account.current_balance -= instance.transaction_amount
                    instance.sender_account.save()

                    instance.recipient_account.current_balance += instance.transaction_amount
                    instance.recipient_account.save()

                    instance.recipient_account_balance = instance.recipient_account.current_balance
                    instance.sender_account_balance = instance.sender_account.current_balance
                    instance.save()

                    affected_tables.extend(['Transaction, Account'])
                elif instance.transaction_type.type_name in ['Payment', 'Purchase']:
                    # Update account balance
                    instance.sender_account.current_balance -= instance.transaction_amount
                    instance.sender_account.save()

                    # Record expense if necessary
                    Expense.objects.create(
                        name=f"{instance.transaction_type.type_name} for transaction {instance.id}",
                        amount=instance.transaction_amount,
                        description=instance.description,
                        branch=instance.branch,
                        status=Status.objects.get(status_name='Completed')
                    )
                    affected_tables.append('Expense')
                    if instance.transaction_type.type_name == 'Purchase':
                        # Update asset if necessary
                        asset_type = AssetType.objects.get(type_name='Inventory')
                        last_asset = Asset.objects.filter(branch=instance.branch, asset_type=asset_type).last()
                        if last_asset:
                            updated_balance = last_asset.updated_balance + instance.transaction_amount
                        else:
                            updated_balance = instance.transaction_amount

                        Asset.objects.create(
                            branch=instance.branch,
                            name=f'Inventory purchased for transaction {instance.id}',
                            value=instance.transaction_amount,
                            updated_balance=updated_balance,
                            asset_type=asset_type,
                            status=Status.objects.get(status_name='Active'),
                            description=f'Inventory purchased for transaction {instance.id}'
                        )

                        affected_tables.append('Asset')

        except Exception as e:
            print(f"An error occurred while handling transaction creation: {e}")
            transaction.set_rollback(True)
