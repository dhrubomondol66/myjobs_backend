from django.db import models
from django.conf import settings
from companies.models import Company

class SalaryAnalytics(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    job_title = models.CharField(max_length=200)
    department = models.CharField(max_length=100)

    base_salary = models.DecimalField(max_digits=12, decimal_places=2)
    fringe_benefits_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bonus_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    market_fairness_rating = models.IntegerField()

    is_anonymous = models.BooleanField(default=True)
    year = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company.name} - {self.job_title}"