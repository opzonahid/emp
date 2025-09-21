from django.contrib import admin
from django.urls import path
# from .views import (DepartmentListCreateView, DepartmentUpdateDestryView,
from .views import (EmployeeInfoListCreateView,EmployeeListUpdateDestryView,get_last_employee_task, TaskUpdateDestryView)
urlpatterns = [
    # path('/dep/list/', DepartmentListCreateView.as_view(), name="department"),
    # path('/dep/<int:pk>/',DepartmentUpdateDestryView.as_view(), name="department" ),
    path('emp/list/',EmployeeInfoListCreateView.as_view(), name="department" ),
    path('emp/<int:pk>/',EmployeeListUpdateDestryView.as_view(), name="department" ),
    path('task/<int:pk>/',get_last_employee_task, name="tasks" ),
    path('update/task/<int:pk>/',TaskUpdateDestryView.as_view(), name="update_tasks" ),
]
