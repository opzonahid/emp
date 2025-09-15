from django.shortcuts import render
from .models import Department,EmployeeInfo
from .serializer import DepartmentSerializer,EmployeeSerializer,UserSerializer
from rest_framework import generics
from rest_framework.response import Response

# Create your views here.

class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset=Department.objects.all()
    serializer_class=DepartmentSerializer

class DepartmentUpdateDestryView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Department.objects.all()
    serializer_class=DepartmentSerializer

class EmployeeInfoListCreateView(generics.ListCreateAPIView):
    queryset = EmployeeInfo.objects.select_related('user', 'department').all()
    serializer_class = EmployeeSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = []
        for employee in queryset:
            data.append({
                'id': employee.id,
                'user': employee.user.username,
                'department': employee.department.name,
                'role': employee.role,
                'salary': employee.salary,

            })
        return Response(data)


class EmployeeListUpdateDestryView(generics.RetrieveUpdateDestroyAPIView):
    queryset=EmployeeInfo.objects.select_related('user','department').all()
    serializer_class=EmployeeSerializer
