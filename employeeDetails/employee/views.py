from django.shortcuts import render,get_object_or_404
from .models import Department,EmployeeInfo,Task
from .serializer import DepartmentSerializer,EmployeeSerializer,UserSerializer,TaskSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
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


    
@api_view(['GET',])
def get_last_employee_task(request, pk):
    last_task_info = get_object_or_404(Task, pk=pk)
    print(last_task_info)
    if request.method == 'GET':
        if not last_task_info:
            return Response({"detail": "No tasks assigned"}, status=404)

        data = {
            "id": last_task_info.task.id,
            "task": last_task_info.task.task,
            "description": last_task_info.task.description,
            "deadline": last_task_info.task.deadline,
            "status": last_task_info.task.status,
            "assigned_at": last_task_info.assigned_at,
        }
        return Response(data)
class TaskUpdateDestryView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Task.objects.all()
    serializer_class=TaskSerializer

