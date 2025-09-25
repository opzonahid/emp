from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Department(models.Model):
    name= models.CharField(max_length=100,)
    description=models.TextField(max_length=500, null=True, blank=True)
    is_active= models.BooleanField(default=True)
    is_delete=models.BooleanField(default=False)
    create_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
            return self.name

class Branch(models.Model):
    name= models.CharField(max_length=100,)
    address=models.TextField(max_length=500, null=True, blank=True)
    is_active= models.BooleanField(default=True)
    is_delete=models.BooleanField(default=False)
    create_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
            return self.name

class EmployeeInfo(models.Model):
    Roles=[
        ('intern', 'Intern'),
        ('junior', 'Junior'),
        ('senior', 'Senior'),
        ('lead', 'Lead'),
    ]
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    salary=models.PositiveBigIntegerField(null=True, blank=True)
    department=models.ForeignKey(Department, on_delete=models.CASCADE,related_name='department')
    role=models.CharField(default="intern", choices=Roles,max_length=20)
    address=models.TextField(max_length=500, null=True, blank=True)
    can_view=models.BooleanField(default=True)
    is_active= models.BooleanField(default=True)
    is_delete=models.BooleanField(default=False)
    create_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username

class BranchPermission(models.Model):
    employee = models.ForeignKey(EmployeeInfo, on_delete=models.CASCADE, related_name='branch_permissions')
    branch= models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_employees')

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'), 
        ('completed', 'Completed'), 
        ('in_progress', 'In Progress')
        ]
    
    task = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    def __str__(self):
        return f"{self.task} - {self.status}"
    
class TaksInfo(models.Model):
    employee = models.ForeignKey(EmployeeInfo, on_delete=models.CASCADE, related_name='tasks')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='employee_tasks')
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.user.username} - {self.task.task}"