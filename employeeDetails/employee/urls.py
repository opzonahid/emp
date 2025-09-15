from django.contrib import admin
from django.urls import path
# from .views import (DepartmentListCreateView, DepartmentUpdateDestryView,
from .views import (EmployeeInfoListCreateView,EmployeeListUpdateDestryView)
urlpatterns = [
    # path('/dep/list/', DepartmentListCreateView.as_view(), name="department"),
    # path('/dep/<int:pk>/',DepartmentUpdateDestryView.as_view(), name="department" ),
    path('emp/list/',EmployeeInfoListCreateView.as_view(), name="department" ),
    path('emp/<int:pk>/',EmployeeListUpdateDestryView.as_view(), name="department" ),
]
