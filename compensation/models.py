from django.db import models
from django.conf import settings
from companies.models import Company

class CompensationData(models.Model):

    FAIRNESS_CHOICES = [
        (1, "Way below market"),
        (2, "Slightly below market"),
        (3, "Fair"),
        (4, "Above market"),
        (5, "Way above market"),
    ]

    BENEFIT_CHOICES = [
        ("NONE", "No benefits"),
        ("5K_15K", "৳5k–৳15k"),
        ("15K_30K", "৳15k–৳30k"),
        ("30K_PLUS", "৳30k+"),
    ]

    BONUS_CHOICES = [
        ("NONE", "No bonus"),
        ("ONE", "1 festival bonus"),
        ("TWO", "2 festival bonuses"),
        ("TWO_PERFORMANCE", "2 bonuses + performance"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    base_salary = models.DecimalField(max_digits=12, decimal_places=2)
    fringe_benefits_value = models.CharField(max_length=20, choices=BENEFIT_CHOICES)
    other_allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bonus_amount = models.CharField(max_length=30, choices=BONUS_CHOICES)
    market_fairness_rating = models.IntegerField(choices=FAIRNESS_CHOICES)
    is_anonymous = models.BooleanField(default=True)
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company.name} - {self.job_title}"