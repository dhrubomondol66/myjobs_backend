from django.db import models
from django.conf import settings

class UserProfile(models.Model):

    WORK_STATUS_CHOICES = [
        ("WORKING", "Working"),
        ("UNEMPLOYED", "Unemployed"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    # Profile basic info
    full_name = models.CharField(max_length=150)

    # Work info
    current_work_status = models.CharField(
        max_length=20,
        choices=WORK_STATUS_CHOICES,
        default="UNEMPLOYED"
    )

    current_designation = models.CharField(max_length=150, blank=True, null=True)
    current_industry = models.CharField(max_length=150, blank=True, null=True)
    current_company = models.CharField(max_length=150, blank=True, null=True)

    # Salary info
    current_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    # Location
    city = models.CharField(max_length=100, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.user.email}"
