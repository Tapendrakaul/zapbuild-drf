from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

ADMIN = 1
MANAGER = 2
CLIENT = 3
EMPLOYEE = 4

USER_ROLE = [(ADMIN, "admin"),(MANAGER, "Sub-Admin"),(CLIENT, "Company"),(EMPLOYEE, "HR"), ]


"""
user model
"""
class User(AbstractUser):
    username    = models.CharField(max_length=150,null=True,blank=True,unique=True)
    full_name   = models.CharField(max_length=150,null=True,blank=True)
    email       = models.EmailField("email address",unique=True,blank=True, null=True)
    role_id     = models.PositiveIntegerField(choices=USER_ROLE, default=1)
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        managed = True;
        db_table = 'tbl_user'
    
    def __str__(self):
        return str(self.username)



# Create your models here.
class Task(models.Model):

    PENDING = 0
    COMPLETE = 1
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (COMPLETE, 'Complete'),
    )

    created_by          = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name="task_creator",)
    assigned_to         = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name="task_assigned",)
    title               = models.CharField(max_length=255)
    description         = models.TextField(null=True,blank=True)
    task_date           = models.DateTimeField(auto_now_add=False,auto_now=False,null=True,blank=True)
    status              = models.PositiveIntegerField(choices=STATUS_CHOICES, default=PENDING)
    created_at          = models.DateTimeField(auto_now_add=True, null=True)
    updated_at          = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title

