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


class EmployeeInfo(models.Model):
    Roles={
        'junior':"junior",
        'senior':"Senior",
        'intern':"intern",
    }
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    salary=models.DecimalField(decimal_places=2,max_digits=10)
    department=models.ForeignKey(Department, on_delete=models.CASCADE,related_name='department')
    role=models.CharField(default="intern", choices=Roles)
    address=models.TextField(max_length=500, null=True, blank=True)
    is_active= models.BooleanField(default=True)
    is_delete=models.BooleanField(default=False)
    create_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
