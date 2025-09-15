from django.contrib import admin
from .models import EmployeeInfo, Department
# Register your models here.
admin.site.register(Department)
admin.site.register(EmployeeInfo)

