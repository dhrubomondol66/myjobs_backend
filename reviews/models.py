from django.db import models
from companies.models import Company
from django.conf import settings

class CompanyReview(models.Model):
    RECOMMEND_CHOICES = [
        ("definitely", "Definitely"),
        ("probably", "Probably"),
        ("neutral", "Neutral"),
        ("probably_not", "Probably not"),
        ("no", "No"),
    ]

    COMPANY_TYPE = [
        ("local", "Local"),
        ("mnc", "MNC"),
        ("startup", "Startup"),
        ("ngo", "NGO"),
        ("government", "Government"),
    ]

    RECOMMENDATION_CHOICES = [
        ("definitely", "Definitely"),
        ("probably", "Probably"),
        ("neutral", "Neutral"),
        ("probably_not", "Probably not"),
        ("no", "No"),
    ]


    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    is_anonymous = models.BooleanField(default=True)

    company_type = models.CharField(max_length=20, choices=COMPANY_TYPE)

    brand_value = models.IntegerField()
    work_environment = models.IntegerField()
    career_growth = models.IntegerField()
    work_life_balance = models.IntegerField()
    management_quality = models.IntegerField()
    salary_benefits = models.IntegerField()

    recommendation = models.CharField(
        max_length=50,
        choices=RECOMMENDATION_CHOICES,
        default='neutral'
    )

    overall_experience = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company.name} Review"