from django.contrib import admin
from django_admin_listfilter_dropdown.filters import (
    RelatedDropdownFilter, ChoiceDropdownFilter
)
from django.contrib.auth.models import User
from django.urls import reverse
from django import forms
from .models import EmployeeInfo, Department , Task, TaksInfo, Branch,BranchPermission
from django.utils.safestring import mark_safe
# Register your models here.

class TaskInfoInline(admin.TabularInline):
    model = TaksInfo
    extra = 1
    fields = ('task',)

class BranchPermissionInline(admin.TabularInline):
    model = BranchPermission
    extra = 1
    fields = ('branch',)


class EmployeeAdmin(admin.ModelAdmin):
    # list_display = ('id', 'user', 'department', 'role', 'salary','branch','task_status')
    search_fields = ('user__username', 'department__name', 'role')
    

    list_filter = (
        ('department', RelatedDropdownFilter),
        ('role', ChoiceDropdownFilter),
        'is_active',
        'is_delete',
        )
    change_list_template="admin/employee_change_list.html"
    inlines = [TaskInfoInline, BranchPermissionInline]

    def get_list_display(self, request):
        
        if request.user.is_superuser:
            return ('id', 'user', 'department', 'role', 'salary', 'get_branches','pdf','excle', 'task_status')
        
        if request.user.is_staff:
            return ('id', 'user', 'department', 'role', 'salary', 'task_status')
        return ('id', 'user', 'department', 'get_branches', 'role')
    
    def pdf(self, obj):
        url = reverse("employee_task_pdf", args=[obj.id])
        return mark_safe(f'<a href="{url}" target="_blank">PDF</a>')
    pdf.short_description = "PDF"
    
    def excle(self,obj):
        url = reverse('employee_task_excel', args=[obj.id])
        return mark_safe(f'<a href="{url}" target="_blank">Excle</a>')
    excle.short_description = "Excle"


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
    
    task_status.short_description = 'Latest Task Status'

    


    def get_branches(self, obj):
        branch_permissions = BranchPermission.objects.filter(employee=obj).select_related("branch")
        if obj.can_view:
            return "All Branches"
        
        if not branch_permissions.exists():
            return "No Branch Assigned"
        return ", ".join([bp.branch.name for bp in branch_permissions])
    get_branches.short_description = 'Branches'
    

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

class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address')
    search_fields = ('name', 'address')
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        employee = EmployeeInfo.objects.filter(user=request.user).first()

        if request.user.is_superuser:
            return qs
        
        if employee:
            if employee.can_view:
                return qs
            assigned_branch_ids = BranchPermission.objects.filter(employee=employee).values_list("branch_id", flat=True)
            return qs.filter(id__in=assigned_branch_ids)
        
        return qs.none()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "branch" and not request.user.is_superuser:
            employee = EmployeeInfo.objects.filter(user=request.user).first()
            if employee:
                if employee.can_view:
                    kwargs["queryset"] = Branch.objects.all()
                else:
                    assigned_branch_ids = BranchPermission.objects.filter(employee=employee).values_list("branch_id", flat=True)
                    kwargs["queryset"] = Branch.objects.filter(id__in=assigned_branch_ids)
            else:
                kwargs["queryset"] = Branch.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Branch, BranchAdmin)