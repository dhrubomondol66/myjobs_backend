from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    INDUSTRY_CHOICES = [
        ('GP', 'Grameenphone'),
        ('ROBI', 'Robi Axiata'),
        ('BR', 'BRAC'),
        ('DBBL', 'Dutch-bangla-bank'),
        ('SQG', 'Square Group'),
        ('ACI', 'Aci Limited'),
        ('Other', 'Other'),
    ]
    # I want to use this industry choice as Radio buttons in my react frontend. 
    # So when i click on a radio button, i want to send the value to the backend.
    # So i need to make sure that the value is sent to the backend.
    # So i need to make sure that the value is sent to the backend.
    # So i need to make sure that the value is sent to the backend.
    # So i need to make sure that the value is sent to the backend.
    # So i need to make sure that the value is sent to the backend.
    email = models.EmailField(unique=True)
    industry = models.CharField(max_length=100, choices=INDUSTRY_CHOICES, null=True, blank=True)
    years_of_experience = models.IntegerField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    credits = models.IntegerField(default=0)

class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name