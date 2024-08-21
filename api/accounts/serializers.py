from rest_framework.serializers import ModelSerializer
from .models import (
    Employee, EntityType, BaseEntity, Notification, Document,
    Department, Role,
    )

class EntityTypeSerializer(ModelSerializer):
    class Meta:
        model = EntityType
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'updated_by']

    def update(self, instance, validated_data):
        # Set the updated_by field to the current user
        request = self.context.get('request', None)
        if request and hasattr(request, 'user'):
            validated_data['updated_by'] = request.user

        return super().update(instance, validated_data)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class BaseEntitySerializer(ModelSerializer):
    class Meta:
        model = BaseEntity
        fields = '__all__'
        read_only_fields = ['id', 'last_login', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class EmployeeSerializer(BaseEntitySerializer):
    class Meta(BaseEntitySerializer.Meta):
        model = Employee
        fields = BaseEntitySerializer.Meta.fields + ['position', 'role', 'salary', 'department']


class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class DocumentSerializer(ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']



class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

