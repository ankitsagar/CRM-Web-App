from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    roles = (
        ('Superuser', 'Superuser'),
        ('Manager', 'Manager'),
        ('Salesman', 'Salesman'),
    )
    email = models.EmailField(null=True, blank=True)
    mobile = models.BigIntegerField(null=True, unique=True)
    role = models.CharField(max_length=40, choices=roles)
    added_by = models.ForeignKey('self', null=True, blank=True)
