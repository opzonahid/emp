from django.contrib import admin
from django_admin_listfilter_dropdown.filters import (
    RelatedDropdownFilter, ChoiceDropdownFilter
)
from django.contrib.auth.models import User
from django import forms
from .models import EmployeeInfo, Department , Task, TaksInfo
from django.utils.safestring import mark_safe
# Register your models here.

class TaskInfoInline(admin.TabularInline):
    model = TaksInfo
    extra = 1
    fields = ('task',)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'department', 'role', 'salary','task_status')
    search_fields = ('user__username', 'department__name', 'role')
    

    list_filter = (
        ('department', RelatedDropdownFilter),
        ('role', ChoiceDropdownFilter),
        'is_active',
        'is_delete',
        )
    change_list_template="admin/employee_change_list.html"
    inlines = [TaskInfoInline]

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ('id', 'user', 'department', 'role', 'salary', 'task_status')
        
        if hasattr(request.user, "employeeinfo") and request.user.employeeinfo.can_view:
            return ('id', 'user', 'department', 'role', 'salary', 'task_status')
        return ('id', 'user', 'department', 'role',)

    
    def task_status(self, obj):
        task_info = obj.tasks.select_related("task").order_by("-assigned_at").first()

        if not task_info:  
            return "No tasks assigned"
        status = task_info.task.status
        task_id = task_info.task.id

        if status in ['pending', 'in_progress']:
            return mark_safe(
                f'<button class="ok" onclick="getTaskDetails(event,{task_id})" '
                f'style="background-color: red; color: white; border: none; padding: 5px 10px; '
                f'border-radius: 4px; cursor: pointer;">{status}</button>'
            )
        if status == 'completed':
            return ""
        
        return "No tasks assigned"
    

    def get_readonly_fields(self, request, obj = ...):
        if obj: 
            return ('department', 'user')
        return super().get_readonly_fields(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['department'].disabled = True
        return form

admin.site.register(EmployeeInfo, EmployeeAdmin)

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
    search_fields = ('name',)
    list_filter = ('is_active', 'is_delete',)

admin.site.register(Department, DepartmentAdmin)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'status', 'deadline')
    fields=( 'task', 'description', 'deadline', 'status')

admin.site.register(Task, TaskAdmin)

