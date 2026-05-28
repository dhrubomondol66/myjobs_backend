from django.db import models
from django.conf import settings

class Company(models.Model):
    COMPANY_TYPES = [
        ('LOCAL', 'Local'),
        ('MNC', 'MNC'),
        ('STARTUP', 'Startup'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="companies")
    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=20, choices=COMPANY_TYPES)
    industry = models.CharField(max_length=100)
    manpower_size = models.CharField(max_length=20)
    headquarters = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# ------------------------------------------------------------------
# DataExchange model – anonymous data contribution / retrieval
# ------------------------------------------------------------------
class DataExchange(models.Model):
    """Professionals can voluntarily submit anonymised company data and receive
    verified data from other companies.  The ``is_anonymous`` flag hides the
    contributor's identity when ``True``.
    """
    provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="data_exchanges")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="data_exchanges")
    is_anonymous = models.BooleanField(default=True)
    # Store arbitrary structured data as JSON – e.g., salary, benefits, culture scores
    payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"DataExchange for {self.company.name} by {'anonymous' if self.is_anonymous else self.provider.username}"

    class Meta:
        ordering = ["-created_at"]