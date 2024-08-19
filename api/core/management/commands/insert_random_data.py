from django.core.management.base import BaseCommand
from accounts.models import BaseEntity, EntityType, Role, Department, Status, TransactionType, Branch, LoanType, InterestRateType, TransactionDirection, AccountType, InvestmentType, AssetType, CapitalType, LiabilityType, IncomeType, ExpenseType
from django.utils import timezone
from uuid import uuid4
import faker

class Command(BaseCommand):
    help = 'Insert random data into the database'

    def handle(self, *args, **kwargs):
        fake = faker.Faker()

        # Create BaseEntity instances for foreign keys
        base_entity = BaseEntity.objects.create(
            id=uuid4(),
            full_name=fake.name(),
            username=fake.user_name(),
            email=fake.email(),
            address=fake.address(),
            phone_number=fake.phone_number(),
            branch=None,  # Assuming branch can be null for this example
            is_active=True,
            is_staff=False,
            date_of_birth=fake.date_of_birth(),
            tax_identifier_number=fake.ssn(),
            first_name=fake.first_name(),
            last_name=fake.last_name()
        )

        # Insert random data into models
        for model in [EntityType, Role, Department, Status, TransactionType, Branch, LoanType, InterestRateType, TransactionDirection, AccountType, InvestmentType, AssetType, CapitalType, LiabilityType, IncomeType, ExpenseType]:
            for _ in range(5):
                model.objects.create(
                    type_name=fake.word(),
                    updated_by=base_entity
                )

        self.stdout.write(self.style.SUCCESS('Successfully inserted random data'))
