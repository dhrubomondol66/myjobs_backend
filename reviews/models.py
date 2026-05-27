from django.db import models
from companies.models import Company
from django.conf import settings

class CompanyReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_anonymous = models.BooleanField(default=True)
    brand_value = models.IntegerField()        # ১-৫
    work_environment = models.IntegerField()   # ১-৫
    career_growth = models.IntegerField()      # ১-৫
    salary_range_perception = models.IntegerField()
    fringe_benefits = models.IntegerField()
    job_security = models.IntegerField()
    employee_respect = models.IntegerField()
    overall_recommendation = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)