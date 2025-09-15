from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Department, EmployeeInfo

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields=['id','name','description']

class UserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name','last_name','email',]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    department = DepartmentSerializer()

    class Meta:
        model = EmployeeInfo
        fields = ['user', 'salary', 'department', 'role', 'address']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        dep_data = validated_data.pop('department')

        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        department, _ = Department.objects.get_or_create(**dep_data)
        employee = EmployeeInfo.objects.create(
            user=user,
            department=department,
            **validated_data
        )

        return employee
