from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from uuid import uuid4


class EntityType(models.Model):
    type_name = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('BaseEntity', on_delete=models.SET_NULL, null=True, related_name='entity_type_updates')

    def __str__(self):
        return self.type_name


class BaseEntityManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        from core.models import Branch

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('tax_identifier_number', 'DEFAULT_TIN')
        extra_fields.setdefault('date_of_birth', '2000-01-01')
        extra_fields.setdefault('branch', Branch.objects.filter(id=1))
        extra_fields.setdefault('phone_number', '000-000-0000')
        extra_fields.setdefault('address', 'Default Address')
        extra_fields.setdefault('entity_type', EntityType.objects.filter(id=1))


        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class BaseEntity(AbstractBaseUser, PermissionsMixin):
# class BaseEntity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    full_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True, null=False)
    entity_type = models.ForeignKey('EntityType', on_delete=models.SET_NULL, null=True)
    address = models.TextField(blank=False, null=False)
    phone_number = models.CharField(max_length=20, unique=True, null=False)
    branch = models.ForeignKey('core.Branch', on_delete=models.SET_NULL, null=True, related_name='employees')
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=False, blank=False)
    last_login = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tax_identifier_number = models.CharField(max_length=50, null=False, blank=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    objects = BaseEntityManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username


# Employees (extends Base_entity)
class Employee(BaseEntity):
    position = models.CharField(max_length=50)
    role = models.ForeignKey('Role', on_delete=models.CASCADE)
    salary = models.FloatField()
    department = models.ForeignKey('Department', on_delete=models.CASCADE)

    def __str__(self):
        return f'Employee {self.full_name}'


class Role(models.Model):
    role_name = models.CharField(max_length=40)

    def __str__(self):
        return self.role_name


class Department(models.Model):
    name = models.CharField(max_length=50)
    head_of_department = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True, related_name='managed_departments')
    location = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    branch = models.ForeignKey('core.Branch', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    entity = models.ForeignKey('BaseEntity', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    recipient = models.ForeignKey('BaseEntity', on_delete=models.CASCADE, related_name='notifications')
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    status = models.ForeignKey('core.Status', on_delete=models.CASCADE)

    def __str__(self):
        return f'Notification {self.id}'
