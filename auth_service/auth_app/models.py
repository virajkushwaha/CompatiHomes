from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('tenant', 'Tenant'),
        ('landlord', 'Landlord'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
     # For tenant-specific questions
    tenant_answers = models.JSONField(default=dict,blank=True)  # Store answers as JSON
    
    # For landlord-specific questions
    landlord_answers = models.JSONField(default=dict,blank=True)  # Store answers as JSON

    def __str__(self):
        return self.username

class Landlord(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.user.username


# Create your models here.
