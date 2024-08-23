from django.core.management.base import BaseCommand
from accounts.models import BaseEntity, EntityType, Role, Department, Branch
from django.utils import timezone
from uuid import uuid4
import faker
import random

class Command(BaseCommand):
    help = 'Insert random data into the database'

    def handle(self, *args, **kwargs):
        fake = faker.Faker()

        roles = ['Branch Manager', 'Head of Department', 'Assistant Manager', 'Supervisor', 'Clerk', 'Officer']
        departments = ['Human Resources', 'Finance', 'IT', 'Marketing', 'Operations']
        entity_types = ['Individual', 'Company', 'Non-Profit Organization', 'Government Agency', 'Partnership']
        branches = ['Kumasi', 'Accra', 'Tamale', 'Ho', 'Mampong', 'Wa']



        # Insert data into Role
        for role_name in roles:
            Role.objects.create(role_name=role_name)

        # Insert data into EntityType
        for type_name in entity_types:
            EntityType.objects.create(type_name=type_name)

        # Insert fake data into Branch
        for branch in branches:
            Branch.objects.create(
                name=branch,
                address=fake.address(),
                branch_code=fake.bothify(text='??-###'),
                phone_number=fake.phone_number()
            )

        # Insert data into Department
        branches = list(Branch.objects.all())
        for department_name in departments:
            if branches:
                Department.objects.create(
                    name=department_name,
                    location=fake.city(),
                    telephone=fake.phone_number(),
                    branch=random.choice(branches)
                )

        self.stdout.write(self.style.SUCCESS('Successfully inserted random data'))
